# Changelog

All notable changes to Feature Guardian are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project is in active development at 0.1.x. Unreleased notes describe `main` since 0.1.0.

## [Unreleased]

### Added

- README status callout and badges for active development (v0.x; schemas and script behavior may change), with pointers to this changelog and the roadmap
- README usage guide: install for Cursor and `.agents/skills/`, script flags and exit codes taken from the scripts, memory layout and statuses, templates and examples, opt-out, uninstall, troubleshooting, and limitations
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1), and `SECURITY.md` (GitHub private vulnerability reporting)
- GitHub issue forms for bugs and feature requests, a pull request template, and a CI workflow that runs the unit tests and `validate_memory.py` on `tests/fixtures/valid/`

### Changed

- `adapters/cursor/INSTALL.md` aligned with the README install, bootstrap, validate, and uninstall steps
- `references/BEGINNER_EXPERIENCE.md` uninstall and validator paths aligned with those two locations
- `SKILL.md` points humans at the README and the Cursor install notes

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
