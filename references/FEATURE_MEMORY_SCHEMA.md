# Feature Memory Schema

One feature = one file: `.feature-guardian/features/<slug>.md`.

Identity is `feature-id` in frontmatter, not the filename. Filename should match `slug`.

## Frontmatter (required)

```yaml
---
fg-schema: "0.1"
memory-revision: <integer>
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

## Two logical layers

1. **Active/current state** — sections 1–27 (mutable, reconciled from events).
2. **Immutable engineering history** — events in `IMMUTABLE EVENT HISTORY` (append-only).

## Canonical section order

Use HTML markers for machine-updatable sections:

1. FAST CONTEXT — `<!-- FG:FAST_CONTEXT:START/END -->`
2. FEATURE CONSTITUTION — `<!-- FG:FEATURE_CONSTITUTION:START/END -->`
3. CURRENT STATE — `<!-- FG:CURRENT_STATE:START/END -->`
4. FEATURE BOUNDARY
5. RELATED FEATURES
6. REQUIREMENTS
7. CRITICAL PATHS
8. INVARIANTS
9. ARCHITECTURE
10. DEPENDENCIES
11. CONTRACTS
12. ACTIVE WORK — feature todos (`FG-TODO-...`); see [FEATURE_TODOS.md](FEATURE_TODOS.md)
13. TEST SUMMARY
14. TEST REGISTRY
15. EVIDENCE REGISTRY
16. TEST / REGRESSION DEBT
17. ACTIVE ISSUES
18. ACTIVE REGRESSIONS
19. ACTIVE RISKS
20. ACTIVE ASSUMPTIONS
21. UNKNOWNS
22. ENGINEERING DECISIONS
23. PRODUCT DECISIONS
24. REVIEW REQUIRED
25. CONTRADICTIONS
26. ARCHITECTURE / BEHAVIOR DRIFT
27. RELEASE / VERIFICATION BASELINES
28. HISTORICAL FAILED APPROACHES
29. ROLLBACKS
30. SESSION CHECKPOINTS
31. IMMUTABLE EVENT HISTORY

Empty sections: `None recorded` or concise placeholder. No verbose filler.

## Constitution (changes deliberately)

Required fields: Core Goal, Who It Serves, Problems It Must Solve, Principles, Non-Goals, Success Definition.

Constitution changes require explicit user direction (unless already stated). Append `CONSTITUTION_CHANGED` event; preserve former direction in history.

## Requirement entry example

```markdown
### FG-REQ-000123

Status: ACCEPTED
Statement: User can copy invoice number with one click.

Maps to:
- Implementation: `components/invoice/InvoiceHeader.tsx`
- Tests: FG-TEST-000041
- Invariants: —
```

## Invariant entry example

```markdown
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
```

Strengths: `GUIDANCE` · `STRONG` · `HARD`

## Test registry entry

```markdown
### FG-TEST-000041

Name: copy-invoice-number unit test
Type: UNIT
Criticality: LOW
Behavior protected: Copy action writes invoice number to clipboard
Requirements protected: FG-REQ-000123
Implementation path: __tests__/invoice-copy.test.ts
Latest result: PASS
Evidence freshness: FRESH
Last run: 2026-09-04
Last verified commit: abc1234
```

## Evidence entry

```markdown
### FG-EVID-000012

Type: UNIT
Claim supported: Copy button works in isolation
Environment: LOCAL
Result: PASS
Timestamp: 2026-09-04T10:00:00+01:00
Commit: abc1234
Strength: UNIT
Freshness: FRESH
Limitations: Clipboard API not exercised in CI headless environment
```

## Failed approach entry

```markdown
### FG-FAIL-000003 (record under HISTORICAL FAILED APPROACHES)

Goal: Prevent duplicate payments
Approach: Frontend-only duplicate click guard
Why reasonable: Fast to ship
Evidence/result: Duplicate rows still created under retry
Why failed: No server-side idempotency
What it taught: Client guards are insufficient for financial flows
Do-not-repeat: Financial idempotency without backend enforcement
Replacement: Database uniqueness + webhook idempotency (FG-DEC-0009)
```

## Review required entry

```markdown
Triggered by: FG-CHG-0041
Reason: PaymentService status contract changed
Potential impact: Payroll finalization reads payment status
Required verification:
- FG-TEST-0021
- FG-TEST-0022
Review result: PENDING
```

Template: [assets/FEATURE_TEMPLATE.md](../assets/FEATURE_TEMPLATE.md)

## Parity (additive, backward compatible)

New feature templates include `parity-claim: UNKNOWN` and a `FG:PARITY` lean **card index** (schema 2) between CONTRACTS and ACTIVE WORK. Schema 1 unit manifests remain valid. Existing records without parity have UNKNOWN status; migrate on relevant work. Hash STALE/FAIL blocks done for touched contracts; agents must report drifts to the user and ask when decisions are required. Details: [PARITY.md](PARITY.md).
