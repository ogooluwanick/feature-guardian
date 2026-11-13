#!/usr/bin/env bash
# Link Feature Guardian skill + always-on Cursor rule from the central package.
# Re-run after moving a project or when the adapter rule changes.
#
# Usage:
#   ./scripts/install_cursor.sh /path/to/project
#   FEATURE_GUARDIAN_HOME=/path/to/feature-guardian ./scripts/install_cursor.sh .
#
set -euo pipefail

PROJECT_ROOT="${1:?Usage: install_cursor.sh /path/to/project}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FG_PACKAGE="${FEATURE_GUARDIAN_HOME:-$(cd "$SCRIPT_DIR/.." && pwd)}"
ADAPTER="$FG_PACKAGE/adapters/cursor/feature-guardian.mdc"

if [[ ! -f "$FG_PACKAGE/SKILL.md" ]]; then
  echo "error: Feature Guardian package not found at $FG_PACKAGE (missing SKILL.md)" >&2
  exit 1
fi
if [[ ! -f "$ADAPTER" ]]; then
  echo "error: Cursor adapter missing at $ADAPTER" >&2
  exit 1
fi

PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd)"
mkdir -p "$PROJECT_ROOT/.cursor/skills" "$PROJECT_ROOT/.cursor/rules"

ln -sfn "$FG_PACKAGE" "$PROJECT_ROOT/.cursor/skills/feature-guardian"
ln -sfn "$ADAPTER" "$PROJECT_ROOT/.cursor/rules/feature-guardian.mdc"

echo "Feature Guardian Cursor install (symlinked, auto-updates with package):"
echo "  skill  -> $FG_PACKAGE"
echo "  rule   -> $ADAPTER"
echo "  project: $PROJECT_ROOT"
echo ""
echo "Optional: bootstrap memory with:"
echo "  python3 \"$FG_PACKAGE/scripts/bootstrap_memory.py\" \"$PROJECT_ROOT\" --name \"Your Product\""
