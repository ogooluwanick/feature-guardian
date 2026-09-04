---
fg-schema: "0.1"
memory-revision: 47
feature-id: FG-FEAT-000002
name: Payroll
slug: payroll
aliases:
  - salary-processing
  - monthly-payroll
  - pay-run
status: IN_DEVELOPMENT
health: DEGRADED
confidence: MEDIUM
monitoring: ACTIVE
last-updated: "2026-09-04T18:30:00+01:00"
last-verified-commit: "4f33a9c"
---

# Payroll

<!-- FG:FAST_CONTEXT:START -->
## FAST CONTEXT

> Run monthly payroll: calculate pay, approve pay runs, disburse via Payments, deliver payslips.

Currently IN_DEVELOPMENT. Payment idempotency work in progress. Health DEGRADED due to open issue FG-ISSUE-0007.
<!-- FG:FAST_CONTEXT:END -->

<!-- FG:FEATURE_CONSTITUTION:START -->
## FEATURE CONSTITUTION

### Core Goal
Allow small businesses to run payroll simply without payroll expertise.

### Who It Serves
Small-business administrators.

### Problems It Must Solve
- calculate employee pay;
- approve a pay run;
- issue payments;
- provide payslips.

### Principles
- minimize manual configuration;
- make common workflows obvious;
- automate calculations when safe.

### Non-Goals
- full accounting suite;
- enterprise custom payroll engine.

### Success Definition
Admin completes pay run end-to-end with verified payment and payslip delivery.
<!-- FG:FEATURE_CONSTITUTION:END -->

<!-- FG:CURRENT_STATE:START -->
## CURRENT STATE

**Status:** IN_DEVELOPMENT
**Health:** DEGRADED
**Confidence:** MEDIUM

Derived from:
- FG-ISSUE-0007 OPEN (MEDIUM)
- FG-TEST-0021 PASS but Freshness: STALE after PaymentService change

**Implementation:** PRESENT (core flows)
**Automated verification:** PARTIAL
**Overall claim:** IMPLEMENTED, PARTIALLY VERIFIED
<!-- FG:CURRENT_STATE:END -->

<!-- FG:INVARIANTS:START -->
## INVARIANTS

### FG-INV-0008

Category: FINANCIAL
Strength: HARD

Invariant:
A payroll entry must never be paid twice.

Protected by:
- FG-TEST-0041
- FG-TEST-0049

Related requirements:
- FG-REQ-0021
<!-- FG:INVARIANTS:END -->

<!-- FG:DEPENDENCIES:START -->
## DEPENDENCIES

### FG-DEP-0031

Target: Payments (FG-FEAT-000003)
Type: RUNTIME
Direction: Payroll → Payments
Criticality: HIGH
Contract: Payroll sends approved payment instructions.
Failure effect: Payroll can calculate but cannot disburse funds.
<!-- FG:DEPENDENCIES:END -->

<!-- FG:TEST_REGISTRY:START -->
## TEST REGISTRY

### FG-TEST-0021

Name: pay run finalizes on payment success
Type: INTEGRATION
Criticality: HIGH
Behavior protected: Pay run completes when payment status succeeds
Requirements protected: FG-REQ-0015
Latest result: PASS
Evidence freshness: STALE
Last verified commit: 4f33a9c
Note: PaymentService contract changed in FG-CHG-0041 after last pass.

### FG-TEST-0041

Name: duplicate payment prevention
Type: INTEGRATION
Criticality: HIGH
Behavior protected: FG-INV-0008
Latest result: PASS
Evidence freshness: FRESH
<!-- FG:TEST_REGISTRY:END -->

<!-- FG:ACTIVE_ISSUES:START -->
## ACTIVE ISSUES

### FG-ISSUE-0007

Severity: MEDIUM
Status: OPEN
Summary: Payslip PDF missing tax breakdown for some employees.
<!-- FG:ACTIVE_ISSUES:END -->

<!-- FG:ENGINEERING_DECISIONS:START -->
## ENGINEERING DECISIONS

### FG-DEC-0009

Status: ACTIVE
Decision: Use database-level idempotency for payment webhook processing.
Why: Frontend-only guard failed (see failed approach FG-FAIL-0001).
Affected invariants: FG-INV-0008
<!-- FG:ENGINEERING_DECISIONS:END -->

<!-- FG:RELEASE_VERIFICATION_BASELINES:START -->
## RELEASE / VERIFICATION BASELINES

- v1.8.0 — VERIFIED
- v1.9.0 — VERIFIED
<!-- FG:RELEASE_VERIFICATION_BASELINES:END -->

<!-- FG:IMMUTABLE_EVENT_HISTORY:START -->
## IMMUTABLE EVENT HISTORY

### FG-EVT-000002

Type: FEATURE_CREATED
Timestamp: 2026-01-10T09:00:00+00:00
Summary: Payroll feature memory established.

### FG-EVT-000450

Type: REVIEW_REQUIRED
Timestamp: 2026-09-04T16:00:00+01:00
Summary: Triggered by FG-CHG-0041 PaymentService contract change. Later re-verified FG-TEST-0021 pending.
<!-- FG:IMMUTABLE_EVENT_HISTORY:END -->
