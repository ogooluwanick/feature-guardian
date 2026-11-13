#!/usr/bin/env bash
# Copy Feature Guardian Cursor hooks into ~/.cursor/hooks/ (same pattern as unlazy).
# Does not edit hooks.json automatically — prints the JSON block to add.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FG_PACKAGE="$(cd "$SCRIPT_DIR/.." && pwd)"
HOOKS_SRC="$FG_PACKAGE/adapters/cursor/hooks"
USER_HOOKS="${CURSOR_HOOKS_DIR:-$HOME/.cursor/hooks}"

mkdir -p "$USER_HOOKS"

for f in before-submit-prompt-feature-guardian.js session-start-feature-guardian.js; do
  cp "$HOOKS_SRC/$f" "$USER_HOOKS/$f"
  chmod +x "$USER_HOOKS/$f"
  echo "installed $USER_HOOKS/$f"
done

cat <<'EOF'

Add to ~/.cursor/hooks.json (if not already present):

sessionStart — after session-start-unlazy:
{
  "command": "node .cursor/hooks/session-start-feature-guardian.js",
  "event": "sessionStart",
  "timeout": 5,
  "failClosed": false,
  "description": "Feature Guardian reminder when workspace has .feature-guardian/"
}

beforeSubmitPrompt — after before-submit-prompt-unlazy:
{
  "command": "node .cursor/hooks/before-submit-prompt-feature-guardian.js",
  "event": "beforeSubmitPrompt",
  "timeout": 5,
  "failClosed": false,
  "description": "Inject FG preflight when workspace has .feature-guardian/"
}

Reload Cursor after editing hooks.json.

EOF
