#!/usr/bin/env python3
"""Suggest or apply peer relationships from code, PRODUCT map, and contracts.

Usage:
  python infer_peers.py . --feature invoicing
  python infer_peers.py . --feature invoicing --apply
  python infer_peers.py . --all --limit 5
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from fg_memory_lib import (
    RELATED_BLOCK_RE,
    RELATED_FIELD_RE,
    default_search_roots,
    extract_code_location_globs,
    parse_related_features,
    read_frontmatter,
    slug_from_path,
    split_peer_list,
)

SKILL_VERSION = "0.1.5"
IMPORT_FROM_RE = re.compile(
    r"""(?:import\s+[^'"]+from\s+|import\s*\(\s*)['"]@/([^'"]+)['"]""",
    re.MULTILINE,
)
PRODUCT_MAP_RE = re.compile(
    r"## FEATURE RELATIONSHIP MAP\s*\n+```(?:text)?\n(.*?)```",
    re.DOTALL | re.IGNORECASE,
)
CONTRACT_BLOCK_RE = re.compile(
    r"### (FG-CONTRACT-\d{6})\s*\n(.*?)(?=### FG-CONTRACT|\Z)",
    re.DOTALL,
)
SLUG_IN_TEXT_RE = re.compile(r"\b[a-z][a-z0-9]*(?:-[a-z0-9]+)*\b")

CODE_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx"}


@dataclass
class PeerSuggestion:
    slug: str
    source: str
    confidence: str
    relation: str


@dataclass
class InferResult:
    slug: str
    documented: Dict[str, List[str]]
    suggested: Dict[str, List[PeerSuggestion]] = field(default_factory=dict)
    gaps: Dict[str, List[str]] = field(default_factory=dict)


def load_all_slugs(features_dir: Path) -> Dict[str, Path]:
    slugs: Dict[str, Path] = {}
    for path in sorted(features_dir.glob("*.md")):
        slugs[slug_from_path(path)] = path
    return slugs


def slug_path_prefixes(slug: str, feature_text: str) -> List[str]:
    prefixes: Set[str] = set()
    for root in default_search_roots(slug):
        prefixes.add(root.rstrip("/"))
    for glob in extract_code_location_globs(feature_text):
        g = glob.strip().strip("`")
        if g.endswith("/"):
            prefixes.add(g.rstrip("/"))
        else:
            p = Path(g)
            if p.suffix:
                prefixes.add(str(p.parent).replace("\\", "/"))
            else:
                prefixes.add(g.rstrip("/"))
    return sorted(prefixes)


def prefix_to_slug(prefix: str, known_slugs: Set[str]) -> Optional[str]:
    normalized = prefix.replace("\\", "/").strip("/")
    for slug in known_slugs:
        if normalized == f"lib/services/{slug}" or normalized.endswith(f"/{slug}"):
            return slug
        for root in default_search_roots(slug):
            if normalized == root.rstrip("/"):
                return slug
    parts = normalized.split("/")
    if len(parts) >= 3 and parts[0] == "lib" and parts[1] == "services":
        candidate = parts[2]
        if candidate in known_slugs:
            return candidate
    return None


def collect_source_files(project_root: Path, prefixes: List[str], max_files: int) -> List[Path]:
    files: List[Path] = []
    for prefix in prefixes:
        base = project_root / prefix
        if base.is_file() and base.suffix in CODE_EXTENSIONS:
            files.append(base)
            continue
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if path.suffix in CODE_EXTENSIONS and path.is_file():
                files.append(path)
                if len(files) >= max_files:
                    return files
    return files


def infer_from_imports(
    project_root: Path,
    primary_slug: str,
    feature_text: str,
    known_slugs: Set[str],
    max_files: int,
) -> Tuple[List[PeerSuggestion], List[PeerSuggestion]]:
    depends: List[PeerSuggestion] = []
    shares: List[PeerSuggestion] = []
    prefixes = slug_path_prefixes(primary_slug, feature_text)
    files = collect_source_files(project_root, prefixes, max_files)
    seen_dep: Set[str] = set()
    seen_share: Set[str] = set()

    shared_lib_markers = (
        "lib/utils/wallet-provider",
        "lib/paystack",
        "lib/jobs/",
        "lib/utils/",
        "lib/models/",
    )

    for file_path in files:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in IMPORT_FROM_RE.finditer(content):
            imp = match.group(1)
            peer = prefix_to_slug(imp, known_slugs)
            if peer and peer != primary_slug and peer not in seen_dep:
                if imp.startswith("lib/services/") or imp.startswith("app/api/"):
                    seen_dep.add(peer)
                    depends.append(
                        PeerSuggestion(
                            slug=peer,
                            source=f"import @{imp} in {file_path.relative_to(project_root)}",
                            confidence="OBSERVED",
                            relation="depends_on",
                        )
                    )
            elif any(imp.startswith(m.rstrip("/")) or imp == m.rstrip("/") for m in shared_lib_markers):
                for slug in known_slugs:
                    if slug == primary_slug or slug in seen_share:
                        continue
                    if slug in ("payment-provider-integration", "background-jobs", "wallet-and-funding"):
                        if slug not in seen_share and imp.startswith(("lib/utils/", "lib/jobs/", "lib/paystack")):
                            seen_share.add(slug)
                            shares.append(
                                PeerSuggestion(
                                    slug=slug,
                                    source=f"shared import @{imp}",
                                    confidence="OBSERVED",
                                    relation="shares",
                                )
                            )

    return depends, shares


def infer_from_product_map(
    product_text: str, primary_slug: str, known_slugs: Set[str]
) -> Tuple[List[PeerSuggestion], List[PeerSuggestion]]:
    depends: List[PeerSuggestion] = []
    feeds: List[PeerSuggestion] = []
    match = PRODUCT_MAP_RE.search(product_text)
    if not match:
        return depends, feeds
    block = match.group(1)
    for line in block.splitlines():
        line = line.strip()
        if not line or line.upper().startswith("KNOWN NON-DEPENDENCY"):
            continue
        tokens = [t for t in SLUG_IN_TEXT_RE.findall(line) if t in known_slugs]
        if primary_slug not in tokens:
            continue
        if "→" in line or "->" in line:
            parts = re.split(r"→|->", line)
            left = SLUG_IN_TEXT_RE.findall(parts[0]) if parts else []
            right = SLUG_IN_TEXT_RE.findall(parts[1]) if len(parts) > 1 else []
            if primary_slug in left:
                for t in right:
                    if t != primary_slug:
                        feeds.append(
                            PeerSuggestion(
                                slug=t,
                                source="PRODUCT.md relationship map",
                                confidence="ASSUMED",
                                relation="feeds_into",
                            )
                        )
            if primary_slug in right:
                for t in left:
                    if t != primary_slug:
                        depends.append(
                            PeerSuggestion(
                                slug=t,
                                source="PRODUCT.md relationship map",
                                confidence="ASSUMED",
                                relation="depends_on",
                            )
                        )
        if "←" in line or "<-" in line:
            parts = re.split(r"←|<-", line)
            right = SLUG_IN_TEXT_RE.findall(parts[0]) if parts else []
            left = SLUG_IN_TEXT_RE.findall(parts[1]) if len(parts) > 1 else []
            if primary_slug in right:
                for t in left:
                    if t != primary_slug:
                        depends.append(
                            PeerSuggestion(
                                slug=t,
                                source="PRODUCT.md relationship map",
                                confidence="ASSUMED",
                                relation="depends_on",
                            )
                        )
    return depends, feeds


def infer_from_contracts(
    product_text: str, primary_slug: str, known_slugs: Set[str]
) -> Tuple[List[PeerSuggestion], List[PeerSuggestion]]:
    depends: List[PeerSuggestion] = []
    feeds: List[PeerSuggestion] = []
    for match in CONTRACT_BLOCK_RE.finditer(product_text):
        body = match.group(2)
        producer_m = re.search(r"Producer:\s*([^\n]+)", body, re.IGNORECASE)
        consumer_m = re.search(r"Consumer:\s*([^\n]+)", body, re.IGNORECASE)
        if not producer_m:
            continue
        producer_tokens = [
            t for t in SLUG_IN_TEXT_RE.findall(producer_m.group(1)) if t in known_slugs
        ]
        consumer_tokens = (
            [t for t in SLUG_IN_TEXT_RE.findall(consumer_m.group(1)) if t in known_slugs]
            if consumer_m
            else []
        )
        for prod in producer_tokens:
            if prod == primary_slug:
                for cons in consumer_tokens:
                    if cons != primary_slug:
                        feeds.append(
                            PeerSuggestion(
                                slug=cons,
                                source=match.group(1),
                                confidence="ASSUMED",
                                relation="feeds_into",
                            )
                        )
            if primary_slug in consumer_tokens and prod != primary_slug:
                depends.append(
                    PeerSuggestion(
                        slug=prod,
                        source=match.group(1),
                        confidence="ASSUMED",
                        relation="depends_on",
                    )
                )
    return depends, feeds


def merge_suggestions(items: List[PeerSuggestion]) -> List[PeerSuggestion]:
    by_slug: Dict[str, PeerSuggestion] = {}
    for item in items:
        existing = by_slug.get(item.slug)
        if not existing:
            by_slug[item.slug] = item
            continue
        if existing.confidence == "ASSUMED" and item.confidence == "OBSERVED":
            by_slug[item.slug] = item
    return list(by_slug.values())


def compute_gaps(
    documented: Dict[str, List[str]], suggested: Dict[str, List[PeerSuggestion]]
) -> Dict[str, List[str]]:
    gaps: Dict[str, List[str]] = {}
    key_map = {
        "depends_on": "depends_on",
        "feeds_into": "feeds_into",
        "shares": "shares",
    }
    for rel, doc_key in key_map.items():
        doc_set = set(documented.get(doc_key, []))
        missing = sorted(
            s.slug for s in suggested.get(rel, []) if s.slug not in doc_set
        )
        if missing:
            gaps[doc_key] = missing
    return gaps


def reciprocal_depends_missing(
    all_related: Dict[str, Dict[str, List[str]]], slug: str
) -> List[str]:
    """If upstream feeds into slug, slug should list upstream in Depends On or Shares."""
    rel_self = all_related.get(slug, {})
    upstream_ok = set(rel_self.get("depends_on", [])) | set(rel_self.get("shares", []))
    missing: List[str] = []
    for upstream, rel in all_related.items():
        if upstream == slug:
            continue
        if slug in rel.get("feeds_into", []) and upstream not in upstream_ok:
            missing.append(upstream)
    return sorted(set(missing))


def load_all_related(slugs: Dict[str, Path]) -> Dict[str, Dict[str, List[str]]]:
    out: Dict[str, Dict[str, List[str]]] = {}
    for slug, path in slugs.items():
        _, text = read_frontmatter(path)
        out[slug] = parse_related_features(text)
    return out


def infer_feature(
    project_root: Path,
    slug: str,
    feature_path: Path,
    product_text: str,
    known_slugs: Set[str],
    max_files: int,
) -> InferResult:
    _, text = read_frontmatter(feature_path)
    documented = parse_related_features(text)
    dep_i, share_i = infer_from_imports(
        project_root, slug, text, known_slugs, max_files
    )
    dep_p, feed_p = infer_from_product_map(product_text, slug, known_slugs)
    dep_c, feed_c = infer_from_contracts(product_text, slug, known_slugs)

    suggested = {
        "depends_on": merge_suggestions(dep_i + dep_p + dep_c),
        "feeds_into": merge_suggestions(feed_p + feed_c),
        "shares": merge_suggestions(share_i),
    }
    gaps = compute_gaps(documented, suggested)
    return InferResult(slug=slug, documented=documented, suggested=suggested, gaps=gaps)


def format_list(slugs: List[str]) -> str:
    if not slugs:
        return "None recorded."
    return ", ".join(sorted(set(slugs)))


def merge_field(existing: str, add: List[str]) -> str:
    current = split_peer_list(existing) if existing else []
    merged = sorted(set(current + add))
    return format_list(merged)


def apply_suggestions(feature_path: Path, gaps: Dict[str, List[str]]) -> bool:
    if not gaps:
        return False
    text = feature_path.read_text(encoding="utf-8")
    match = RELATED_BLOCK_RE.search(text)
    if not match:
        return False
    block = match.group(1)
    updates = {
        "Depends On": gaps.get("depends_on", []),
        "Feeds Into": gaps.get("feeds_into", []),
        "Shares Infrastructure With": gaps.get("shares", []),
    }
    new_block = block
    changed = False
    for field, slugs in updates.items():
        if not slugs:
            continue
        pattern = rf"(\-\s+\*\*{re.escape(field)}:\*\*\s*)(.+)(\s*)$"
        m = re.search(pattern, new_block, re.MULTILINE)
        if not m:
            continue
        merged = merge_field(m.group(2), slugs)
        if merged != m.group(2).strip():
            new_block = (
                new_block[: m.start(2)] + merged + new_block[m.end(2) :]
            )
            changed = True
    if not changed:
        return False
    if "Peer inference (auto)" not in new_block:
        new_block = new_block.rstrip() + "\n\n<!-- Peer inference (auto): merged from infer_peers.py -->\n"
    new_text = text[: match.start(1)] + new_block + text[match.end(1) :]
    # bump memory-revision if present
    rev_m = re.search(r"^(memory-revision:\s*)(\d+)\s*$", new_text, re.MULTILINE)
    if rev_m:
        new_rev = int(rev_m.group(2)) + 1
        new_text = (
            new_text[: rev_m.start(2)]
            + str(new_rev)
            + new_text[rev_m.end(2) :]
        )
    feature_path.write_text(new_text, encoding="utf-8")
    return True


def result_to_dict(result: InferResult) -> dict:
    return {
        "slug": result.slug,
        "documented": result.documented,
        "suggested": {
            k: [s.__dict__ for s in v] for k, v in result.suggested.items()
        },
        "gaps": result.gaps,
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Infer Feature Guardian peer relationships")
    parser.add_argument("project", nargs="?", default=".", help="Project root")
    parser.add_argument("--feature", "-f", help="Feature slug")
    parser.add_argument("--all", action="store_true", help="Infer all features")
    parser.add_argument("--limit", type=int, default=80, help="Max source files per feature")
    parser.add_argument("--apply", action="store_true", help="Merge gaps into RELATED FEATURES")
    parser.add_argument("--json", action="store_true", dest="as_json", help="JSON output")
    parser.add_argument(
        "--version", action="version", version=f"feature-guardian-infer-peers {SKILL_VERSION}"
    )
    args = parser.parse_args(argv)

    project_root = Path(args.project).resolve()
    memory = project_root / ".feature-guardian"
    features_dir = memory / "features"
    product_path = memory / "PRODUCT.md"
    if not features_dir.is_dir() or not product_path.is_file():
        print("error: missing .feature-guardian/PRODUCT.md or features/", file=sys.stderr)
        return 1

    product_text = product_path.read_text(encoding="utf-8")
    slugs = load_all_slugs(features_dir)
    known = set(slugs.keys())

    targets: List[str] = []
    if args.feature:
        if args.feature not in slugs:
            print(f"error: unknown feature slug {args.feature}", file=sys.stderr)
            return 1
        targets = [args.feature]
    elif args.all:
        targets = sorted(slugs.keys())
    else:
        parser.error("Specify --feature SLUG or --all")

    all_related = load_all_related(slugs)

    results: List[InferResult] = []
    applied = 0
    for slug in targets:
        result = infer_feature(
            project_root, slug, slugs[slug], product_text, known, args.limit
        )
        rec = reciprocal_depends_missing(all_related, slug)
        if rec:
            merged_dep = sorted(set(result.gaps.get("depends_on", []) + rec))
            result.gaps["depends_on"] = merged_dep
        results.append(result)
        if args.apply and result.gaps:
            if apply_suggestions(slugs[slug], result.gaps):
                applied += 1
                _, text = read_frontmatter(slugs[slug])
                all_related[slug] = parse_related_features(text)

    if args.as_json:
        print(json.dumps([result_to_dict(r) for r in results], indent=2))
    else:
        for result in results:
            print(f"## {result.slug}")
            if result.gaps:
                for key, slugs_missing in result.gaps.items():
                    print(f"  gaps.{key}: {', '.join(slugs_missing)}")
            else:
                print("  gaps: none (documented matches inference)")
            for rel, items in result.suggested.items():
                if not items:
                    continue
                print(f"  suggested.{rel}:")
                for s in items[:12]:
                    print(f"    - {s.slug} ({s.confidence}, {s.source[:60]})")
            print()
        if args.apply:
            print(f"Applied RELATED FEATURES updates: {applied} feature(s)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
