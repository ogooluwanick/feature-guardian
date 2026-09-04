# Behavior Scenarios (Acceptance Suite)

Acceptance tests for Feature Guardian **skill behavior** (v0.1). These scenarios define expected agent conduct; they are validated by review and future automation, not solely by `validate_memory.py`.

## Scenario 1 — New tiny feature

**User:** "Add a copy button beside invoice number."

**Expected:**
- Distinct feature tracked (`copy-invoice-number` or equivalent).
- Concise feature memory created from template.
- Relevant test/evidence recorded.
- `PRODUCT.md` registry updated.
- No unnecessary architecture ceremony.

## Scenario 2 — Existing feature discovered

**User:** "Fix password reset."

**Expected:**
- Guardian identifies existing feature via alias/registry (`forgot-password`, etc.).
- Reads memory; does not create duplicate feature file.

## Scenario 3 — Previous failed approach

**Memory:** Frontend-only duplicate prevention failed.

**Expected:**
- Agent does not repeat approach without new evidence/reason.
- Consults `HISTORICAL FAILED APPROACHES`.

## Scenario 4 — Completed feature affected

**Change:** Shared payment service contract changes.

**Expected:**
- Completed Payroll dependency detected.
- Payroll → `REVIEW_REQUIRED`, `ACTIVE_REVIEW`.
- Required tests listed (`FG-TEST-...`).
- After pass → restore `COMPLETED`, `DORMANT`.

## Scenario 5 — Regression

**Change:** Previously passing behavior now fails with reliable evidence.

**Expected:**
- Status → `REGRESSED`.
- Prior success retained in history.
- `FG-REG-...` created with lineage.

## Scenario 6 — Memory contradicts tests

**State:** Memory says working; latest reliable test fails.

**Expected:**
- Evidence wins.
- `CONTRADICTION_FOUND` recorded.
- Current state downgraded.

## Scenario 7 — Missing coverage

**State:** HARD invariant has no test.

**Expected:**
- Test created when feasible, or `FG-DEBT-...` recorded.

## Scenario 8 — Third-party limitation

**State:** Mocks pass; no sandbox credentials.

**Expected:**
- No claim of real-provider verification.
- Limitation recorded in evidence.

## Scenario 9 — Feature-direction conflict

**Request:** Strongly contradicts feature constitution.

**Expected:**
- Conflict explained (`STRONG_CONFLICT`).
- Constitution not silently rewritten.

## Scenario 10 — Similar features

**State:** Two feature files substantially overlap.

**Expected:**
- Merge recommendation with rationale.
- No automatic merge.

## Scenario 11 — Feature becomes oversized

**State:** One feature spans independent domains.

**Expected:**
- Split recommendation.
- No automatic split.

## Scenario 12 — Multi-feature bug

**Issue:** Affects payroll, invoices, subscriptions.

**Expected:**
- Single `FG-ISSUE-...`.
- Per-feature impact in each feature file.

## Scenario 13 — Stale evidence

**State:** Implementation changed after test pass.

**Expected:**
- Evidence freshness → `STALE`.
- Completed features → `REVIEW_REQUIRED` when credible.

## Scenario 14 — Flaky test

**History:** PASS → FAIL → PASS → FAIL.

**Expected:**
- Test marked `FLAKY`.
- Feature failure not inferred from flaky test alone.

## Scenario 15 — Unknown root cause

**State:** Hypotheses only, no proof.

**Expected:**
- `Root cause: UNKNOWN`.

## Scenario 16 — Git branch disagreement

**State:** Branch A PASS, Branch B FAIL for same test.

**Expected:**
- Both preserved with branch/commit context.
- Post-merge reverification; current state updated.

## Scenario 17 — User exclusion

**User:** "Stop tracking this feature."

**Expected:**
- `Monitoring: EXCLUDED`.
- History preserved unless deletion explicitly requested.

## Scenario 18 — Product-level invariant

**Change:** Could violate tenant isolation.

**Expected:**
- `INVARIANT_VIOLATION`; blocking conflict.

## Scenario 19 — Architecture drift

**State:** Code bypasses documented service boundary.

**Expected:**
- Drift recorded with severity.
- No automatic refactor without justification.

## Scenario 20 — Feature completion

**State:** Implementation done; dependency evidence stale.

**Expected:**
- No `VERIFIED_COMPLETE` claim.
- `COMPLETE_WITH_KNOWN_RISK` or `NOT_COMPLETE` as appropriate.
