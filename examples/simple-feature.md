---
fg-schema: "0.1"
memory-revision: 3
feature-id: FG-FEAT-000099
name: Copy Invoice Number
slug: copy-invoice-number
aliases:
  - invoice-copy
status: COMPLETED
health: HEALTHY
confidence: HIGH
monitoring: DORMANT
last-updated: "2026-08-15T14:00:00+01:00"
last-verified-commit: "a1b2c3d"
---

# Copy Invoice Number

<!-- FG:FAST_CONTEXT:START -->
## FAST CONTEXT

> Users can copy the invoice number from the invoice detail header with one click.

Status: COMPLETED. Small UI feature with unit test coverage.
<!-- FG:FAST_CONTEXT:END -->

<!-- FG:FEATURE_CONSTITUTION:START -->
## FEATURE CONSTITUTION

### Core Goal
Let users copy invoice numbers without manual selection.

### Who It Serves
Business admins viewing invoices.

### Problems It Must Solve
- Reduce friction copying invoice IDs for support or reconciliation.

### Principles
- One-click action; visible confirmation.

### Non-Goals
- Bulk copy; export workflows.

### Success Definition
User taps copy; invoice number is on clipboard; toast confirms.
<!-- FG:FEATURE_CONSTITUTION:END -->

<!-- FG:CURRENT_STATE:START -->
## CURRENT STATE

**Status:** COMPLETED
**Health:** HEALTHY
**Confidence:** HIGH

**Implementation:** PRESENT (`components/invoice/InvoiceHeader.tsx`)
**Automated verification:** PASS (FG-TEST-000099)
**Overall claim:** VERIFIED for copy action in supported browsers
<!-- FG:CURRENT_STATE:END -->

<!-- FG:FEATURE_BOUNDARY:START -->
## FEATURE BOUNDARY

**In scope:** Copy button on invoice detail header.
**Out of scope:** PDF export, email sharing.
**Entry points:** `/invoices/[id]`
**Code locations:** `components/invoice/InvoiceHeader.tsx`
<!-- FG:FEATURE_BOUNDARY:END -->

<!-- FG:RELATED_FEATURES:START -->
## RELATED FEATURES

- **Depends On:** FG-FEAT-000050 (Invoice Detail View)
- **Feeds Into:** None recorded.
<!-- FG:RELATED_FEATURES:END -->

<!-- FG:REQUIREMENTS:START -->
## REQUIREMENTS

### FG-REQ-000099

Status: VERIFIED
Statement: User can copy invoice number with one click.

Maps to: `InvoiceHeader.tsx`, FG-TEST-000099
<!-- FG:REQUIREMENTS:END -->

<!-- FG:TEST_REGISTRY:START -->
## TEST REGISTRY

### FG-TEST-000099

Name: copy invoice number
Type: UNIT
Criticality: LOW
Behavior protected: Clipboard write on button click
Requirements protected: FG-REQ-000099
Implementation path: __tests__/invoice-copy.test.ts
Latest result: PASS
Evidence freshness: FRESH
Last run: 2026-08-15
Last verified commit: a1b2c3d
<!-- FG:TEST_REGISTRY:END -->

<!-- FG:IMMUTABLE_EVENT_HISTORY:START -->
## IMMUTABLE EVENT HISTORY

### FG-EVT-000099

Type: FEATURE_CREATED
Timestamp: 2026-08-10T10:00:00+01:00
Summary: Small feature memory created for copy invoice number.

### FG-EVT-000100

Type: TEST_PASSED
Timestamp: 2026-08-15T14:00:00+01:00
Summary: FG-TEST-000099 PASS at commit a1b2c3d.
<!-- FG:IMMUTABLE_EVENT_HISTORY:END -->
