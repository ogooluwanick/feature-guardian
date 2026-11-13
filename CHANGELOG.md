# Changelog

All notable changes to Feature Guardian are documented here.

## [0.1.6] - 2026-11-13

### Changed

- Parity is **index-first**: lean schema 2 cards (provider + `check_here` + hashes) instead of full audits every turn.
- Hash mismatch demotes OK → **STALE**; STALE/FAIL **blocks done** for touched contracts (`blocks_done`).
- Agents must **report drifts to the user** and **ask** when fixes are ambiguous or need business decisions.
- `check_parity.py` supports schema 2 cards + schema 1 units; adds `--report` and drift list.
- Preflight, operating protocol, skill, Cursor rule, and feature template updated for forced lean parity.

## [0.1.5] - 2026-11-13

### Added

- Automatic cross-surface parity for shared data, logic, schemas and props, with provider/consumer/variant tracking, intentional differences and persistent evidence.
- `references/PARITY.md`, feature-template manifest and reusable `scripts/check_parity.py`; unknown/stale/empty coverage cannot certify parity.
- Backward-compatible memory validation of manifests and VERIFIED claims; semantic regression controls for source drift, missing evidence and intended differences.

### Changed

- Preflight, lifecycle and Cursor adapters include parity; existing feature records migrate lazily without changing historical completion states.

## [0.1.4] - 2026-11-04

### Added

- `scripts/fg_memory_lib.py` — shared RELATED FEATURES parsers.
- `scripts/infer_peers.py` — suggest/apply peer edges from imports, PRODUCT map, and contracts; reciprocal **Depends On** backfill from documented **Feeds Into**.
- Validator **FG036** — reciprocal Depends On / Feeds Into consistency.

### Changed

- End-of-work protocol: run `infer_peers.py` before `validate_memory.py`.
- Skill 0.1.4; FEATURE_PEER_AWARENESS documents automatic discovery.

## [0.1.3] - 2026-11-04

### Added

- [FEATURE_PEER_AWARENESS.md](references/FEATURE_PEER_AWARENESS.md) — product graph + per-feature RELATED FEATURES; mandatory preflight peer pass; standalone explicit non-dependencies.
- Validator warning **FG035** when active features lack peer links in RELATED FEATURES.

### Changed

- Preflight steps 3–8 include peer graph load and peer FAST CONTEXT skim.
- Operating protocol, PRODUCT schema, feature template, Cursor rule, and prompt hook reference peer awareness.

## [0.1.2] - 2026-11-04

### Added

- First-class **feature todos** (`FG-TODO-...`) in **ACTIVE WORK**; lifecycle in [FEATURE_TODOS.md](references/FEATURE_TODOS.md) (including promote todo → new feature file).
- Validator checks for todo status, DONE evidence, duplicate ids, multiple IN_PROGRESS (`validate_memory.py` FG031–FG034).
- Preflight and operating protocol require reading **ACTIVE WORK** and reporting open todos.

### Changed

- `SKILL.md`, Cursor adapter rule, prompt hook — track and complete `FG-TODO` during feature work; mirror in Cursor TodoWrite when useful.

## [0.1.1] - 2026-11-03

### Added

- `scripts/install_cursor.sh` — symlink skill + always-on rule from central package (auto-updates on all projects).
- [PREFLIGHT_PROTOCOL.md](references/PREFLIGHT_PROTOCOL.md) — mandatory ordering before product code edits; gates A–D.
- [COMPANION_SKILLS.md](references/COMPANION_SKILLS.md) — integration with **unlazy**, **council** (counsel), **impeccable**, and **emil-design-eng**.
- [assets/GATES_FEATURE_TEMPLATE.md](assets/GATES_FEATURE_TEMPLATE.md) — starter `GATES.md` for feature work (preflight, tests, validate, completion check).

### Changed

- `SKILL.md` and [OPERATING_PROTOCOL.md](references/OPERATING_PROTOCOL.md) — preflight-first lifecycle; companion skill hooks at start/end of work.
- Cursor adapter rule and `assets/CURSOR_RULE_TEMPLATE.mdc` — deterministic preflight + unlazy + council + taste pointers (still concise).

### Notes

- v0.1.0 remains tagged `feature-guardian-v0.1.0` for dogfood baseline; 0.1.1 addresses activation/completion coupling found in blind evaluation.

## [0.1.0] - 2026-09-04

### Added

- Initial production-quality Agent Skill (`SKILL.md`) with schema version `0.1`
- Ten reference documents under `references/`
- Product and feature memory templates (`assets/`)
- Cursor always-on adapter rule (`adapters/cursor/feature-guardian.mdc`)
- Cursor installation guide (`adapters/cursor/INSTALL.md`)
- `bootstrap_memory.py` — safe `.feature-guardian/` initialization
- `validate_memory.py` — structural memory validation (stdlib only)
- Example memory files: simple, mature, regression-heavy, product
- Validator unit tests (`tests/test_validate_memory.py`)
- Behavior scenario acceptance document (`tests/BEHAVIOR_SCENARIOS.md`)
- Beginner-first README with install, workflow, and limitations

### Principles encoded

- One feature = one permanent Markdown memory file
- Product memory separate in `PRODUCT.md`
- Evidence hierarchy; no evidence, no claim
- Append-only engineering history
- Completed-feature `REVIEW_REQUIRED` protocol
- Blast-radius and direction-conflict handling
- Portable Agent Skill design (not Cursor-locked)
