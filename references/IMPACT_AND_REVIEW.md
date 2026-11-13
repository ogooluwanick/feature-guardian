# Impact and Review

## Blast-radius protocol

For every meaningful change, answer (after [FEATURE_PEER_AWARENESS.md](FEATURE_PEER_AWARENESS.md) peer pass):

1. What changed directly?
2. What behavior depends on it?
3. What related features depend on it?
4. What contracts may have changed?
5. What tests protect those behaviors?
6. What remains untested?
7. Which completed features now require review?

## Impact classification

`DIRECT` · `DOWNSTREAM` · `SHARED_INFRASTRUCTURE` · `CONTRACT` · `CONFIGURATION` · `SCHEMA` · `POSSIBLE` · `NONE`

Confidence: `CERTAIN` · `HIGH` · `MEDIUM` · `LOW`

Example:

```markdown
## BLAST RADIUS — FG-CHG-0041

Changed: src/payments/webhook.ts

Affected:
- Payments — DIRECT — CERTAIN
- Payroll — DOWNSTREAM — HIGH
- Subscriptions — DOWNSTREAM — MEDIUM
- Dark Mode — NONE — CERTAIN
```

Low-confidence relationships are candidates, not automatic review triggers for every feature.

## Negative knowledge

Record known non-dependencies:

```markdown
### KNOWN NON-DEPENDENCY
Dark Mode does not affect payroll calculations or payment processing.
```

## Completed-feature review protocol

When credible impact affects a completed feature:

1. `Status: REVIEW_REQUIRED`
2. `Monitoring: ACTIVE_REVIEW`
3. Record trigger `FG-CHG-...` and reason
4. List required verification (specific `FG-TEST-...` IDs)
5. Preserve previous completion evidence
6. Do **not** call broken unless evidence shows regression

After verification:

| Result | Status | Monitoring |
|---|---|---|
| Healthy | COMPLETED | DORMANT |
| Broken | REGRESSED | ACTIVE |

Append `REVIEW_PASSED` or `REVIEW_FAILED` event.

## Contracts

Track: Contract ID, producer, consumer, shape/behavior, compatibility, protected tests, last verified.

Contract change → all consumers are blast-radius candidates → completed consumers with credible impact → `REVIEW_REQUIRED`.

## Risk model

`LOW` · `MEDIUM` · `HIGH` · `CRITICAL`

Controls: test depth, blast-radius breadth, completion requirements, warning strength, human confirmation.

## Architecture drift

Compare documented vs observed architecture. Severity: `INFORMATION` · `WARNING` · `CONCERN` · `BLOCKING`.

Do not refactor architecture merely because drift exists.

## Regression sources

Classify: `CODE` · `CONFIGURATION` · `SCHEMA` · `DATA` · `INFRASTRUCTURE` · `EXTERNAL_SERVICE` · `DEPENDENCY_VERSION` · `ENVIRONMENT` · `UNKNOWN`

## Release baselines (optional)

```text
v1.8.0 — VERIFIED
v2.0.0 — REVIEW_REQUIRED
```

Before release, surface: changed features, stale evidence, open regressions, review-required features, critical unknowns.
