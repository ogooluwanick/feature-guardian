# Contributing to Feature Guardian

Thanks for helping. Feature Guardian is an Agent Skill (Markdown instructions plus two standard-library scripts) at version 0.1.0, schema 0.1. It is in active development: behavior and schemas can change. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before participating.

The maintainer is [@ogooluwanick](https://github.com/ogooluwanick). Private contact: ogooluwanick@gmail.com.

## Development setup

Clone the repository and run the tests. There is no package to install, no virtualenv requirement, and no third-party Python dependency.

```bash
git clone https://github.com/ogooluwanick/feature-guardian.git
cd feature-guardian
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/validate_memory.py tests/fixtures/valid
```

Use `python3` (3.9 or newer). `python` is equivalent when that command is Python 3. The GitHub Actions workflow calls `python` after `actions/setup-python` installs 3.12. Both scripts are executable and use `#!/usr/bin/env python3`.

| Path | What it is |
|---|---|
| `SKILL.md` | Operating guide the agent loads |
| `references/` | Protocol, schemas, safety, evidence |
| `assets/` | Product template, feature template, Cursor rule template |
| `scripts/bootstrap_memory.py` | Creates `.feature-guardian/` without overwriting existing memory unless `--force` |
| `scripts/validate_memory.py` | Structural checks. Exit 0 with warnings allowed. Exit 1 on errors. |
| `examples/` | Sample memory files. Not a valid `.feature-guardian/` tree. |
| `adapters/cursor/` | Cursor rule and install notes |
| `tests/test_validate_memory.py` | Unit tests for the validator |
| `tests/fixtures/valid/` | Known-good memory copied by those tests |
| `tests/BEHAVIOR_SCENARIOS.md` | Written acceptance scenarios for agent behavior. Reviewed by hand in v0.1. |

Human install and script flags: [README.md](README.md).

## Tests and the validator

Run both before a pull request:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/validate_memory.py tests/fixtures/valid
```

The fixture command should print `OK: Feature Guardian memory validation passed.` and exit 0.

Validator flags are `project` (default `.`), `--version`, and `--help`. It does not modify files. Warnings are `WARNING [FGxxx]` lines and still exit 0. Errors are `ERROR [FGxxx]` and exit 1. The code list is in the README.

When you change validation rules, extend `tests/test_validate_memory.py`. The existing tests copy `tests/fixtures/valid/` into a temp directory, mutate a file, and assert the exit code and the `FG` code. Follow that pattern. Keep fixtures free of secrets.

`tests/BEHAVIOR_SCENARIOS.md` describes how an agent using the skill should behave. A documentation or skill change that affects those scenarios should update the scenario text in the same pull request. v0.1 does not execute that file.

To try bootstrap locally without touching a real project:

```bash
python3 scripts/bootstrap_memory.py /tmp/fg-bootstrap-demo --name "Demo"
python3 scripts/validate_memory.py /tmp/fg-bootstrap-demo
```

`--force` overwrites `PRODUCT.md`. It does not delete `features/`.

## Style

Match the files around your change.

- Python stays on the standard library: `argparse`, `pathlib`, dataclasses, and type hints. Do not add a dependency for v0.1.
- Keep the current exit codes unless the pull request explains the change. Bootstrap exits 0 when it creates memory or when memory already exists, and 2 when `assets/PRODUCT_TEMPLATE.md` is missing. The validator exits 0 when there are no errors (warnings are allowed) and 1 when there are errors.
- Markdown uses the heading and table style already in `references/`.
- Memory rules that the skill states as non-negotiable stay intact unless the change is explicit: one feature per file, product memory in `PRODUCT.md`, evidence over assertion, append-only history, and `REVIEW_REQUIRED` when a completed feature is credibly affected.
- Document flags, statuses, and paths from the code and the files. Do not describe commands, services, or adapters that are not in the repository. Roadmap items live in the README roadmap and are plans.
- User-facing changes get an entry under `[Unreleased]` in [CHANGELOG.md](CHANGELOG.md), in the style already used there.

## Pull requests

1. Branch from `main`.
2. Make the change, including docs and changelog when the behavior or the public docs change.
3. Run the unit tests and `validate_memory.py` on `tests/fixtures/valid/`.
4. Open a pull request against `main`. The template asks for the summary and the test checklist.
5. GitHub Actions runs those same two commands on the pull request (`.github/workflows/ci.yml`, Python 3.12).

Describe what changed and why. If something is intentionally left for later, say so in the pull request.

## Reporting issues

Use the bug and feature-request templates. Security vulnerabilities go through [SECURITY.md](SECURITY.md), not a public issue.

v0.x will keep changing. A feature request that overlaps the roadmap is still welcome; say which roadmap item it relates to.
