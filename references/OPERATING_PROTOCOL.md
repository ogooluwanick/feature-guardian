# Operating Protocol

Central lifecycle for Feature Guardian v0.1.

## Automatic protocol

When `.feature-guardian/` exists, run [PREFLIGHT_PROTOCOL.md](PREFLIGHT_PROTOCOL.md) **before** editing product code. Pair substantial work with unlazy gates per [COMPANION_SKILLS.md](COMPANION_SKILLS.md).

```text
USER REQUEST
      ↓
FG PREFLIGHT (mandatory)
      ↓
COUNCIL / TASTE (when triggered)
      ↓
UNLAZY GATES (substantial work)
      ↓
IDENTIFY PRODUCT + FEATURE(S)
      ↓
LOAD PRODUCT.md
      ↓
LOAD RELEVANT FEATURE MEMORY + PEER FAST CONTEXT (RELATED FEATURES graph)
      ↓
READ ACTIVE WORK + CURRENT STATE / FAILURES / DECISIONS / INVARIANTS
      ↓
INSPECT ACTUAL CODE + TESTS + GIT STATE
      ↓
RECONCILE MEMORY WITH EVIDENCE
      ↓
CHECK PRODUCT + FEATURE ALIGNMENT
      ↓
CALCULATE RISK
      ↓
CALCULATE BLAST RADIUS
      ↓
READ PARITY CARD INDEX / PATH INTERSECTION / ESCALATE IF STALE OR TOUCHED
      ↓
SELECT TEST DEPTH
      ↓
IMPLEMENT
      ↓
RUN DIRECT TESTS
      ↓
RUN RELATED / DEPENDENCY TESTS
      ↓
CHECK INVARIANTS
      ↓
CHECK REGRESSIONS
      ↓
RECONCILE PARITY CARDS / HASH STALE GATE / REPORT DRIFTS TO USER / ASK IF DECISION NEEDED
      ↓
FLAG COMPLETED FEATURES FOR REVIEW
      ↓
CREATE MISSING TESTS / RECORD TEST DEBT
      ↓
UPDATE CURRENT MEMORY (increment memory-revision)
      ↓
APPEND EVENTS / FAILURES / DECISIONS
      ↓
UPDATE PRODUCT.md IF PRODUCT-LEVEL STATE CHANGED
      ↓
VALIDATE MEMORY
      ↓
SESSION CHECKPOINT
      ↓
CONCISE USER REPORT
```

## Feature identification

Use evidence from: user intent, routes/screens, API endpoints, modules, DB entities, tests, aliases, product registry, related features.

Before creating a new feature file:

1. Search canonical names and aliases in `PRODUCT.md` and `features/`.
2. Inspect related features for overlap.
3. Determine if the request extends an existing feature.
4. Avoid duplicates from wording variations (`payroll` vs `monthly-pay`).

## Peer awareness (after identification)

Before implementation on the primary feature:

1. Load [FEATURE_PEER_AWARENESS.md](FEATURE_PEER_AWARENESS.md) peer pass.
2. Update **RELATED FEATURES** when code inspection reveals new peers.
3. Sync `PRODUCT.md` relationship map when product-level edges change.

Isolation is valid only when **Known Non-Dependencies** or explicit standalone peers are recorded.

## Bootstrap (no `.feature-guardian/` yet)

1. Run `bootstrap_memory.py`.
2. Inspect repository (README, docs, code, tests).
3. Create `PRODUCT.md` content from evidence.
4. Create a feature file for every identifiable product behavior, including small ones.
5. Mark uncertain pre-existing behavior as `DISCOVERED`; do not claim verified without evidence.
6. Record code/test locations and unknowns.

For large repos, bootstrap in passes but do not permanently ignore small features.

## New feature creation

1. Allocate `FG-FEAT-...` ID (immutable).
2. Create slug and aliases; use [FEATURE_TEMPLATE.md](../assets/FEATURE_TEMPLATE.md).
3. Derive constitution from user intent; mark inferences as assumptions.
4. Add row to product registry and relationship map.
5. Set lifecycle `PLANNED` or `IN_DEVELOPMENT`.

## Memory update timing

Do **not** update after every line edit. Update after meaningful events:

- implementation milestone, test result, failure, bug discovered;
- approach abandoned, architecture/product decision;
- regression discovered/fixed, requirement changed/completed;
- dependency/contract/invariant affected, review triggered, rollback;
- **todo added, started, completed, cancelled, or blocked** (`FG-TODO-...`).

## Feature todos

See [FEATURE_TODOS.md](FEATURE_TODOS.md). During work:

1. Preflight lists open `FG-TODO` rows on the primary feature.
2. User picks or agent proposes the next todo; set `IN_PROGRESS` (one at a time by default).
3. On finish: `DONE` + evidence + `TODO_COMPLETED` event; or `CANCELLED` + reason.
4. Large scope: spawn a new feature file and close parent todo with spawn evidence.

Mirror open `FG-TODO` ids in Cursor TodoWrite when the user is working through a list.

## Memory update failure

If code succeeded but memory update failed: report failure, attempt safe repair, do not claim Feature Guardian completion until reconciled.

## Session checkpoint

Append to `SESSION CHECKPOINTS` and event history:

- changes made, requirements affected;
- tests run/passed/failed/not run;
- new/resolved issues and regressions;
- stale evidence, review-required features;
- files updated, validator result.

## Temporal questions memory must answer

- When did this begin failing?
- What changed immediately before?
- When was it last known healthy?
- Which solutions worked or failed before?
- Why was this decision made?
- What features were affected by this refactor?
- Why is this completed feature under review?

Design event history so these are answerable from immutable records plus current state sections.

## Cross-surface parity

Follow [PARITY.md](PARITY.md): maintain a lean card index; read it on related work; force investigation on STALE/FAIL or path intersection. Hash mismatch demotes OK → STALE and **blocks done** for touched contracts. Always tell the user what drifted and what was done; ask when the fix is ambiguous or needs a business decision. New features start UNKNOWN; migrate touched legacy records lazily.
