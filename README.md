# Feature Guardian

**Persistent engineering memory and product integrity for AI coding agents.**

Feature Guardian tracks every product feature (including small ones), preserves complete engineering history, verifies changes with evidence, detects regressions and blast radius, and protects completed features from silent breakage across AI sessions.

> Nothing is forgotten, nothing is assumed to work, and nothing important changes without understanding what it could affect.

**Version:** 0.1.0 · **Schema:** 0.1 · **License:** MIT

---

## Why Feature Guardian exists

AI coding agents excel at the current task but often forget prior failures, rejected approaches, test coverage, dependencies, and whether "done" was ever verified. Feature Guardian creates durable Markdown memory that **actively influences** future implementation, testing, risk analysis, and completion decisions.

## Five-minute install (Cursor)

### 1. Copy the skill

```bash
cp -R feature-guardian /path/to/your-project/.cursor/skills/feature-guardian
```

Alternative portable path: `.agents/skills/feature-guardian/`

### 2. Install the always-on rule

```bash
cp feature-guardian/adapters/cursor/feature-guardian.mdc \
   /path/to/your-project/.cursor/rules/feature-guardian.mdc
```

### 3. Bootstrap memory in your project

```bash
cd /path/to/your-project
python .cursor/skills/feature-guardian/scripts/bootstrap_memory.py . --name "My Product"
```

### 4. Work normally

Ask Cursor to build features as usual. Feature Guardian runs via the **skill + always-on rule** combination.

See [adapters/cursor/INSTALL.md](adapters/cursor/INSTALL.md) for details.

## How automatic tracking works

| Component | Purpose |
|---|---|
| `SKILL.md` | Full lifecycle, evidence rules, schemas (invoked automatically when relevant) |
| `.cursor/rules/feature-guardian.mdc` | `alwaysApply: true` reminder on product/engineering tasks |
| `.feature-guardian/` | Durable memory in your project repo |

Feature Guardian does **not** run as a background service between sessions. Continuity comes from memory files updated during agent work.

## What `.feature-guardian/` contains

```text
.feature-guardian/
├── PRODUCT.md          # Product intent, registry, relationships
└── features/
    └── <slug>.md       # One permanent file per feature
```

**Rule:** one feature = one Markdown file, forever. Even copy buttons and dark mode get a file.

## Example workflow

**You:** "Add a copy button beside the invoice number."

**Guardian (internally):**
1. Identifies or creates `copy-invoice-number` feature memory.
2. Loads `PRODUCT.md` and related features.
3. Implements with appropriate test depth.
4. Records evidence (not just "code written").
5. Updates registry and validates memory.

**You see:** a concise checkpoint report, not a memory dump.

## Example completed-feature review

When shared payment code changes:

1. Guardian marks dependent completed features `REVIEW_REQUIRED`.
2. Lists specific tests to rerun (`FG-TEST-...`).
3. After pass → restore `COMPLETED`; on fail → `REGRESSED` + `FG-REG-...`.

## Inspecting status

- **Product overview:** `.feature-guardian/PRODUCT.md`
- **Feature detail:** `.feature-guardian/features/<slug>.md`
- **Validate structure:** `python scripts/validate_memory.py .`

## Opt-out

| Request | Effect |
|---|---|
| "Stop tracking this feature" | `Monitoring: EXCLUDED`; memory kept |
| "Delete Feature Guardian history for X" | Explicit deletion after registry update |

## Uninstall safely

1. Remove `.cursor/rules/feature-guardian.mdc`
2. Remove `.cursor/skills/feature-guardian/`
3. Keep or delete `.feature-guardian/` as you prefer

## Privacy and security

- Memory lives in **your repository** (plain Markdown).
- **Never store secrets** in memory (record config names only).
- No telemetry, hosted backend, or cloud sync in v0.1.

## Current limitations (v0.1)

- No dashboard, database, MCP server, or PR bot.
- Validator checks structure and references, not runtime behavior.
- Behavior scenarios are documented; full automated skill-behavior tests are manual/future.
- Automatic invocation depends on Cursor skill + rule setup.

## Package layout

```text
feature-guardian/
├── SKILL.md
├── README.md
├── references/          # Deep protocol docs
├── assets/              # Templates
├── scripts/             # bootstrap + validate
├── examples/            # Sample memory files
├── adapters/cursor/     # always-on rule + install guide
└── tests/               # Validator unit tests
```

## Version and schema compatibility

- Skill version: `0.1.0` (in `SKILL.md` metadata)
- Memory schema: `0.1` (`fg-schema` in frontmatter)
- Newer skill versions should migrate older memory in place (see `references/DATA_MODEL.md`)

## Roadmap

### v0.2 — Intelligence
- Richer dependency inference
- Deterministic stale-evidence detection
- Stronger schema validation
- Release review workflow

### v0.3 — Portability
- Claude Code, Codex, Copilot adapters
- Generic AGENTS.md adapter

### v0.4 — Tooling
- Optional lightweight CLI
- Graph/status queries, feature audit

### v1.0 — Stable release
- Hardened schema, migration guarantees, installation automation

## Contributing

1. Read `SKILL.md` and `references/`.
2. Keep one-feature-one-file and evidence hierarchy intact.
3. Run `python -m unittest discover -s tests -p 'test_*.py'`.
4. Run `validate_memory.py` on fixtures.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
