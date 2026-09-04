# Feature Guardian — Cursor Installation

Install Feature Guardian into a Cursor project in two steps: **skill** + **always-on rule**.

## 1. Install the Agent Skill

Copy the entire `feature-guardian/` package into **one** of:

```text
<your-project>/.cursor/skills/feature-guardian/
```

or the portable Agent Skills location:

```text
<your-project>/.agents/skills/feature-guardian/
```

The directory must contain `SKILL.md`, `references/`, `assets/`, `scripts/`, and `examples/` at the skill root.

### Example (copy from this repo)

```bash
# From the feature-guardian package directory
cp -R feature-guardian /path/to/your-project/.cursor/skills/feature-guardian
```

Or symlink if you maintain a central copy:

```bash
ln -s /path/to/feature-guardian /path/to/your-project/.cursor/skills/feature-guardian
```

## 2. Install the always-on Cursor rule

Copy:

```text
feature-guardian/adapters/cursor/feature-guardian.mdc
```

to:

```text
<your-project>/.cursor/rules/feature-guardian.mdc
```

The rule uses `alwaysApply: true` so Feature Guardian is considered during ordinary coding work, not only when you type `/feature-guardian`.

## 3. Bootstrap project memory

From your project root:

```bash
python /path/to/feature-guardian/scripts/bootstrap_memory.py . --name "Your Product Name"
```

Then let the agent inspect the repository to populate `PRODUCT.md` and feature files.

## 4. Validate memory (after updates)

```bash
python /path/to/feature-guardian/scripts/validate_memory.py /path/to/your-project
```

## Skills vs rules

| Layer | Role |
|---|---|
| **Agent Skill** (`SKILL.md` + references) | Full operating protocol, schemas, evidence rules |
| **Cursor rule** (`.mdc`) | Lightweight always-on reminder to use the skill |

The rule must not duplicate the entire skill; it points agents to the installed skill.

## Uninstall

1. Delete `.cursor/rules/feature-guardian.mdc` (or `.agents` equivalent).
2. Delete `.cursor/skills/feature-guardian/` (or `.agents/skills/feature-guardian/`).
3. Optionally keep or remove `.feature-guardian/` project memory.

## Verify installation

- `SKILL.md` is discoverable by Cursor skills.
- Rule appears in project rules with `alwaysApply: true`.
- `bootstrap_memory.py` creates `.feature-guardian/` without overwriting existing memory.
- `validate_memory.py` exits 0 on valid memory.
