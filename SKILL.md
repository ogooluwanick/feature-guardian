---
name: feature-guardian
description: >-
  Persistent product and feature engineering memory for AI-assisted development.
  Use whenever creating, modifying, debugging, testing, refactoring, reviewing,
  or completing product behavior, including small features. Tracks feature intent,
  requirements, tests, evidence, dependencies, regressions, failures, decisions,
  blast radius, and completed-feature review across sessions.
license: MIT
metadata:
  version: "0.1.0"
  schema-version: "0.1"
---

# Feature Guardian

**Nothing is forgotten, nothing is assumed to work, and nothing important changes without understanding what it could affect.**

Feature Guardian is persistent engineering memory for AI coding agents. It tracks every product feature (including small ones), preserves complete history, verifies claims with evidence, detects regressions and blast radius, and protects completed features from silent breakage.

## When this skill applies

Apply automatically for any task that touches:

- product behavior, UX copy with behavioral impact, or feature scope;
- application code, tests, configuration, schemas, or dependencies;
- architecture, contracts, or shared infrastructure;
- bug fixes, refactors, reviews, or completion claims.

Skip only when the user explicitly excluded the feature (`Monitoring: EXCLUDED`) or the task is purely unrelated tooling with zero product impact.

## Non-negotiable rules

1. **One feature = one permanent Markdown file** in `.feature-guardian/features/<slug>.md`. Never split a feature across multiple memory files.
2. **Product memory is separate:** `.feature-guardian/PRODUCT.md` holds product intent, registry, and relationships.
3. **Memory is not evidence.** Evidence hierarchy: runtime observation → executed tests → code/config → build/lint → memory → inference → assumption.
4. **No evidence, no claim.** Never mark FIXED/VERIFIED/STABLE from implementation alone.
5. **Preserve history.** Failures, rejected approaches, regressions, and superseded decisions are append-only.
6. **Blast radius on meaningful changes.** See [IMPACT_AND_REVIEW.md](references/IMPACT_AND_REVIEW.md).
7. **Completed ≠ forgotten.** Credible downstream impact → `REVIEW_REQUIRED`, not silent breakage.
8. **User remains authority.** Recommend and warn; block only on hard invariant violations or unrequested destructive ops.
9. **Track small features.** Copy buttons, dark mode, CSV export — all get memory.
10. **Uncertainty stays explicit.** `UNKNOWN` is valid; never invent root causes.

## Runtime memory layout

```text
.feature-guardian/
├── PRODUCT.md
└── features/
    └── <feature-slug>.md
```

Bootstrap if missing: run `scripts/bootstrap_memory.py` from the installed skill package, then inspect the repository and populate memory.

## Operating lifecycle

For every meaningful engineering task, follow [OPERATING_PROTOCOL.md](references/OPERATING_PROTOCOL.md):

```text
Identify feature(s) → Load PRODUCT.md + feature memory → Inspect code/tests
→ Reconcile memory with evidence → Check alignment + invariants → Risk + blast radius
→ Select test depth → Implement → Run tests → Check regressions
→ Flag completed features for review → Update memory + append events
→ Validate memory → Concise user report
```

## Start of work (before changing code)

1. Load `PRODUCT.md` and relevant feature file(s). Use section markers and IDs — do not dump entire histories blindly.
2. Read constitution, current state, active issues, failed approaches, invariants, dependencies, and test registry.
3. Inspect actual code, tests, and Git state. Reconcile contradictions (evidence wins).
4. Search aliases/registry before creating a new feature file.

## During work

Update memory after **meaningful events** (implementation milestone, test result, failure, decision, regression, contract change, review trigger). Increment `memory-revision` in frontmatter after successful updates.

Record change IDs (`FG-CHG-...`) for meaningful engineering changes.

## End of work (before declaring done)

1. Run relevant tests at appropriate depth (default: Level 2 — feature + related/dependency). See [TESTING_AND_EVIDENCE.md](references/TESTING_AND_EVIDENCE.md).
2. Never claim completion without [completion check](references/TESTING_AND_EVIDENCE.md#feature-completion-check).
3. Mark affected completed features `REVIEW_REQUIRED` with required verification listed.
4. Append session checkpoint and immutable events.
5. Update `PRODUCT.md` registry/health if product-level state changed.
6. Run `validate_memory.py` on the project root.

## Direction conflicts

Evaluate requests against product vision, principles, constitution, non-goals, and invariants:

| Level | Action |
|---|---|
| ALIGNED | Proceed |
| POTENTIAL_CONFLICT | Explain; continue if intent clear |
| STRONG_CONFLICT | Ask before changing constitution |
| INVARIANT_VIOLATION | Stop; require explicit resolution |

Details: [SAFETY_AND_AUTONOMY.md](references/SAFETY_AND_AUTONOMY.md)

## Reference map

| Topic | Document |
|---|---|
| Full lifecycle | [OPERATING_PROTOCOL.md](references/OPERATING_PROTOCOL.md) |
| IDs, events, revisions | [DATA_MODEL.md](references/DATA_MODEL.md) |
| Feature file schema | [FEATURE_MEMORY_SCHEMA.md](references/FEATURE_MEMORY_SCHEMA.md) |
| Product file schema | [PRODUCT_MEMORY_SCHEMA.md](references/PRODUCT_MEMORY_SCHEMA.md) |
| Tests and evidence | [TESTING_AND_EVIDENCE.md](references/TESTING_AND_EVIDENCE.md) |
| Blast radius and review | [IMPACT_AND_REVIEW.md](references/IMPACT_AND_REVIEW.md) |
| Feature boundaries, merge/split | [FEATURE_BOUNDARIES.md](references/FEATURE_BOUNDARIES.md) |
| Git and multi-agent | [GIT_AND_MULTI_AGENT.md](references/GIT_AND_MULTI_AGENT.md) |
| Safety, opt-out, destructive ops | [SAFETY_AND_AUTONOMY.md](references/SAFETY_AND_AUTONOMY.md) |
| Beginner experience | [BEGINNER_EXPERIENCE.md](references/BEGINNER_EXPERIENCE.md) |

## Templates and examples

- New feature: [assets/FEATURE_TEMPLATE.md](assets/FEATURE_TEMPLATE.md)
- New product: [assets/PRODUCT_TEMPLATE.md](assets/PRODUCT_TEMPLATE.md)
- Examples: [examples/](examples/)

## User report format

After meaningful work, provide a compact checkpoint (not a full memory dump):

```text
✓ [Feature] update completed

Changed: ...
Verification: ... (tests run, results, environments)
Feature health: HEALTHY — HIGH confidence (with reasons)
Completed-feature review: ...
Feature Guardian: memory files updated; validator result
Remaining: ... (explicit unknowns/limitations)
```

## Limitations (v0.1)

- No background execution between sessions; continuity depends on memory files and the next agent turn.
- No hosted dashboard, database, or MCP server.
- Validator checks structure and key consistency; it does not run tests or verify runtime behavior.
- Automatic behavior in Cursor requires both this skill **and** the always-on adapter rule.

## Version

Skill `0.1.0` · Schema `0.1`

Human guide (install, scripts, opt-out, uninstall): [README.md](README.md). Cursor steps: [adapters/cursor/INSTALL.md](adapters/cursor/INSTALL.md).
