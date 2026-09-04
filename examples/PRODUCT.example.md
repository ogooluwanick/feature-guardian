---
fg-schema: "0.1"
memory-revision: 5
product-id: FG-PROD-000001
name: Acme Payroll (Example)
created-at: "2026-01-01T00:00:00+00:00"
last-updated: "2026-09-04T18:00:00+01:00"
---

# PRODUCT MEMORY (Example)

## IDENTITY

- **Product:** Acme Payroll
- **Feature Guardian schema:** 0.1

## FAST CONTEXT

> SaaS payroll for small businesses: staff, pay runs, payments, payslips.

## PRODUCT VISION

Make payroll approachable for teams without dedicated HR/payroll staff.

## PRODUCT PRINCIPLES

- Clarity over feature bloat
- Financial correctness over speed of shipping
- Evidence before "done"

## FEATURE REGISTRY

| Feature ID | Feature | Status | Health | Confidence | Monitoring | Last Verified |
|---|---|---|---|---|---|---|
| FG-FEAT-000001 | Authentication | COMPLETED | HEALTHY | HIGH | DORMANT | 2026-09-01 |
| FG-FEAT-000002 | Payroll | IN_DEVELOPMENT | DEGRADED | MEDIUM | ACTIVE | 2026-09-04 |
| FG-FEAT-000003 | Payments | REGRESSED | DEGRADED | HIGH | ACTIVE | 2026-09-04 |
| FG-FEAT-000099 | Copy Invoice Number | COMPLETED | HEALTHY | HIGH | DORMANT | 2026-08-15 |

## FEATURE RELATIONSHIP MAP

```text
Authentication → Payroll → Payments
Payroll → Payslips
Invoice Detail → Copy Invoice Number
Payments — webhook events → (future) Staff Notifications
Dark Mode — no runtime dependency on Payments or Payroll
```

## CROSS-FEATURE CONTRACTS

### FG-CONTRACT-0001

Producer: Payments
Consumer: Payroll
Shape: Payment status enum + provider reference ID
Protected tests: FG-TEST-0021, FG-TEST-0022

## CURRENT PRODUCT HEALTH

```text
Features: 4
Completed: 2
In development: 1
Regressed: 1
Review required: 0

Critical concerns:
- Payments regression FG-REG-0004
- Payroll evidence stale after PaymentService change
```

## PRODUCT EVENT HISTORY

<!-- FG:PRODUCT_EVENT_HISTORY:START -->
### FG-EVT-000001

Type: PRODUCT_MEMORY_CREATED
Timestamp: 2026-01-01T00:00:00+00:00
Summary: Example product memory for Feature Guardian documentation.
<!-- FG:PRODUCT_EVENT_HISTORY:END -->
