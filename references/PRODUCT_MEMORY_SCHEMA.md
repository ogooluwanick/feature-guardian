# Product Memory Schema

Single product file: `.feature-guardian/PRODUCT.md`.

## Frontmatter (recommended)

```yaml
---
fg-schema: "0.1"
memory-revision: 1
product-id: FG-PROD-000001
name: Product Name
created-at: "2026-09-04T12:00:00+01:00"
last-updated: "2026-09-04T12:00:00+01:00"
---
```

## Required sections

| Section | Purpose |
|---|---|
| IDENTITY | Product name, schema version |
| FAST CONTEXT | One-paragraph product summary |
| PRODUCT VISION | Why the product exists |
| CORE PROBLEM | Problem being solved |
| TARGET USERS | Primary audiences |
| PRODUCT PRINCIPLES | Non-negotiable product values |
| PRODUCT NON-GOALS | Explicit exclusions |
| PRODUCT-LEVEL INVARIANTS | Cross-feature rules |
| SECURITY / PRIVACY INVARIANTS | Tenant isolation, auth boundaries |
| PRODUCT ARCHITECTURE | Expected high-level shape |
| FEATURE REGISTRY | Index of all features (authoritative list) |
| FEATURE RELATIONSHIP MAP | Product graph, not flat list |
| CROSS-FEATURE CONTRACTS | Shared interfaces |
| PRODUCT DECISIONS | Product-level choices |
| PRODUCT RISKS | Ongoing product risks |
| PRODUCT ASSUMPTIONS | Product-level assumptions |
| PRODUCT UNKNOWNS | Legitimate unknowns |
| ARCHITECTURE DRIFT | Documented vs observed architecture |
| RELEASE BASELINES | Optional release verification |
| ACTIVE PRODUCT CONFLICTS | Cross-feature conflicts |
| CURRENT PRODUCT HEALTH | Evidence-based summary |
| PRODUCT EVENT HISTORY | Append-only product events |

## Feature registry (v0.1)

Lives inside `PRODUCT.md`. The registry is an **index**; feature files are authoritative for detail.

```markdown
| Feature ID | Feature | Status | Health | Confidence | Monitoring | Last Verified |
|---|---|---|---|---|---|---|
| FG-FEAT-000001 | Authentication | COMPLETED | HEALTHY | HIGH | DORMANT | 2026-09-01 |
| FG-FEAT-000002 | Payroll | IN_DEVELOPMENT | DEGRADED | MEDIUM | ACTIVE | 2026-09-04 |
```

Rules:

- Every feature file must have a registry row.
- Every registry row must point to an existing feature file.
- Feature ID in registry must match feature file frontmatter.
- Update registry when status/health/monitoring changes.

## Relationship map

Model dependencies as a graph:

```text
Authentication → Payroll → Payments
Staff Notifications ← Payments (events)
Dark Mode — (no runtime dependency on Payments)
```

Record known non-dependencies to prevent blast-radius inflation.

## Product health summary

Evidence-based counts, not invented scores:

```text
Features: 43
Completed: 28
Review required: 4
Regressed: 2
Critical concerns:
- Authentication review required
- Payment regression FG-REG-0019
```

## Product decisions

Same states as feature decisions: `ACTIVE`, `EXPERIMENTAL`, `SUPERSEDED`, `REVERSED`.

Record: decision, why, alternatives, evidence, affected features/invariants, date, supersedes.

Template: [assets/PRODUCT_TEMPLATE.md](../assets/PRODUCT_TEMPLATE.md)
