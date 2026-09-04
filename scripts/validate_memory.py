#!/usr/bin/env python3
"""Feature Guardian memory validator (v0.1.0).

Validates .feature-guardian/ product and feature memory for structural integrity.
Does not modify memory unless an explicit repair mode is added in a future version.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple

FG_SCHEMA_VERSION = "0.1"
SKILL_VERSION = "0.1.0"

VALID_FEATURE_STATUSES = {
    "DISCOVERED",
    "PLANNED",
    "IN_DEVELOPMENT",
    "TESTING",
    "BLOCKED",
    "REVIEW_REQUIRED",
    "REGRESSED",
    "COMPLETED",
    "DEPRECATED",
}
VALID_MONITORING = {"ACTIVE", "DORMANT", "ACTIVE_REVIEW", "EXCLUDED"}
VALID_HEALTH = {"HEALTHY", "DEGRADED", "UNSAFE", "UNKNOWN"}
VALID_CONFIDENCE = {"HIGH", "MEDIUM", "LOW", "UNKNOWN"}

HEADING_ID_RE = re.compile(r"^###\s+(FG-(?:FEAT|REQ|INV|TEST|EVID|ISSUE|REG|DEC|RISK|DEP|CONTRACT|UNK|ASM|CHG|DEBT|ROLLBACK|EVT)-\d{6})\s*$", re.MULTILINE)
FEATURE_ID_FM_RE = re.compile(r"^feature-id:\s*(FG-FEAT-\d{6})\s*$", re.MULTILINE)
ID_PATTERN = re.compile(
    r"\b(FG-(?:FEAT|REQ|INV|TEST|EVID|ISSUE|REG|DEC|RISK|DEP|CONTRACT|UNK|ASM|CHG|DEBT|ROLLBACK|EVT)-\d{6})\b"
)
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
REGISTRY_ROW_RE = re.compile(
    r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
    re.MULTILINE,
)
SLUG_FROM_FILENAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
OPEN_CRITICAL_REGRESSION_RE = re.compile(
    r"###\s+(FG-REG-\d{6}).*?\n(?:.*?\n)*?Severity:\s*\n?\s*CRITICAL.*?\n(?:.*?\n)*?Status:\s*\n?\s*OPEN",
    re.IGNORECASE | re.DOTALL,
)
OPEN_BLOCKING_ISSUE_RE = re.compile(
    r"###\s+(FG-ISSUE-\d{6}).*?\n(?:.*?\n)*?Severity:\s*\n?\s*(?:CRITICAL|BLOCKING).*?\n(?:.*?\n)*?Status:\s*\n?\s*OPEN",
    re.IGNORECASE | re.DOTALL,
)


@dataclass
class ValidationMessage:
    level: str  # error | warning
    code: str
    message: str
    path: Optional[str] = None


@dataclass
class ValidationResult:
    messages: List[ValidationMessage] = field(default_factory=list)

    @property
    def errors(self) -> List[ValidationMessage]:
        return [m for m in self.messages if m.level == "error"]

    @property
    def warnings(self) -> List[ValidationMessage]:
        return [m for m in self.messages if m.level == "warning"]

    def add(self, level: str, code: str, message: str, path: Optional[str] = None) -> None:
        self.messages.append(ValidationMessage(level, code, message, path))


def parse_simple_yaml(text: str) -> Dict[str, str]:
    """Parse minimal YAML frontmatter without external dependencies."""
    data: Dict[str, str] = {}
    current_key: Optional[str] = None
    list_values: List[str] = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line or line.strip().startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            list_values.append(line[4:].strip().strip('"').strip("'"))
            data[current_key] = "\n".join(list_values)
            continue
        if ":" in line and not line.startswith(" "):
            if current_key and list_values:
                data[current_key] = "\n".join(list_values)
            list_values = []
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            current_key = key
            if value == "":
                continue
            if value in ("null", "~"):
                data[key] = ""
            else:
                data[key] = value
    if current_key and list_values:
        data[current_key] = "\n".join(list_values)
    return data


def read_frontmatter(path: Path) -> Tuple[Dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    return parse_simple_yaml(match.group(1)), text


def extract_ids(text: str) -> Set[str]:
    return set(ID_PATTERN.findall(text))


def extract_definition_ids(text: str, path: Path) -> Dict[str, List[str]]:
    """Return IDs that define entities (not mere cross-references)."""
    definitions: Dict[str, List[str]] = {}
    loc = str(path)

    for match in FEATURE_ID_FM_RE.finditer(text):
        definitions.setdefault(match.group(1), []).append(f"{loc}:frontmatter")

    for match in HEADING_ID_RE.finditer(text):
        entity_id = match.group(1)
        definitions.setdefault(entity_id, []).append(f"{loc}:heading")

    return definitions


def slug_from_path(path: Path) -> str:
    return path.stem


def parse_feature_registry(product_text: str) -> Dict[str, Dict[str, str]]:
    """Parse FEATURE REGISTRY table rows. Keyed by feature ID."""
    registry: Dict[str, Dict[str, str]] = {}
    in_registry = False
    for line in product_text.splitlines():
        if "FEATURE REGISTRY" in line.upper():
            in_registry = True
            continue
        if in_registry and line.startswith("## ") and "REGISTRY" not in line.upper():
            break
        if not in_registry or not line.startswith("|"):
            continue
        if re.match(r"^\|\s*[-:]+\s*\|", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 7:
            continue
        feature_id, name, status = cells[0], cells[1], cells[2]
        if not feature_id.startswith("FG-FEAT-"):
            continue
        registry[feature_id] = {
            "feature_id": feature_id,
            "name": name,
            "status": status,
            "health": cells[3],
            "confidence": cells[4],
            "monitoring": cells[5],
            "last_verified": cells[6],
        }
    return registry


def find_slug_in_registry(product_text: str, slug: str) -> Optional[str]:
    slug_pattern = re.compile(rf"\bslug:\s*{re.escape(slug)}\b", re.IGNORECASE)
    if slug_pattern.search(product_text):
        return slug
    alias_pattern = re.compile(rf"^\s*-\s*{re.escape(slug)}\s*$", re.MULTILINE)
    if alias_pattern.search(product_text):
        return slug
    return None


def collect_referenced_ids(text: str, prefix: str) -> Set[str]:
    return {i for i in extract_ids(text) if i.startswith(prefix)}


def validate_project(project_root: Path) -> ValidationResult:
    result = ValidationResult()
    memory_root = project_root / ".feature-guardian"
    product_path = memory_root / "PRODUCT.md"
    features_dir = memory_root / "features"

    if not memory_root.is_dir():
        result.add("error", "FG001", f"Missing memory directory: {memory_root}")
        return result

    if not product_path.is_file():
        result.add("error", "FG002", f"Missing PRODUCT.md: {product_path}")
        return result

    product_fm, product_text = read_frontmatter(product_path)
    validate_product_frontmatter(product_fm, product_path, result)
    validate_product_sections(product_text, product_path, result)

    if not features_dir.is_dir():
        result.add("warning", "FG003", f"Features directory missing: {features_dir}")

    feature_files = sorted(features_dir.glob("*.md")) if features_dir.is_dir() else []
    registry = parse_feature_registry(product_text)
    registry_ids = set(registry.keys())
    file_ids: Dict[str, Path] = {}
    file_slugs: Dict[str, Path] = {}
    slug_values: Dict[str, Path] = {}
    all_ids: Dict[str, List[str]] = {}
    definition_sites: Dict[str, List[str]] = {}

    def register_id(entity_id: str, location: str) -> None:
        all_ids.setdefault(entity_id, []).append(location)

    for entity_id in extract_ids(product_text):
        register_id(entity_id, str(product_path))
    for def_id, sites in extract_definition_ids(product_text, product_path).items():
        definition_sites.setdefault(def_id, []).extend(sites)

    for feature_path in feature_files:
        slug = slug_from_path(feature_path)
        if slug in file_slugs:
            result.add(
                "error",
                "FG004",
                f"Duplicate feature slug filename: {slug}",
                str(feature_path),
            )
        file_slugs[slug] = feature_path

        if not SLUG_FROM_FILENAME_RE.match(feature_path.name):
            result.add(
                "warning",
                "FG005",
                f"Feature filename should be kebab-case slug: {feature_path.name}",
                str(feature_path),
            )

        fm, text = read_frontmatter(feature_path)
        validate_feature_frontmatter(fm, feature_path, result)

        slug_value = fm.get("slug", slug)
        if slug_value:
            if slug_value in slug_values:
                result.add(
                    "error",
                    "FG031",
                    f"Duplicate canonical slug '{slug_value}' in {slug_values[slug_value]} and {feature_path}",
                    str(feature_path),
                )
            slug_values[slug_value] = feature_path

        feature_id = fm.get("feature-id", "")
        if feature_id:
            if feature_id in file_ids:
                result.add(
                    "error",
                    "FG006",
                    f"Duplicate feature-id {feature_id} in {file_ids[feature_id]} and {feature_path}",
                    str(feature_path),
                )
            file_ids[feature_id] = feature_path

        for entity_id in extract_ids(text):
            register_id(entity_id, str(feature_path))
        for def_id, sites in extract_definition_ids(text, feature_path).items():
            definition_sites.setdefault(def_id, []).extend(sites)

        validate_feature_body(text, fm, feature_path, result)

    for entity_id, sites in definition_sites.items():
        if entity_id.startswith("FG-FEAT-"):
            frontmatter_sites = [s for s in sites if s.endswith(":frontmatter")]
            if len(frontmatter_sites) > 1:
                result.add(
                    "error",
                    "FG007",
                    f"Duplicate feature identity {entity_id} defined in: {', '.join(sorted(set(frontmatter_sites)))}",
                )
            continue
        if len(sites) > 1:
            result.add(
                "error",
                "FG007",
                f"Duplicate stable ID {entity_id} defined in: {', '.join(sorted(set(sites)))}",
            )

    feature_ids_in_files = set(file_ids.keys())
    for reg_id in registry_ids:
        if reg_id not in feature_ids_in_files:
            result.add(
                "error",
                "FG008",
                f"Registry references missing feature file for {reg_id}",
                str(product_path),
            )
    for feat_id, feat_path in file_ids.items():
        if feat_id not in registry_ids:
            result.add(
                "error",
                "FG009",
                f"Feature file not listed in product registry: {feat_id}",
                str(feat_path),
            )

    defined_test_ids = {eid for eid in definition_sites if eid.startswith("FG-TEST-")}
    defined_feat_ids = {
        eid for eid, sites in definition_sites.items()
        if eid.startswith("FG-FEAT-") and any(s.endswith(":frontmatter") for s in sites)
    }
    cross_reference_checks(
        product_text, feature_files, defined_test_ids, defined_feat_ids, result
    )

    return result


def validate_product_frontmatter(fm: Dict[str, str], path: Path, result: ValidationResult) -> None:
    schema = fm.get("fg-schema", "")
    if schema and schema != FG_SCHEMA_VERSION:
        result.add(
            "warning",
            "FG010",
            f"PRODUCT.md fg-schema {schema} differs from validator schema {FG_SCHEMA_VERSION}",
            str(path),
        )
    if not fm.get("fg-schema"):
        result.add("warning", "FG011", "PRODUCT.md missing fg-schema in frontmatter", str(path))


def validate_product_sections(text: str, path: Path, result: ValidationResult) -> None:
    required_sections = [
        "IDENTITY",
        "FAST CONTEXT",
        "FEATURE REGISTRY",
        "FEATURE RELATIONSHIP MAP",
        "CURRENT PRODUCT HEALTH",
    ]
    upper = text.upper()
    for section in required_sections:
        if section not in upper:
            result.add(
                "warning",
                "FG012",
                f"PRODUCT.md missing recommended section: {section}",
                str(path),
            )


def validate_feature_frontmatter(fm: Dict[str, str], path: Path, result: ValidationResult) -> None:
    loc = str(path)
    if not fm:
        result.add("error", "FG013", "Feature file missing YAML frontmatter", loc)
        return

    schema = fm.get("fg-schema", "")
    if schema and schema != FG_SCHEMA_VERSION:
        result.add(
            "warning",
            "FG014",
            f"fg-schema {schema} differs from validator schema {FG_SCHEMA_VERSION}",
            loc,
        )
    elif not schema:
        result.add("error", "FG015", "Missing fg-schema in feature frontmatter", loc)

    feature_id = fm.get("feature-id", "")
    if not feature_id.startswith("FG-FEAT-"):
        result.add("error", "FG016", "Missing or invalid feature-id in frontmatter", loc)

    slug = fm.get("slug", "")
    expected_slug = slug_from_path(path)
    if slug and slug != expected_slug:
        result.add(
            "warning",
            "FG017",
            f"Frontmatter slug '{slug}' does not match filename '{expected_slug}'",
            loc,
        )

    status = fm.get("status", "")
    if status and status not in VALID_FEATURE_STATUSES:
        result.add("error", "FG018", f"Invalid feature status: {status}", loc)

    monitoring = fm.get("monitoring", "")
    if monitoring and monitoring not in VALID_MONITORING:
        result.add("error", "FG019", f"Invalid monitoring state: {monitoring}", loc)

    health = fm.get("health", "")
    if health and health not in VALID_HEALTH:
        result.add("error", "FG020", f"Invalid health value: {health}", loc)

    confidence = fm.get("confidence", "")
    if confidence and confidence not in VALID_CONFIDENCE:
        result.add("error", "FG021", f"Invalid confidence value: {confidence}", loc)

    revision = fm.get("memory-revision", "")
    if revision and not revision.isdigit():
        result.add("error", "FG022", f"memory-revision must be numeric: {revision}", loc)


def validate_feature_body(text: str, fm: Dict[str, str], path: Path, result: ValidationResult) -> None:
    loc = str(path)
    status = fm.get("status", "")

    required_markers = [
        "FG:FAST_CONTEXT",
        "FG:CURRENT_STATE",
        "FG:IMMUTABLE_EVENT_HISTORY",
    ]
    for marker in required_markers:
        if marker not in text:
            result.add(
                "warning",
                "FG023",
                f"Missing section marker: {marker}",
                loc,
            )

    if status == "COMPLETED":
        if OPEN_CRITICAL_REGRESSION_RE.search(text):
            result.add(
                "error",
                "FG024",
                "COMPLETED feature has open CRITICAL regression",
                loc,
            )
        if OPEN_BLOCKING_ISSUE_RE.search(text):
            result.add(
                "error",
                "FG025",
                "COMPLETED feature has open blocking/critical issue",
                loc,
            )
        if "Freshness: STALE" in text or "freshness: STALE" in text:
            result.add(
                "warning",
                "FG026",
                "COMPLETED feature has stale status-relevant evidence",
                loc,
            )

    test_ids_in_registry = collect_referenced_ids(text, "FG-TEST-")
    for test_id in re.findall(r"Protected by:\s*\n(?:\s*-\s*(FG-TEST-\d{6})\s*\n?)+", text):
        pass
    for match in re.finditer(r"Protected by:\s*\n((?:\s*-\s*FG-TEST-\d{6}\s*\n)+)", text):
        for tid in re.findall(r"FG-TEST-\d{6}", match.group(1)):
            if tid not in test_ids_in_registry and tid not in text:
                result.add(
                    "warning",
                    "FG027",
                    f"Referenced test ID {tid} not found in feature body",
                    loc,
                )

    if "CONTRADICTION" in text.upper() and "Status: OPEN" in text:
        result.add(
            "warning",
            "FG028",
            "Feature has open contradiction requiring reconciliation",
            loc,
        )


def cross_reference_checks(
    product_text: str,
    feature_files: Iterable[Path],
    defined_test_ids: Set[str],
    defined_feat_ids: Set[str],
    result: ValidationResult,
) -> None:
    for feature_path in feature_files:
        text = feature_path.read_text(encoding="utf-8")
        loc = str(feature_path)
        own_feat = re.search(r"feature-id:\s*(FG-FEAT-\d{6})", text)
        own_feat_id = own_feat.group(1) if own_feat else None
        for test_ref in set(ID_PATTERN.findall(text)):
            if not test_ref.startswith("FG-TEST-"):
                continue
            if test_ref not in defined_test_ids:
                result.add(
                    "warning",
                    "FG029",
                    f"Referenced test ID {test_ref} not defined in memory corpus",
                    loc,
                )
        for feat_ref in set(ID_PATTERN.findall(text)):
            if not feat_ref.startswith("FG-FEAT-"):
                continue
            if feat_ref != own_feat_id and feat_ref not in defined_feat_ids:
                result.add(
                    "warning",
                    "FG030",
                    f"Referenced feature ID {feat_ref} not defined in memory corpus",
                    loc,
                )


def format_messages(result: ValidationResult) -> str:
    lines: List[str] = []
    for msg in result.errors:
        prefix = f"ERROR [{msg.code}]"
        loc = f" ({msg.path})" if msg.path else ""
        lines.append(f"{prefix}{loc}: {msg.message}")
    for msg in result.warnings:
        prefix = f"WARNING [{msg.code}]"
        loc = f" ({msg.path})" if msg.path else ""
        lines.append(f"{prefix}{loc}: {msg.message}")
    if not lines:
        lines.append("OK: Feature Guardian memory validation passed.")
    lines.append("")
    lines.append(
        f"Summary: {len(result.errors)} error(s), {len(result.warnings)} warning(s)"
    )
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Feature Guardian memory")
    parser.add_argument(
        "project",
        nargs="?",
        default=".",
        help="Project root containing .feature-guardian/ (default: current directory)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"feature-guardian-validate {SKILL_VERSION} (schema {FG_SCHEMA_VERSION})",
    )
    args = parser.parse_args(argv)
    project_root = Path(args.project).resolve()
    result = validate_project(project_root)
    print(format_messages(result))
    return 1 if result.errors else 0


if __name__ == "__main__":
    sys.exit(main())
