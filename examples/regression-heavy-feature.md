---
fg-schema: "0.1"
memory-revision: 28
feature-id: FG-FEAT-000003
name: Payments
slug: payments
aliases:
  - payment-processing
  - webhooks
status: REGRESSED
health: DEGRADED
confidence: HIGH
monitoring: ACTIVE
last-updated: "2026-09-04T20:00:00+01:00"
last-verified-commit: "9aa11bb"
---

# Payments

<!-- FG:FAST_CONTEXT:START -->
## FAST CONTEXT

> Process outbound payments and inbound provider webhooks with idempotency.

REGRESSED after FG-CHG-0041. Duplicate payment rows under concurrent webhook retries. Root cause confirmed: missing uniqueness constraint.
<!-- FG:FAST_CONTEXT:END -->

<!-- FG:CURRENT_STATE:START -->
## CURRENT STATE

**Status:** REGRESSED
**Health:** DEGRADED
**Confidence:** HIGH

Derived from:
- FG-REG-0004 OPEN
- FG-TEST-0022 FAIL

**Overall claim:** BROKEN for concurrent webhook idempotency; fix in progress (FG-CHG-0043)
<!-- FG:CURRENT_STATE:END -->

<!-- FG:ACTIVE_REGRESSIONS:START -->
## ACTIVE REGRESSIONS

### FG-REG-0004

Introduced by: FG-CHG-0041
First observed: 2026-09-03
Previously known-good baseline: commit 4f33a9c
Affected behavior: Single provider event must not create duplicate payment rows
Severity: HIGH
Test that detected it: FG-TEST-0022
Root cause: CONFIRMED — no database uniqueness/idempotency constraint on provider event ID
Why coverage missed it: No concurrent webhook test existed
Status: OPEN
Resolution: FG-CHG-0043 (in progress)
New regression coverage: FG-TEST-0036 (planned)
<!-- FG:ACTIVE_REGRESSIONS:END -->

<!-- FG:HISTORICAL_FAILED_APPROACHES:START -->
## HISTORICAL FAILED APPROACHES

### FG-FAIL-0001

Goal: Prevent duplicate payments on webhook retry
Approach: Frontend-only duplicate click guard (initially attempted in Payroll UI — lesson applied here)
Why reasonable: Fast to ship
Evidence/result: Duplicate rows under concurrent retries
Why failed: No server-side idempotency
What it taught: Client guards insufficient for financial webhooks
Do-not-repeat: Webhook idempotency without backend enforcement
Replacement: FG-DEC-0009 database uniqueness + status check
<!-- FG:HISTORICAL_FAILED_APPROACHES:END -->

<!-- FG:TEST_REGISTRY:START -->
## TEST REGISTRY

### FG-TEST-0022

Name: webhook idempotency concurrent
Type: INTEGRATION
Criticality: HIGH
Latest result: FAIL
Evidence freshness: FRESH
Historical sequence: PASS (4f33a9c) → FAIL (9aa11bb)

### FG-TEST-0036

Name: webhook concurrency regression
Type: INTEGRATION
Criticality: HIGH
Latest result: NOT RUN
Status: Added post-regression; pending FG-CHG-0043
<!-- FG:TEST_REGISTRY:END -->

<!-- FG:REVIEW_REQUIRED:START -->
## REVIEW REQUIRED

### Downstream: Payroll (FG-FEAT-000002)

Triggered by: FG-CHG-0041
Reason: Payment status contract changed during regression period
Required verification: FG-TEST-0021, FG-TEST-0022, FG-TEST-0027
Review result: PENDING (Payroll marked REVIEW_REQUIRED until Payments stabilizes)
<!-- FG:REVIEW_REQUIRED:END -->

<!-- FG:IMMUTABLE_EVENT_HISTORY:START -->
## IMMUTABLE EVENT HISTORY

### FG-EVT-000300

Type: TEST_PASSED
Timestamp: 2026-08-20T12:00:00+01:00
Summary: FG-TEST-0022 PASS at commit 4f33a9c.

### FG-EVT-000410

Type: REGRESSION_FOUND
Timestamp: 2026-09-03T11:00:00+01:00
Summary: FG-REG-0004 introduced by FG-CHG-0041. FG-TEST-0022 FAIL.

### FG-EVT-000411

Type: APPROACH_REJECTED
Timestamp: 2026-09-03T14:00:00+01:00
Summary: Confirmed root cause — missing DB constraint. Prior HYPOTHESIS: concurrent retries bypass status check.

### FG-EVT-000420

Type: IMPLEMENTATION_CHANGED
Timestamp: 2026-09-04T09:00:00+01:00
Summary: FG-CHG-0043 started — add uniqueness constraint and concurrency test FG-TEST-0036.
<!-- FG:IMMUTABLE_EVENT_HISTORY:END -->
