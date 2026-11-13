#!/usr/bin/env python3
"""Feature Guardian memory bootstrap (v0.1.0).

Creates .feature-guardian/ safely from templates without overwriting existing memory.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_VERSION = "0.1.5"
FG_SCHEMA_VERSION = "0.1"


def package_root() -> Path:
    return Path(__file__).resolve().parent.parent


def asset_path(name: str) -> Path:
    path = package_root() / "assets" / name
    if not path.is_file():
        raise FileNotFoundError(f"Missing asset template: {path}")
    return path


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def render_product_template(template_text: str, project_name: str) -> str:
    return (
        template_text.replace("{{PROJECT_NAME}}", project_name)
        .replace("{{CREATED_AT}}", now_iso())
        .replace("{{FG_SCHEMA}}", FG_SCHEMA_VERSION)
    )


def bootstrap(project_root: Path, project_name: str, force: bool = False) -> int:
    memory_root = project_root / ".feature-guardian"
    product_path = memory_root / "PRODUCT.md"
    features_dir = memory_root / "features"

    if memory_root.exists() and not force:
        print(f"Memory already exists at {memory_root}")
        print("Bootstrap skipped. Use --force only if you intend to overwrite PRODUCT.md.")
        if product_path.is_file():
            print("Existing PRODUCT.md preserved.")
        if not features_dir.is_dir():
            features_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created missing features directory: {features_dir}")
        return 0

    memory_root.mkdir(parents=True, exist_ok=True)
    features_dir.mkdir(parents=True, exist_ok=True)

    if product_path.exists() and not force:
        print(f"PRODUCT.md already exists: {product_path}")
    else:
        if product_path.exists() and force:
            print("WARNING: --force will overwrite PRODUCT.md")
        template = asset_path("PRODUCT_TEMPLATE.md").read_text(encoding="utf-8")
        product_path.write_text(
            render_product_template(template, project_name), encoding="utf-8"
        )
        print(f"Created {product_path}")

    print("")
    print("Feature Guardian bootstrap complete.")
    print(f"  Project: {project_root}")
    print(f"  Memory:  {memory_root}")
    print(f"  Version: {SKILL_VERSION} (schema {FG_SCHEMA_VERSION})")
    print("")
    print("Next steps:")
    print("  1. Install the feature-guardian skill and Cursor adapter rule.")
    print("  2. Let the agent inspect the repo and populate feature memory.")
    print("  3. Run: python scripts/validate_memory.py <project-root>")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bootstrap Feature Guardian memory")
    parser.add_argument(
        "project",
        nargs="?",
        default=".",
        help="Project root (default: current directory)",
    )
    parser.add_argument(
        "--name",
        default="",
        help="Product/project display name for PRODUCT.md",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite PRODUCT.md if it already exists (destructive)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"feature-guardian-bootstrap {SKILL_VERSION} (schema {FG_SCHEMA_VERSION})",
    )
    args = parser.parse_args(argv)
    project_root = Path(args.project).resolve()
    project_name = args.name or project_root.name
    try:
        return bootstrap(project_root, project_name, force=args.force)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
