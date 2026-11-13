# Feature Guardian — Cursor Installation

Install Feature Guardian into a Cursor project: **symlink the central package** so skill + rule updates apply automatically.

## Recommended: `install_cursor.sh`

From the Feature Guardian package:

```bash
chmod +x scripts/install_cursor.sh   # once
./scripts/install_cursor.sh /path/to/your-project
```

Or set a custom package location:

```bash
export FEATURE_GUARDIAN_HOME="/path/to/feature-guardian"
./scripts/install_cursor.sh /path/to/your-project
```

This creates:

| Path | Target |
|------|--------|
| `<project>/.cursor/skills/feature-guardian` | Symlink → central `feature-guardian/` package |
| `<project>/.cursor/rules/feature-guardian.mdc` | Symlink → `adapters/cursor/feature-guardian.mdc` |

**Re-run the script** after cloning a repo on a new machine or when you want to refresh rule links.

### Ex Workbench canonical package

```bash
FG="/Users/user/Documents/WORK DOCS/Ex_workbench/feature-guardian"
"$FG/scripts/install_cursor.sh" "/path/to/project"
```

Projects already using this pattern: Staff Pay web, Human OS, Glam Haven (symlink skill + rule).

## What auto-updates vs what stays in the repo

| Updates automatically (symlink) | Stays in your project repo |
|--------------------------------|----------------------------|
| `SKILL.md`, all `references/` (preflight, companion skills, unlazy integration) | `.feature-guardian/PRODUCT.md` |
| `scripts/validate_memory.py`, templates | `.feature-guardian/features/*.md` |
| Always-on Cursor rule (companion stack: unlazy, council, taste) | Your product memory only |

Do **not** `cp -R` the skill into the project unless you need a fork; copies drift from 0.1.1+ preflight and companion skills.

## Manual install (not recommended)

Copy-only installs require you to re-copy after every package upgrade.

```bash
cp -R feature-guardian /path/to/your-project/.cursor/skills/feature-guardian
cp feature-guardian/adapters/cursor/feature-guardian.mdc \
   /path/to/your-project/.cursor/rules/feature-guardian.mdc
```

Portable Agent Skills path: `.agents/skills/feature-guardian/` (adjust validate paths in your local rule if you copy instead of symlink).

## Bootstrap project memory

From your project root:

```bash
python3 .cursor/skills/feature-guardian/scripts/bootstrap_memory.py . --name "Your Product Name"
```

## Validate memory (after updates)

```bash
python3 .cursor/skills/feature-guardian/scripts/validate_memory.py .
```

## Companion skills (machine-wide, not bundled)

Feature Guardian 0.1.1+ expects these skills on the agent host:

- **unlazy** — completion gates (`GATES.md`)
- **council** — ambiguous product decisions
- **impeccable** + **emil-design-eng** — user-facing surfaces

See `references/COMPANION_SKILLS.md` in the package.

## Skills vs rules

| Layer | Role |
|---|---|
| **Agent Skill** (`SKILL.md` + references) | Full operating protocol, preflight, evidence rules |
| **Cursor rule** (`.mdc`, symlinked) | Always-on reminder: preflight before code, unlazy before done |

## Uninstall

1. Delete `.cursor/rules/feature-guardian.mdc`
2. Delete `.cursor/skills/feature-guardian` symlink
3. Optionally keep or remove `.feature-guardian/` project memory

## Verify installation

```bash
ls -la .cursor/skills/feature-guardian .cursor/rules/feature-guardian.mdc
test -f .cursor/skills/feature-guardian/references/COMPANION_SKILLS.md && echo OK
python3 .cursor/skills/feature-guardian/scripts/validate_memory.py .   # if memory exists
```

## Stronger enforcement (optional hooks)

Rules and skills are **soft** constraints; the model can still skip them. For repos with `.feature-guardian/`, install **prompt hooks** (same pattern as unlazy):

```bash
./scripts/install_cursor_hooks.sh
```

Then register the printed entries in `~/.cursor/hooks.json` (`sessionStart` + `beforeSubmitPrompt`). Hooks inject preflight + companion stack on **every prompt** when the workspace has product memory.

Pair with **unlazy Stop hook** (`node ~/.agents/skills/unlazy/scripts/install-hooks.mjs`) to block "done" while gates are open.
