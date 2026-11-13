# Feature Guardian

**Persistent engineering memory and product integrity for AI coding agents.**

[![Status: active development](https://img.shields.io/badge/status-active%20development-orange)](#active-development)
[![Version 0.1.0](https://img.shields.io/badge/version-0.1.0-blue)](CHANGELOG.md)
[![Schema 0.1](https://img.shields.io/badge/schema-0.1-blue)](references/DATA_MODEL.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

<a id="active-development"></a>

> **Active development (v0.x).** This release is **0.1.0**, memory schema **0.1**. APIs, schemas, and script behavior may change before 1.0, and the project will keep being updated as needed. Shipped changes are recorded in the [changelog](CHANGELOG.md). Planned work is in the [roadmap](#roadmap).

> Nothing is forgotten, nothing is assumed to work, and nothing important changes without understanding what it could affect.

Feature Guardian tracks every product feature (including small ones), preserves engineering history, verifies changes with evidence, detects regressions and blast radius, and protects completed features from silent breakage across AI sessions.

| | |
|---|---|
| Skill version | `0.1.0` (in [`SKILL.md`](SKILL.md) metadata) |
| Memory schema | `0.1` (`fg-schema` in memory frontmatter) |
| License | [MIT](LICENSE) |
| Runtime | Python 3.9+ standard library for the two scripts. No package install. |
| Repository | [github.com/ogooluwanick/feature-guardian](https://github.com/ogooluwanick/feature-guardian) |

## Contents

- [What it is](#what-it-is)
- [Why it exists](#why-it-exists)
- [Quick start](#quick-start)
- [Install](#install)
- [How tracking works](#how-tracking-works)
- [Usage walkthrough](#usage-walkthrough)
- [Scripts](#scripts)
- [Memory layout and statuses](#memory-layout-and-statuses)
- [Templates and examples](#templates-and-examples)
- [Opt out](#opt-out)
- [Uninstall](#uninstall)
- [Troubleshooting and FAQ](#troubleshooting-and-faq)
- [Privacy and security](#privacy-and-security)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

## What it is

Feature Guardian is an [Agent Skill](SKILL.md): a `SKILL.md` file plus reference docs, templates, and two Python scripts. An agent that has the skill installed follows it while doing product and engineering work. The memory it writes is plain Markdown in **your** project, under `.feature-guardian/`.

[`SKILL.md`](SKILL.md) is the operating guide the agent loads. This README is the human guide: install it, see what it writes, run the scripts, and turn it off.

It is one feature per file, for the life of that feature. A copy button and a payroll run each get a file. How much you write scales with risk. The file still exists either way.

## Why it exists

AI coding agents handle the current task well and often drop prior failures, rejected approaches, test coverage, dependencies, and whether "done" was verified. Feature Guardian keeps that record in the repo so later sessions use it for implementation, testing, risk, and completion decisions.

## Quick start

From a machine with Git and Python 3.9+ (the `python3` command):

```bash
git clone https://github.com/ogooluwanick/feature-guardian.git
mkdir -p /path/to/your-project/.cursor/skills /path/to/your-project/.cursor/rules
cp -R feature-guardian /path/to/your-project/.cursor/skills/feature-guardian
cp feature-guardian/adapters/cursor/feature-guardian.mdc \
   /path/to/your-project/.cursor/rules/feature-guardian.mdc
cd /path/to/your-project
python3 .cursor/skills/feature-guardian/scripts/bootstrap_memory.py . --name "My Product"
```

Then work in Cursor as usual. The skill plus the always-on rule is what runs Feature Guardian. Details, the portable install path, and how to check the result are below.

## Install

### Requirements

- Git, to clone this repository.
- Python 3.9 or newer as `python3`. Both scripts use only the Python standard library. There is no `requirements.txt` and nothing to pip install. Tests use `tuple[int, str]`, which needs 3.9+. GitHub Actions runs the suite on Python 3.12.
- Cursor, if you want the always-on project rule. The skill files themselves are ordinary Markdown and Python.

`python` is fine wherever that command is Python 3, including the CI runner. The scripts' shebang is `#!/usr/bin/env python3`, and both files are executable.

### 1. Get the repository

```bash
git clone https://github.com/ogooluwanick/feature-guardian.git
```

The copy commands below run from the parent of that clone, where `feature-guardian/` is the directory Git just created. The symlink command is the exception: run it from inside the clone.

### 2. Install the skill

Copy the repository into **one** of these directories in the project you want tracked.

Cursor project skills:

```bash
mkdir -p /path/to/your-project/.cursor/skills
cp -R feature-guardian /path/to/your-project/.cursor/skills/feature-guardian
```

Portable Agent Skills path (agents that read `.agents/skills/`):

```bash
mkdir -p /path/to/your-project/.agents/skills
cp -R feature-guardian /path/to/your-project/.agents/skills/feature-guardian
```

The installed directory must contain `SKILL.md`, `references/`, `assets/`, `scripts/`, and `examples/` at its root. `bootstrap_memory.py` loads `assets/PRODUCT_TEMPLATE.md` from the parent of `scripts/`. Keep those directories together.

A symlink works when you keep one clone and update it with `git pull`:

```bash
ln -s "$(pwd)" /path/to/your-project/.cursor/skills/feature-guardian
```

Run that from inside the clone so `pwd` is the skill root. Use `.agents/skills/feature-guardian` instead for the portable path.

You can also clone straight into the skill directory:

```bash
git clone https://github.com/ogooluwanick/feature-guardian.git \
  /path/to/your-project/.cursor/skills/feature-guardian
```

That nested clone is how you `git pull` updates later. It is optional. A copied tree works without its own `.git` directory; delete `.git` inside the skill directory if you do not want a nested repository.

### 3. Install the Cursor always-on rule

The rule is separate from the skill, and it is Cursor-specific. Copy:

```bash
cp feature-guardian/adapters/cursor/feature-guardian.mdc \
   /path/to/your-project/.cursor/rules/feature-guardian.mdc
```

The file sets `alwaysApply: true`, so Cursor considers Feature Guardian during ordinary coding. The rule is a short reminder. [`SKILL.md`](SKILL.md) stays the operating guide. There is no `.agents` copy of this rule. If the skill lives under `.agents/skills/`, you still add `.cursor/rules/feature-guardian.mdc` for Cursor.

[`assets/CURSOR_RULE_TEMPLATE.mdc`](assets/CURSOR_RULE_TEMPLATE.mdc) is the same rule with explicit skill paths filled in. The file to install is [`adapters/cursor/feature-guardian.mdc`](adapters/cursor/feature-guardian.mdc).

Cursor install notes also live in [`adapters/cursor/INSTALL.md`](adapters/cursor/INSTALL.md).

### 4. Bootstrap memory

From the project you want tracked (not from this repository, unless you intend to track this repository):

```bash
cd /path/to/your-project
python3 .cursor/skills/feature-guardian/scripts/bootstrap_memory.py . --name "My Product"
```

If the skill is under `.agents/skills/`, call that copy of the script instead. `--name` is the product title written into `PRODUCT.md`. Omit it and the script uses the project directory's name.

Bootstrap creates `.feature-guardian/PRODUCT.md` and `.feature-guardian/features/`. It does not create feature files. The agent adds those from [`assets/FEATURE_TEMPLATE.md`](assets/FEATURE_TEMPLATE.md) as it inspects the repo.

### 5. Confirm

- `SKILL.md` is inside the installed skill directory.
- `.cursor/rules/feature-guardian.mdc` contains `alwaysApply: true`.
- `.feature-guardian/PRODUCT.md` exists and the bootstrap command exited 0.
- Validation exits 0:

```bash
python3 .cursor/skills/feature-guardian/scripts/validate_memory.py .
```

A fresh bootstrap is structurally valid: the placeholder registry row does not use an `FG-FEAT-` id, so the validator does not require a feature file yet.

## How tracking works

| Component | Purpose |
|---|---|
| `SKILL.md` | Lifecycle, evidence rules, and schemas. Invoked when the task is product or engineering work. |
| `.cursor/rules/feature-guardian.mdc` | `alwaysApply: true` reminder on those tasks. |
| `.feature-guardian/` | Durable memory in the project repository. |

Continuity between sessions is the Markdown in `.feature-guardian/`. Feature Guardian has no background process, daemon, or hosted service in v0.1. The next agent turn reads the files the previous turn wrote.

The agent applies the skill for product behavior, UX copy that changes behavior, application code, tests, configuration, schemas, dependencies, architecture, bug fixes, refactors, reviews, and completion claims. It skips a feature only when that feature's monitoring is `EXCLUDED`, and it skips work that has no product impact.

You do not run a `/update-feature` or `/save-history` command. Ask for the product change. The checkpoint at the end of the turn is the user-facing result.

## Usage walkthrough

### A small new feature

**You:** "Add a copy button beside the invoice number."

**The agent, following the skill:**

1. Searches `PRODUCT.md` and existing feature files for an alias or overlapping feature before creating a new one.
2. Creates `.feature-guardian/features/copy-invoice-number.md` (one file, kebab-case slug) from the feature template.
3. Assigns a new `FG-FEAT-######` id, sets status, and adds a row to the feature registry in `PRODUCT.md`.
4. Implements the button and runs the tests that match the risk. A small UI feature stays a small file. The schema still wants intent, location, requirement, test or evidence, relationships, and current state.
5. Records evidence (a test result, a runtime observation, or an explicit gap). Implementation alone is not marked verified.
6. Appends an event, bumps `memory-revision`, and runs `validate_memory.py` on the project root.

**You see** a short checkpoint, not the whole memory file:

```text
✓ Copy Invoice Number update completed

Changed: one-click copy beside the invoice number.
Verification: unit test result, and anything not run.
Feature health: HEALTHY — HIGH confidence, with the reasons.
Completed-feature review: none for this isolated change.
Feature Guardian: memory files updated; validator result.
Remaining: anything still unknown.
```

That follows the checkpoint shape in [`SKILL.md`](SKILL.md). The words above are an illustration, not a stored sample. Open `.feature-guardian/features/copy-invoice-number.md` when you want the full record. [`examples/simple-feature.md`](examples/simple-feature.md) shows a completed file for this kind of feature.

### A change that can break a completed feature

When shared payment code changes, the agent:

1. Reads the relationship map and dependencies, not only the file being edited.
2. Marks a completed dependent feature `REVIEW_REQUIRED` and its monitoring `ACTIVE_REVIEW` when the impact is credible.
3. Lists the specific tests to rerun (`FG-TEST-...`). Previous completion evidence stays in the file.
4. After those checks pass, restores `COMPLETED` and `DORMANT`. If they fail, sets `REGRESSED`, records `FG-REG-...`, and keeps the earlier passing result in the event history.

[`examples/regression-heavy-feature.md`](examples/regression-heavy-feature.md) and [`references/IMPACT_AND_REVIEW.md`](references/IMPACT_AND_REVIEW.md) show that protocol.

### What "done" means

The skill's completion check has four outcomes: `VERIFIED_COMPLETE`, `COMPLETE_WITH_KNOWN_RISK`, `NOT_COMPLETE`, and `BLOCKED`. Those are claim outcomes in the testing reference. Feature **status** is a separate field (`COMPLETED`, `REGRESSED`, and the rest below). A feature with code written and a provider never observed is not described as fully verified.

Evidence is ordered: observed runtime behavior, then executed tests, then code and config, then build or lint, then Feature Guardian memory, then inference, then assumption. When memory and a reliable test disagree, the evidence wins and the old claim stays in the history.

## Scripts

Both tools live in [`scripts/`](scripts/). Run them with `python3` or by executing the file. Paths below assume your current directory is the project being checked, and the skill is installed at `.cursor/skills/feature-guardian/`. Substitute `.agents/skills/feature-guardian/` if that is where you copied it. From a clone of this repository, `scripts/bootstrap_memory.py` and `scripts/validate_memory.py` are the same programs.

`--help` and `--version` work on both. Version strings:

```text
feature-guardian-bootstrap 0.1.0 (schema 0.1)
feature-guardian-validate 0.1.0 (schema 0.1)
```

### `bootstrap_memory.py`

Creates `.feature-guardian/` from [`assets/PRODUCT_TEMPLATE.md`](assets/PRODUCT_TEMPLATE.md). It substitutes three placeholders: `{{PROJECT_NAME}}`, `{{CREATED_AT}}` (local-time ISO-8601, seconds precision), and `{{FG_SCHEMA}}` (`0.1`).

```text
python3 scripts/bootstrap_memory.py [-h] [--name NAME] [--force] [--version] [project]
```

| Argument | Meaning |
|---|---|
| `project` | Project root. Default: current directory (`.`). Resolved to an absolute path. |
| `--name` | Product display name written into `PRODUCT.md`. Default: the project directory's basename. |
| `--force` | Overwrite `PRODUCT.md` when memory already exists. The help text marks this as destructive. |
| `--version` | Print the version string and exit. |
| `-h`, `--help` | Print argparse help and exit. |

Behavior that matters:

- If `.feature-guardian/` **does not** exist, the script creates it, creates `features/`, writes `PRODUCT.md`, and exits 0. It does not add feature files.
- If `.feature-guardian/` **already** exists and you omit `--force`, the script prints `Memory already exists`, leaves an existing `PRODUCT.md` in place, creates `features/` only when that directory is missing, and exits 0. It does not treat "already bootstrapped" as a failure.
- In that already-exists path, a missing `PRODUCT.md` stays missing until you pass `--force`.
- `--force` overwrites `PRODUCT.md` and prints a warning first. It does not ask for confirmation. It does not delete files under `features/`.
- `mkdir(parents=True)` creates missing directories up to the memory root. A mistyped project path can create a new directory. Check the `Project:` line in the output.
- Exit 2 means `assets/PRODUCT_TEMPLATE.md` is missing beside `scripts/` (`FileNotFoundError`). Other unexpected failures are a Python traceback.

```bash
python3 .cursor/skills/feature-guardian/scripts/bootstrap_memory.py . --name "My Product"
python3 .cursor/skills/feature-guardian/scripts/bootstrap_memory.py /path/to/your-project --force
```

The success message suggests `python scripts/validate_memory.py <project-root>`. From an installed copy, call the script by its installed path, as in the validate examples below.

### `validate_memory.py`

Checks structural integrity of `.feature-guardian/` at a project root. It does not modify memory. There is no repair flag in v0.1.

```text
python3 scripts/validate_memory.py [-h] [--version] [project]
```

| Argument | Meaning |
|---|---|
| `project` | Directory that contains `.feature-guardian/`. Default: current directory. |
| `--version` | Print the version string and exit. |
| `-h`, `--help` | Print argparse help and exit. |

```bash
python3 .cursor/skills/feature-guardian/scripts/validate_memory.py .
python3 scripts/validate_memory.py tests/fixtures/valid
```

The second command is how this repository checks its known-good fixture.

Exit codes:

| Code | When |
|---|---|
| 0 | No errors. Warnings may still be printed. |
| 1 | One or more errors. |

Output is `ERROR [FGxxx]` and `WARNING [FGxxx]` lines, then either `OK: Feature Guardian memory validation passed.` or no OK line, then `Summary: N error(s), M warning(s)`.

The validator checks, in short:

- `.feature-guardian/` and `PRODUCT.md` exist.
- Product `fg-schema`, when present, matches `0.1` (a mismatch or a missing value is a warning).
- Recommended product sections exist (missing sections are warnings): Identity, Fast Context, Feature Registry, Feature Relationship Map, Current Product Health.
- Each `features/*.md` file has frontmatter, `fg-schema`, and a `feature-id` of the form `FG-FEAT-` plus six digits.
- Status, monitoring, health, and confidence are in the sets below when those keys are present.
- `memory-revision`, when present, is an integer.
- Filenames are kebab-case (warning if not). Frontmatter `slug` matches the filename (warning if not).
- Feature ids and canonical slugs are unique. Heading-defined stable ids are unique.
- Every `FG-FEAT-` registry row has a feature file, and every feature file is in the registry.
- Feature bodies contain the markers `FG:FAST_CONTEXT`, `FG:CURRENT_STATE`, and `FG:IMMUTABLE_EVENT_HISTORY` (warning if missing).
- A `COMPLETED` feature has no open critical regression and no open critical or blocking issue.
- Referenced `FG-TEST-` and `FG-FEAT-` ids are defined somewhere in the memory corpus (warning if not).

It does not run the project's tests, read application code, or decide whether a feature works.

#### Result codes

| Code | Level | Meaning |
|---|---|---|
| FG001 | error | No `.feature-guardian/` directory. |
| FG002 | error | No `PRODUCT.md`. |
| FG003 | warning | No `features/` directory. |
| FG004 | error | Duplicate feature slug filename. |
| FG005 | warning | Feature filename is not a kebab-case slug. |
| FG006 | error | Same `feature-id` in two files. |
| FG007 | error | Duplicate stable id, or the same feature id defined in two frontmatters. |
| FG008 | error | Registry row has no feature file. |
| FG009 | error | Feature file is missing from the registry. |
| FG010 | warning | `PRODUCT.md` `fg-schema` is not `0.1`. |
| FG011 | warning | `PRODUCT.md` has no `fg-schema`. |
| FG012 | warning | `PRODUCT.md` is missing a recommended section. |
| FG013 | error | Feature file has no YAML frontmatter. |
| FG014 | warning | Feature `fg-schema` is not `0.1`. |
| FG015 | error | Feature frontmatter has no `fg-schema`. |
| FG016 | error | Missing or invalid `feature-id`. |
| FG017 | warning | Frontmatter `slug` does not match the filename. |
| FG018 | error | Status is not in the allowed set. |
| FG019 | error | Monitoring is not in the allowed set. |
| FG020 | error | Health is not in the allowed set. |
| FG021 | error | Confidence is not in the allowed set. |
| FG022 | error | `memory-revision` is present and not numeric. |
| FG023 | warning | Missing `FG:FAST_CONTEXT`, `FG:CURRENT_STATE`, or `FG:IMMUTABLE_EVENT_HISTORY`. |
| FG024 | error | `COMPLETED` feature has an open `CRITICAL` regression. |
| FG025 | error | `COMPLETED` feature has an open `CRITICAL` or `BLOCKING` issue. |
| FG026 | warning | `COMPLETED` feature contains `Freshness: STALE`. |
| FG027 | warning | A test id under a `Protected by:` list was not found in the feature body. |
| FG028 | warning | The file contains `CONTRADICTION` and `Status: OPEN`. This is a text search, not a parsed block. |
| FG029 | warning | A referenced `FG-TEST-` id is not defined in the memory corpus. |
| FG030 | warning | A referenced `FG-FEAT-` id is not defined in the memory corpus. |
| FG031 | error | Two feature files use the same frontmatter `slug`. |

## Memory layout and statuses

```text
.feature-guardian/
├── PRODUCT.md          # Product intent, registry, relationships
└── features/
    └── <slug>.md       # One permanent file per feature
```

One feature is one permanent Markdown file. The filename is the slug (`copy-invoice-number.md`). Identity is `feature-id` in the frontmatter, not the filename. Renames and merges are recorded; the file is not split into several memory files for one feature.

`PRODUCT.md` holds product intent, the feature registry, the relationship map, and product-level health. The registry is an index. The feature file is the detail. Every feature file needs a registry row whose feature id matches the frontmatter, and every `FG-FEAT-` registry row needs a file. The bootstrap template ships a non-id placeholder row (`_None yet_`) until the first real feature is added.

### Feature frontmatter

Schema: [`references/FEATURE_MEMORY_SCHEMA.md`](references/FEATURE_MEMORY_SCHEMA.md). A new file starts from [`assets/FEATURE_TEMPLATE.md`](assets/FEATURE_TEMPLATE.md).

```yaml
---
fg-schema: "0.1"
memory-revision: 1
feature-id: FG-FEAT-000027
name: Human Name
slug: feature-slug
aliases:
  - alternate-name
status: IN_DEVELOPMENT
health: DEGRADED
confidence: MEDIUM
monitoring: ACTIVE
last-updated: "2026-09-04T18:30:00+01:00"
last-verified-commit: null
---
```

`memory-revision` increments after a successful meaningful update. There is no side-car id counter: the writer picks the next unused id. Ids are never reused. Gaps are fine.

### Feature status

`DISCOVERED` · `PLANNED` · `IN_DEVELOPMENT` · `TESTING` · `BLOCKED` · `REVIEW_REQUIRED` · `REGRESSED` · `COMPLETED` · `DEPRECATED`

`DISCOVERED` is the right status for pre-existing behavior that has not been verified yet.

### Monitoring

Separate from status: `ACTIVE` · `DORMANT` · `ACTIVE_REVIEW` · `EXCLUDED`

A typical completed feature is `COMPLETED` and `DORMANT`. A review in progress is `REVIEW_REQUIRED` and `ACTIVE_REVIEW`. `EXCLUDED` means the user turned tracking off for that feature. The file stays.

### Health and confidence

**Health:** `HEALTHY` · `DEGRADED` · `UNSAFE` · `UNKNOWN`

**Confidence:** `HIGH` · `MEDIUM` · `LOW` · `UNKNOWN`

`UNKNOWN` is a valid value. Health conclusions are supposed to list the reasons (failed tests, open issues, stale evidence).

### Ids you will see in the files

| Prefix | Meaning |
|---|---|
| `FG-FEAT-` | Feature |
| `FG-REQ-` | Requirement |
| `FG-INV-` | Invariant |
| `FG-TEST-` | Registered test |
| `FG-EVID-` | Evidence |
| `FG-ISSUE-` | Issue |
| `FG-REG-` | Regression |
| `FG-DEC-` | Decision |
| `FG-CHG-` | Meaningful change |
| `FG-EVT-` | Append-only event |

The full prefix list, requirement and decision states, and event types are in [`references/DATA_MODEL.md`](references/DATA_MODEL.md). Numbers are six digits (`FG-FEAT-000027`).

### Where to read more

| Topic | Document |
|---|---|
| Lifecycle the agent follows | [`references/OPERATING_PROTOCOL.md`](references/OPERATING_PROTOCOL.md) |
| Ids, events, revisions | [`references/DATA_MODEL.md`](references/DATA_MODEL.md) |
| Feature file sections | [`references/FEATURE_MEMORY_SCHEMA.md`](references/FEATURE_MEMORY_SCHEMA.md) |
| Product file sections | [`references/PRODUCT_MEMORY_SCHEMA.md`](references/PRODUCT_MEMORY_SCHEMA.md) |
| Tests, evidence, completion | [`references/TESTING_AND_EVIDENCE.md`](references/TESTING_AND_EVIDENCE.md) |
| Blast radius and review | [`references/IMPACT_AND_REVIEW.md`](references/IMPACT_AND_REVIEW.md) |
| Boundaries, merge, split, opt-out | [`references/FEATURE_BOUNDARIES.md`](references/FEATURE_BOUNDARIES.md) |
| Git and several agents | [`references/GIT_AND_MULTI_AGENT.md`](references/GIT_AND_MULTI_AGENT.md) |
| Safety and destructive edits | [`references/SAFETY_AND_AUTONOMY.md`](references/SAFETY_AND_AUTONOMY.md) |
| What the user should see | [`references/BEGINNER_EXPERIENCE.md`](references/BEGINNER_EXPERIENCE.md) |

## Templates and examples

| File | Role |
|---|---|
| [`assets/PRODUCT_TEMPLATE.md`](assets/PRODUCT_TEMPLATE.md) | Source for `PRODUCT.md`. Bootstrap fills `{{PROJECT_NAME}}`, `{{CREATED_AT}}`, and `{{FG_SCHEMA}}`. |
| [`assets/FEATURE_TEMPLATE.md`](assets/FEATURE_TEMPLATE.md) | Empty feature file: frontmatter plus the canonical sections and `FG:` markers. Copy it to `.feature-guardian/features/<slug>.md` and fill it in. Bootstrap does not copy it for you. |
| [`assets/CURSOR_RULE_TEMPLATE.mdc`](assets/CURSOR_RULE_TEMPLATE.mdc) | Rule template with skill paths written out. Install the adapter file, not this one, unless you are editing the rule. |
| [`examples/simple-feature.md`](examples/simple-feature.md) | Completed, healthy, dormant copy-invoice-number feature (`FG-FEAT-000099`). |
| [`examples/mature-feature.md`](examples/mature-feature.md) | Payroll in development, health degraded, monitoring active (`FG-FEAT-000002`). |
| [`examples/regression-heavy-feature.md`](examples/regression-heavy-feature.md) | Payments regressed after a recorded change (`FG-FEAT-000003`). |
| [`examples/PRODUCT.example.md`](examples/PRODUCT.example.md) | Sample product memory ("Acme Payroll") whose registry lists those features plus authentication. |

The examples are illustrations of shape and tone. They are not a `.feature-guardian/` tree: the filenames are `simple-feature.md` and similar, and the product sample mentions an authentication feature that has no file in `examples/`. Copying `examples/` into a project and running the validator will fail the registry checks. Use the assets as the starting point, and use the examples to see how full a small file, an in-progress file, and a regressed file look.

[`tests/fixtures/valid/`](tests/fixtures/valid/) is the known-good memory the unit tests copy. It is a test fixture, not a product template.

To add a feature by hand:

1. Copy `assets/FEATURE_TEMPLATE.md` to `.feature-guardian/features/<slug>.md`. The slug is lowercase words separated by hyphens.
2. Set a new `feature-id`, `name`, `slug` (same as the filename), and the status fields.
3. Replace `None recorded` only where you have something to say. Empty sections stay short.
4. Add a matching row to the feature registry in `PRODUCT.md`.
5. Run `validate_memory.py` on the project root.

Search aliases and the registry before creating a file, so "monthly pay" does not become a second payroll feature.

## Opt out

Say so in the conversation. The agent sets `Monitoring` on the feature. v0.1 has no separate opt-out file.

| You say | What happens |
|---|---|
| "Stop tracking this feature" | `Monitoring: EXCLUDED`. The file and its history stay. |
| "Never track this feature" | A product-level exclusion, and `Monitoring: EXCLUDED`. |
| "Delete Feature Guardian history for X" | The agent deletes only after you explicitly ask. It updates the registry. Casual "ignore for now" keeps the history. |

`EXCLUDED` is reversible: set monitoring back to `ACTIVE` or `DORMANT`. Deletion is not, so it waits for an explicit request. Details: [`references/FEATURE_BOUNDARIES.md`](references/FEATURE_BOUNDARIES.md) and [`references/SAFETY_AND_AUTONOMY.md`](references/SAFETY_AND_AUTONOMY.md).

## Uninstall

1. Delete `.cursor/rules/feature-guardian.mdc`.
2. Delete the skill directory you installed: `.cursor/skills/feature-guardian/` or `.agents/skills/feature-guardian/` (or remove the symlink).
3. Keep `.feature-guardian/` if you still want the Markdown history in the project. Delete that directory only when you want the memory gone.

Removing the skill leaves the memory files where they are.

## Troubleshooting and FAQ

**Bootstrap says `Memory already exists` and exits 0.** The project was already initialized. Existing `PRODUCT.md` was kept. Pass `--force` only when you intend to replace `PRODUCT.md`. Feature files are left in place either way.

**Bootstrap exits 2 with `Missing asset template`.** The script is separated from `assets/PRODUCT_TEMPLATE.md`. Re-copy the skill so `scripts/` and `assets/` share one parent directory.

**A new directory appeared after bootstrap.** The `project` argument is created if it does not exist. Confirm the path you passed.

**Validator exits 1 with FG001 or FG002.** Run it on the project root (the directory that contains `.feature-guardian/`), not on `.feature-guardian` itself and not on this skill repository unless you have bootstrapped this repo.

**FG008 or FG009.** The registry and the files under `features/` disagree. Add the missing file or the missing registry row, and make the `FG-FEAT-` ids match. The `_None yet_` placeholder row is ignored because it is not an `FG-FEAT-` id.

**FG018 (or FG019, FG020, FG021).** A frontmatter value is outside the sets in [Memory layout and statuses](#memory-layout-and-statuses). The schema and the validator use the same sets.

**Warnings and exit 0.** Warnings are printed and the process still exits 0. CI for this repository fails on a non-zero exit, so warnings in the fixture would not fail CI. Treat warnings as memory to fix, and errors as invalid memory.

**The agent never brings Feature Guardian up.** Confirm both pieces: the skill directory contains `SKILL.md`, and `.cursor/rules/feature-guardian.mdc` is present with `alwaysApply: true`. The portable skill path alone does not install the Cursor rule.

**Does this run in the background?** No. The next session continues from the Markdown files.

**Does the validator prove the product works?** No. It checks memory structure and cross-references. Test results are recorded in the feature file when the agent, or you, run the project's own tests.

**Are the behavior scenarios automated?** [`tests/BEHAVIOR_SCENARIOS.md`](tests/BEHAVIOR_SCENARIOS.md) is the written acceptance list for agent behavior (20 scenarios). Automated coverage in v0.1 is [`tests/test_validate_memory.py`](tests/test_validate_memory.py), which exercises the validator.

**Can several agents edit memory?** Yes. They share the files. `memory-revision`, the event history, and a validator run after edits are how conflicts stay visible. See [`references/GIT_AND_MULTI_AGENT.md`](references/GIT_AND_MULTI_AGENT.md). Commit `.feature-guardian/` when you want that history on a branch. The skill does not commit or push unless you ask.

**Which agents besides Cursor?** v0.1 ships a Cursor rule and the portable `.agents/skills/` directory layout. Adapters for other products are roadmap items, not files in this repository.

## Privacy and security

- Memory is plain Markdown in **your** repository.
- Record configuration **names** only. API keys, passwords, tokens, and connection strings with credentials do not belong in memory.
- v0.1 has no telemetry, hosted backend, or cloud sync.

To report a vulnerability in this repository, use GitHub private vulnerability reporting. See [`SECURITY.md`](SECURITY.md). Do not open a public issue for that.

## Limitations

v0.1 is the behavior in this repository:

- No dashboard, database, MCP server, or pull-request bot.
- No background execution between sessions.
- The validator checks structure and references. It does not run tests or observe runtime behavior.
- Skill-behavior scenarios are documented for review. They are not an automated suite yet.
- Cursor applies the skill on ordinary tasks when the skill **and** the always-on rule are installed.
- Schema migration is described in [`references/DATA_MODEL.md`](references/DATA_MODEL.md). The only schema that exists today is `0.1`.
- `--force` overwrites `PRODUCT.md` without a confirmation prompt.

## Roadmap

These are plans. The published behavior is v0.1.

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

## Package layout

```text
feature-guardian/
├── SKILL.md                 # Agent operating guide
├── README.md                # This guide
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── LICENSE                  # MIT
├── references/              # Protocol and schemas
├── assets/                  # Product, feature, and rule templates
├── scripts/                 # bootstrap_memory.py, validate_memory.py
├── examples/                # Sample memory files (not a valid tree)
├── adapters/cursor/         # Always-on rule and Cursor install notes
├── tests/                   # Validator unit tests, fixture, behavior scenarios
└── .github/                 # Issue and PR templates, CI workflow
```

## Version and schema compatibility

- Skill version: `0.1.0`
- Memory schema: `0.1`
- When a future skill's schema is newer than the memory it opens, the skill is supposed to migrate in place, keep history, append a `SCHEMA_MIGRATED` event, update `fg-schema`, and validate. That procedure is specified. v0.1 has nothing older to migrate.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the local test loop, validator, and pull requests. The code of conduct is [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Security reports go through [`SECURITY.md`](SECURITY.md).

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/validate_memory.py tests/fixtures/valid
```

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md).

## License

[MIT](LICENSE). Copyright (c) 2026 Feature Guardian contributors.
