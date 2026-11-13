#!/usr/bin/env python3
"""Shared parsers for Feature Guardian memory scripts (stdlib only)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
RELATED_BLOCK_RE = re.compile(
    r"<!-- FG:RELATED_FEATURES:START -->(.*?)<!-- FG:RELATED_FEATURES:END -->",
    re.DOTALL,
)
RELATED_FIELD_RE = re.compile(
    r"^\-\s+\*\*(Depends On|Feeds Into|Shares Infrastructure With|Known Non-Dependencies):\*\*\s*(.+)\s*$",
    re.MULTILINE,
)
CODE_LOCATIONS_RE = re.compile(
    r"^\*\*Code locations:\*\*\s*(.+)$", re.MULTILINE | re.IGNORECASE
)
SLUG_TOKEN_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")


def parse_simple_yaml(text: str) -> Dict[str, str]:
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
            key, value = key.strip(), value.strip().strip('"').strip("'")
            current_key = key
            if value in ("", "null", "~"):
                continue
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


def slug_from_path(path: Path) -> str:
    return path.stem


def split_peer_list(value: str) -> List[str]:
    value = value.strip()
    if not value or value.lower() == "none recorded.":
        return []
    parts = re.split(r",|\s+\|\s+", value)
    out: List[str] = []
    for part in parts:
        token = part.strip().strip(".")
        if not token or token.lower() in ("none", "none recorded"):
            continue
        token = token.split("(")[0].strip()
        if SLUG_TOKEN_RE.fullmatch(token):
            out.append(token)
    return out


def parse_related_features(text: str) -> Dict[str, List[str]]:
    """Return depends_on, feeds_into, shares, non_dependencies slug lists."""
    result: Dict[str, List[str]] = {
        "depends_on": [],
        "feeds_into": [],
        "shares": [],
        "non_dependencies": [],
    }
    match = RELATED_BLOCK_RE.search(text)
    if not match:
        return result
    block = match.group(1)
    field_map = {
        "Depends On": "depends_on",
        "Feeds Into": "feeds_into",
        "Shares Infrastructure With": "shares",
        "Known Non-Dependencies": "non_dependencies",
    }
    for m in RELATED_FIELD_RE.finditer(block):
        key = field_map.get(m.group(1), "")
        if key:
            result[key] = split_peer_list(m.group(2))
    return result


def extract_code_location_globs(text: str) -> List[str]:
    globs: List[str] = []
    for m in CODE_LOCATIONS_RE.finditer(text):
        raw = m.group(1)
        for chunk in re.split(r"[,;]", raw):
            chunk = chunk.strip().strip("`").strip()
            if chunk:
                globs.append(chunk)
    return globs


def default_search_roots(slug: str) -> List[str]:
    """Repository-relative directory prefixes to scan for a feature slug."""
    roots = [
        f"lib/services/{slug}/",
        f"lib/{slug}/",
        f"app/api/{slug}/",
        f"app/api/{slug}s/",
        f"components/{slug}/",
        f"components/dashboard/{slug}/",
    ]
    if slug.endswith("s"):
        singular = slug[:-1]
        roots.append(f"lib/services/{singular}/")
    return roots
