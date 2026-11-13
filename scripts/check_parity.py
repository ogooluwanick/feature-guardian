#!/usr/bin/env python3
"""Inspect recorded parity cards/units; never execute evidence commands or certify runtime behavior.

Schema 2 (preferred): lean parity cards with provider + check_here + hashes.
Schema 1 (legacy): detailed units with aspect/variant fields.

OK/PASS demotes to STALE when listed source hashes no longer match disk.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

START = "<!-- FG:PARITY:START -->"
END = "<!-- FG:PARITY:END -->"
# Card statuses; PASS is legacy schema-1 alias for OK.
STATES = {"OK", "PASS", "FAIL", "UNKNOWN", "STALE", "NOT_APPLICABLE"}
ASPECTS = {
    "collection",
    "validation",
    "storage",
    "meaning",
    "visibility",
    "presentation",
    "logic",
    "props",
}


def normalize_state(state: str) -> str:
    if state == "OK":
        return "PASS"
    return state


def summarize(states: List[str], scope_reviewed: bool = False) -> dict:
    normalized = [normalize_state(s) for s in states]
    counts = {state: normalized.count(state) for state in ("PASS", "FAIL", "UNKNOWN", "STALE", "NOT_APPLICABLE")}
    applicable = len(normalized) - counts["NOT_APPLICABLE"]
    known = counts["PASS"] + counts["FAIL"]
    status = "FAIL" if counts["FAIL"] else (
        "PASS"
        if applicable and scope_reviewed and counts["PASS"] == applicable and counts["STALE"] == 0
        else "UNKNOWN"
    )
    if counts["STALE"] and status != "FAIL":
        status = "STALE" if counts["STALE"] == applicable else "UNKNOWN"
    return {
        "status": status,
        "passed": counts["PASS"],
        "failed": counts["FAIL"],
        "unknown": counts["UNKNOWN"],
        "stale": counts["STALE"],
        "not_applicable": counts["NOT_APPLICABLE"],
        "applicable": applicable,
        "parity_percent": round(100 * counts["PASS"] / applicable, 2) if applicable else None,
        "evidence_coverage_percent": round(100 * known / applicable, 2) if applicable else None,
        "scope_reviewed": scope_reviewed,
        "blocks_done": bool(counts["FAIL"] or counts["STALE"]),
    }


def source_is_current(root: Path, name: str, expected: str) -> bool:
    if not isinstance(name, str) or not isinstance(expected, str):
        return False
    target = (root / name).resolve()
    try:
        target.relative_to(root.resolve())
        return (
            not Path(name).is_absolute()
            and hashlib.sha256(target.read_bytes()).hexdigest() == expected
        )
    except (ValueError, OSError):
        return False


def evidence_matches(text: str, evidence_id: str, state: str) -> bool:
    if not isinstance(evidence_id, str) or not re.fullmatch(r"FG-EVID-\d{6}", evidence_id):
        return False
    match = re.search(
        r"^###\s+" + re.escape(evidence_id) + r"\s*\n(.*?)(?=^### |<!-- FG:[^>]+:END -->|\Z)",
        text,
        re.M | re.S,
    )
    if not match:
        return False
    body = match.group(1)
    result_state = "PASS" if state == "OK" else state
    return bool(
        re.search(r"^Result:\s*" + result_state + r"\s*$", body, re.M)
        and re.search(r"^Environment:\s*\S.+$", body, re.M)
        and re.search(r"^Timestamp:\s*\d{4}-\d{2}-\d{2}\S*\s*$", body, re.M)
        and (result_state != "PASS" or re.search(r"^Freshness:\s*FRESH\s*$", body, re.M))
    )


def hash_paths_current(root: Path, paths: List[str], hashes: Any) -> bool:
    if not isinstance(hashes, dict) or not hashes:
        return False
    for path in paths:
        if path not in hashes or not source_is_current(root, path, hashes[path]):
            return False
    for name, value in hashes.items():
        if not source_is_current(root, name, value):
            return False
    return True


def inspect_schema1_units(
    data: dict, text: str, root: Path, errors: List[str], warnings: List[str]
) -> tuple[List[str], List[dict], bool]:
    if not isinstance(data.get("scope_reviewed", False), bool):
        raise ValueError("scope_reviewed must be a boolean.")
    scope_reviewed = data.get("scope_reviewed", False)
    states: List[str] = []
    units_out: List[dict] = []
    ids: Set[str] = set()
    for index, unit in enumerate(data.get("units", [])):
        if not isinstance(unit, dict):
            errors.append(f"Unit {index}: expected an object.")
            states.append("UNKNOWN")
            continue
        uid = unit.get("id", "")
        if not isinstance(uid, str) or not uid.strip() or uid in ids:
            errors.append(f"Unit {index}: missing or duplicate id.")
        if isinstance(uid, str):
            ids.add(uid)
        for key in ["contract", "provider", "consumer", "variant"]:
            if not isinstance(unit.get(key), str) or not unit[key].strip():
                errors.append(f"{uid}: missing {key}.")
        state = unit.get("status", "UNKNOWN")
        if not isinstance(state, str) or state not in STATES:
            errors.append(f"{uid}: invalid status.")
            state = "UNKNOWN"
        if unit.get("aspect") not in ASPECTS:
            errors.append(f"{uid}: invalid aspect.")
        if state == "NOT_APPLICABLE" and not (
            isinstance(unit.get("reason"), str) and unit["reason"].strip()
        ):
            errors.append(f"{uid}: NOT_APPLICABLE requires a reason.")
            state = "UNKNOWN"
        if state in {"PASS", "OK", "FAIL"}:
            evidence = unit.get("evidence", [])
            check_state = "PASS" if state == "OK" else state
            if not isinstance(evidence, list) or not evidence or any(
                not evidence_matches(text, eid, check_state) for eid in evidence
            ):
                errors.append(
                    f"{uid}: {state} requires matching result/environment/timestamp evidence "
                    "records in the owning feature file (PASS/OK also requires FRESH)."
                )
                state = "UNKNOWN"
        if state in {"PASS", "OK"}:
            hashes = unit.get("source_hashes", {})
            required = [unit.get("provider"), unit.get("consumer")]
            if not hash_paths_current(root, [p for p in required if isinstance(p, str)], hashes):
                warnings.append(f"{uid}: source coverage missing or changed; PASS demoted to STALE.")
                state = "STALE"
        states.append(state)
        units_out.append({**unit, "effective_status": normalize_state(state)})
    return states, units_out, scope_reviewed


def inspect_schema2_cards(
    data: dict, text: str, root: Path, errors: List[str], warnings: List[str]
) -> tuple[List[str], List[dict], bool]:
    items = data.get("items")
    if not isinstance(items, list):
        raise ValueError("Expected items array for schema_version 2.")
    # Cards are always "scope reviewed" for listed items only; inventory growth is additive.
    scope_reviewed = True if items else False
    states: List[str] = []
    units_out: List[dict] = []
    ids: Set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"Item {index}: expected an object.")
            states.append("UNKNOWN")
            continue
        uid = item.get("id", "")
        if not isinstance(uid, str) or not uid.strip() or uid in ids:
            errors.append(f"Item {index}: missing or duplicate id.")
        if isinstance(uid, str):
            ids.add(uid)
        for key in ["contract", "provider"]:
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"{uid}: missing {key}.")
        check_here = item.get("check_here", [])
        if not isinstance(check_here, list) or not check_here or any(
            not isinstance(p, str) or not p.strip() for p in check_here
        ):
            errors.append(f"{uid}: check_here must be a non-empty list of paths.")
            check_here = []
        diffs = item.get("intentional_diffs", "none")
        if not isinstance(diffs, str) or not diffs.strip():
            errors.append(f"{uid}: intentional_diffs required (use 'none' if none).")
        state = item.get("status", "UNKNOWN")
        if not isinstance(state, str) or state not in STATES:
            errors.append(f"{uid}: invalid status.")
            state = "UNKNOWN"
        if state == "NOT_APPLICABLE" and not (
            isinstance(item.get("reason"), str) and item["reason"].strip()
        ):
            errors.append(f"{uid}: NOT_APPLICABLE requires a reason.")
            state = "UNKNOWN"
        if state in {"OK", "PASS", "FAIL"}:
            evidence = item.get("evidence", [])
            check_state = "PASS" if state in {"OK", "PASS"} else state
            if not isinstance(evidence, list) or not evidence or any(
                not evidence_matches(text, eid, check_state) for eid in evidence
            ):
                errors.append(
                    f"{uid}: {state} requires matching evidence records "
                    "(Result/Environment/Timestamp; PASS/OK needs Freshness: FRESH)."
                )
                state = "UNKNOWN"
        tracked = []
        if isinstance(item.get("provider"), str):
            tracked.append(item["provider"])
        tracked.extend([p for p in check_here if isinstance(p, str)])
        if state in {"OK", "PASS"}:
            if not hash_paths_current(root, tracked, item.get("source_hashes", {})):
                warnings.append(
                    f"{uid}: listed sources missing or changed; OK/PASS demoted to STALE."
                )
                state = "STALE"
        states.append(state)
        units_out.append(
            {
                **item,
                "effective_status": normalize_state(state),
                "schema": 2,
            }
        )
    return states, units_out, scope_reviewed


def inspect_feature(feature: Path, root: Path) -> dict:
    text = feature.read_text(encoding="utf-8")
    report: Dict[str, Any] = {
        "feature": feature.stem,
        "errors": [],
        "warnings": [],
        "units": [],
        "drifts": [],
        "present": START in text or END in text,
    }
    errors, warnings = report["errors"], report["warnings"]
    states: List[str] = []
    scope_reviewed = False
    if START not in text and END not in text:
        warnings.append(
            "Parity index absent; initialize lazily on the next relevant feature change."
        )
    elif text.count(START) != 1 or text.count(END) != 1 or text.index(END) < text.index(START):
        errors.append("Parity section must have one ordered START/END marker pair.")
    else:
        section = text.split(START, 1)[1].split(END, 1)[0]
        blocks = re.findall(r"```json\s*\n(.*?)\n```", section, re.S)
        try:
            if len(blocks) != 1:
                raise ValueError("Parity section requires exactly one JSON manifest.")
            data = json.loads(blocks[0])
            if not isinstance(data, dict):
                raise ValueError("Parity manifest must be a JSON object.")
            version = data.get("schema_version")
            if version == 2:
                states, units, scope_reviewed = inspect_schema2_cards(
                    data, text, root, errors, warnings
                )
            elif version == 1:
                if not isinstance(data.get("units"), list):
                    raise ValueError("Expected schema_version: 1 and units array.")
                states, units, scope_reviewed = inspect_schema1_units(
                    data, text, root, errors, warnings
                )
            else:
                raise ValueError("Expected schema_version 1 (units) or 2 (parity cards).")
            report["units"] = units
            for unit in units:
                eff = unit.get("effective_status")
                if eff in {"STALE", "FAIL"}:
                    report["drifts"].append(
                        {
                            "id": unit.get("id"),
                            "status": eff,
                            "contract": unit.get("contract"),
                            "provider": unit.get("provider"),
                            "check_here": unit.get("check_here")
                            or ([unit.get("consumer")] if unit.get("consumer") else []),
                        }
                    )
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            errors.append(str(exc))
    report.update(summarize(states, scope_reviewed))
    if errors:
        report["status"] = "FAIL"
        report["blocks_done"] = True
    frontmatter = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    claim = (
        re.search(r"^parity-claim:\s*['\"]?([A-Z_]+)['\"]?\s*$", frontmatter.group(1), re.M)
        if frontmatter
        else None
    )
    if claim and claim.group(1) not in {"UNKNOWN", "PARTIAL", "VERIFIED"}:
        errors.append("Invalid parity-claim.")
        report["status"] = "FAIL"
        report["blocks_done"] = True
    if claim and claim.group(1) == "VERIFIED" and report["status"] != "PASS":
        errors.append(
            "VERIFIED parity claim requires reviewed scope and all applicable items "
            "PASS/OK with current sources."
        )
        report["status"] = "FAIL"
        report["blocks_done"] = True
    return report


def format_user_drift_report(report: dict) -> str:
    """Plain-text block agents must show the user when drifts exist."""
    drifts = report.get("drifts") or []
    if not drifts and not report.get("blocks_done"):
        return ""
    lines = ["Parity drift report:", f"Feature: {report.get('feature')}"]
    if not drifts:
        lines.append("No item-level drifts listed; see checker errors/warnings.")
    for d in drifts:
        lines.append(
            f"- [{d.get('status')}] {d.get('id')}: {d.get('contract')} "
            f"(provider={d.get('provider')}; check_here={', '.join(d.get('check_here') or [])})"
        )
    lines.append(
        "Action: fix obvious mechanical drift, or ask the user when the fix is ambiguous "
        "or needs a product/business decision. Do not claim done while blocks_done is true."
    )
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", default=".")
    parser.add_argument("--feature", help="Feature slug; default all features")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when status is not PASS or when STALE/FAIL blocks_done",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Print human drift report for features with drifts",
    )
    args = parser.parse_args(argv)
    root = Path(args.project).resolve()
    files = sorted((root / ".feature-guardian/features").glob("*.md"))
    if args.feature:
        files = [file for file in files if file.stem == args.feature]
    if not files:
        print("No matching feature memory files.", file=sys.stderr)
        return 2
    reports = [inspect_feature(file, root) for file in files]
    print(json.dumps({"metric": "feature-parity", "features": reports}, indent=2))
    if args.report:
        for report in reports:
            text = format_user_drift_report(report)
            if text:
                print(text, file=sys.stderr)
    if any(report["errors"] for report in reports):
        return 1
    if args.check and any(
        report["status"] != "PASS" or report.get("blocks_done") for report in reports
    ):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
