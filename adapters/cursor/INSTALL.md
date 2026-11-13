# Feature Guardian — Cursor installation

Install two pieces into a Cursor project: the **skill** and the **always-on rule**. Then bootstrap `.feature-guardian/` in that project.

This file is the Cursor path. The full guide (script flags, memory statuses, templates, opt-out, troubleshooting) is the repository [README](../../README.md).

> **Active development.** Version 0.1.0, schema 0.1. Schemas and script behavior may change. See the README status note, [changelog](../../CHANGELOG.md), and [roadmap](../../README.md#roadmap).

## 1. Get the package

```bash
git clone https://github.com/ogooluwanick/feature-guardian.git
```

The `cp` commands below run from the parent of this clone. Python 3.9+ is required for the scripts (`python3`). They use the standard library only.

## 2. Install the Agent Skill

Copy the whole `feature-guardian/` directory into **one** of:

```text
<your-project>/.cursor/skills/feature-guardian/
```

```text
<your-project>/.agents/skills/feature-guardian/
```

`.cursor/skills/` is Cursor's project skill directory. `.agents/skills/` is the portable Agent Skills directory. The installed folder must contain `SKILL.md`, `references/`, `assets/`, `scripts/`, and `examples/` at its root. `bootstrap_memory.py` reads `assets/PRODUCT_TEMPLATE.md` next to `scripts/`.

```bash
mkdir -p /path/to/your-project/.cursor/skills
cp -R feature-guardian /path/to/your-project/.cursor/skills/feature-guardian
```

Portable path:

```bash
mkdir -p /path/to/your-project/.agents/skills
cp -R feature-guardian /path/to/your-project/.agents/skills/feature-guardian
```

Or symlink a clone you update with `git pull`. Run this from inside the clone:

```bash
ln -s "$(pwd)" /path/to/your-project/.cursor/skills/feature-guardian
```

Use `.agents/skills/feature-guardian` as the link path for the portable location.

## 3. Install the always-on Cursor rule

Copy [`feature-guardian.mdc`](feature-guardian.mdc) in this directory to the project:

```bash
cp feature-guardian/adapters/cursor/feature-guardian.mdc \
   /path/to/your-project/.cursor/rules/feature-guardian.mdc
```

The rule sets `alwaysApply: true`, so Cursor considers Feature Guardian during ordinary work. It is a reminder. `SKILL.md` is the operating guide. The rule does not duplicate the skill.

The rule file is only for `.cursor/rules/`. Installing the skill under `.agents/skills/` does not add a second rule. Cursor still needs `.cursor/rules/feature-guardian.mdc`.

[`assets/CURSOR_RULE_TEMPLATE.mdc`](../../assets/CURSOR_RULE_TEMPLATE.mdc) is the rule template with skill paths written out. Install the adapter file above.

## 4. Bootstrap project memory

From the project root:

```bash
cd /path/to/your-project
python3 .cursor/skills/feature-guardian/scripts/bootstrap_memory.py . --name "Your Product Name"
```

If the skill is under `.agents/skills/`, call `.agents/skills/feature-guardian/scripts/bootstrap_memory.py` instead.

| Argument | Meaning |
|---|---|
| `project` | Project root. Default `.` |
| `--name` | Name stored in `PRODUCT.md`. Default: the project directory's name. |
| `--force` | Overwrite an existing `PRODUCT.md`. Does not delete files in `features/`. |
| `--version` | Print `feature-guardian-bootstrap 0.1.0 (schema 0.1)`. |

When `.feature-guardian/` already exists, the script keeps `PRODUCT.md`, creates a missing `features/` directory, and exits 0. Exit 2 means `assets/PRODUCT_TEMPLATE.md` was not next to the script. A mistyped project path is created, because bootstrap makes missing parent directories. Read the `Project:` line it prints.

Bootstrap writes `PRODUCT.md` and `features/`. It does not create feature files. The agent fills those from `assets/FEATURE_TEMPLATE.md` after it inspects the repository.

## 5. Validate memory

After memory changes:

```bash
python3 /path/to/feature-guardian/scripts/validate_memory.py /path/to/your-project
```

Pass the project root (the directory that contains `.feature-guardian/`). Exit 0 means no errors. Warnings still exit 0. Exit 1 means errors. The script does not modify memory. Codes and the rest of the flags are in the [README](../../README.md#scripts).

## Skills vs rules

| Layer | Role |
|---|---|
| **Agent Skill** (`SKILL.md` + `references/`) | Operating protocol, schemas, evidence rules |
| **Cursor rule** (`.mdc`) | Short always-on reminder to use the skill |

## Update

- Copied tree: copy the repository over the skill directory again.
- Symlink or a clone checked out inside the skill path: `git pull` in that clone.

Re-copy `feature-guardian.mdc` when that file changes. `.feature-guardian/` in the project stays as it is. Schema migration for memory older than the skill is specified for future schemas; v0.1 only reads schema `0.1`.

## Uninstall

1. Delete `.cursor/rules/feature-guardian.mdc`.
2. Delete `.cursor/skills/feature-guardian/` or `.agents/skills/feature-guardian/` (or remove the symlink).
3. Keep `.feature-guardian/` to retain the history. Delete it only when you want the memory gone.

## Verify installation

- `SKILL.md` is in the installed skill directory.
- `.cursor/rules/feature-guardian.mdc` contains `alwaysApply: true`.
- `bootstrap_memory.py` creates `.feature-guardian/` and exits 0. A second run without `--force` leaves `PRODUCT.md` in place and still exits 0.
- `validate_memory.py` exits 0 on that project.
