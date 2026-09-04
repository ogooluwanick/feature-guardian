# Changelog

All notable changes to Feature Guardian are documented here.

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
