# Data Model

Stable IDs, events, and revision tracking for Feature Guardian schema `0.1`.

## ID categories

| Prefix | Purpose |
|---|---|
| `FG-FEAT-` | Feature (immutable identity) |
| `FG-REQ-` | Requirement |
| `FG-INV-` | Invariant |
| `FG-TEST-` | Registered test |
| `FG-EVID-` | Evidence record |
| `FG-ISSUE-` | Issue (may span features) |
| `FG-REG-` | Regression |
| `FG-DEC-` | Decision |
| `FG-RISK-` | Risk |
| `FG-DEP-` | Dependency |
| `FG-CONTRACT-` | Cross-feature contract |
| `FG-UNK-` | Unknown |
| `FG-ASM-` | Assumption |
| `FG-CHG-` | Meaningful change |
| `FG-TODO-` | Feature-scoped todo (ACTIVE WORK) |
| `FG-DEBT-` | Test/regression debt |
| `FG-ROLLBACK-` | Rollback record |
| `FG-EVT-` | Immutable event |

IDs are six-digit zero-padded (`FG-FEAT-000027`). Never reuse IDs. Gaps are acceptable.

## Feature lifecycle status

`DISCOVERED` · `PLANNED` · `IN_DEVELOPMENT` · `TESTING` · `BLOCKED` · `REVIEW_REQUIRED` · `REGRESSED` · `COMPLETED` · `DEPRECATED`

## Monitoring (separate from status)

`ACTIVE` · `DORMANT` · `ACTIVE_REVIEW` · `EXCLUDED`

Typical completed state: `Status: COMPLETED`, `Monitoring: DORMANT`.

Review trigger: `Status: REVIEW_REQUIRED`, `Monitoring: ACTIVE_REVIEW`.

## Health and confidence

**Health:** `HEALTHY` · `DEGRADED` · `UNSAFE` · `UNKNOWN`

**Confidence:** `HIGH` · `MEDIUM` · `LOW` · `UNKNOWN`

Every health conclusion must list deriving reasons (failed tests, open issues, stale evidence).

## Requirement states

`PROPOSED` · `ACCEPTED` · `IMPLEMENTED` · `VERIFIED` · `BLOCKED` · `BROKEN` · `SUPERSEDED` · `REMOVED`

Never delete; supersede with reason and successor ID.

## Decision states

`ACTIVE` · `EXPERIMENTAL` · `SUPERSEDED` · `REVERSED`

## Fact discipline

When debugging, label: `FACT` · `INTERPRETATION` · `HYPOTHESIS` · `CONFIRMED_ROOT_CAUSE`.

If unproven: `Root cause: UNKNOWN`.

## Event types (append-only history)

Include: `FEATURE_CREATED`, `FEATURE_DISCOVERED`, `FEATURE_RENAMED`, `FEATURE_MERGED`, `FEATURE_SPLIT`, `FEATURE_DEPRECATED`, `FEATURE_EXCLUDED`, `REQUIREMENT_ADDED`, `REQUIREMENT_CHANGED`, `REQUIREMENT_SUPERSEDED`, `IMPLEMENTATION_CHANGED`, `DEPENDENCY_CHANGED`, `CONTRACT_CHANGED`, `ASSUMPTION_INVALIDATED`, `TEST_ADDED`, `TEST_RUN`, `TEST_PASSED`, `TEST_FAILED`, `TEST_FLAKY`, `ISSUE_FOUND`, `ISSUE_RESOLVED`, `REGRESSION_FOUND`, `REGRESSION_RESOLVED`, `DECISION_MADE`, `DECISION_SUPERSEDED`, `APPROACH_REJECTED`, `ROLLBACK`, `REVIEW_REQUIRED`, `REVIEW_PASSED`, `REVIEW_FAILED`, `CONTRADICTION_FOUND`, `CONSTITUTION_CHANGED`, `PRODUCT_ALIGNMENT_WARNING`, `RELEASE_BASELINE`, `MEMORY_CORRECTION`, `SCHEMA_MIGRATED`, `TODO_ADDED`, `TODO_STARTED`, `TODO_COMPLETED`, `TODO_CANCELLED`, `TODO_BLOCKED`.

Historical events are never deleted. Wrong beliefs get `MEMORY_CORRECTION` appended.

## Memory revision

`fg-schema` and `memory-revision` in frontmatter of `PRODUCT.md` and each feature file.

Increment `memory-revision` after each successful meaningful update.

## Schema migration

When skill schema > memory schema:

1. Detect old schema.
2. Migrate in place; preserve all history.
3. Append `SCHEMA_MIGRATED` event.
4. Update `fg-schema`.
5. Validate.

v0.1 implements the migration interface; only schema `0.1` exists today.

## Contradiction handling

When evidence contradicts memory:

1. Evidence wins for current state.
2. Preserve historical claim in event history.
3. Update current state sections.
4. Record `CONTRADICTION_FOUND` event.
5. Open issue/regression when appropriate.

## Multi-feature issues

One `FG-ISSUE-...` identity; record per-feature impact in each affected feature file.

## Regression lineage

Link: `FG-REG-...` introduced by `FG-CHG-...`, affects `FG-REQ-...`, detected by `FG-TEST-...`, resolved by `FG-CHG-...`, protected by `FG-TEST-...`.

## Parity units and events

Parity manifests are additive to schema 0.1. Prefer schema 2 **parity cards** (local item ids); schema 1 units remain valid. Link global FG-CONTRACT / FG-ISSUE / FG-TODO / FG-EVID / FG-DEC records rather than duplicating feature files. See [PARITY.md](PARITY.md). Append PARITY_BASELINE_RECORDED, PARITY_DRIFT_FOUND, PARITY_EVIDENCE_INVALIDATED and PARITY_VERIFIED events as appropriate. Missing historical parity is UNKNOWN, not a regression inferred from absent records.
