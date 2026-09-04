# Testing and Evidence

## Evidence hierarchy

```text
Observed runtime behavior
        ↓
Executed tests and checks
        ↓
Actual implementation / configuration / schema
        ↓
Build / type / lint / static evidence
        ↓
Feature Guardian memory
        ↓
AI inference
        ↓
Assumption
```

## Claim states

Do not conflate:

- **IMPLEMENTED** — code exists
- **VERIFIED** — reliable evidence supports behavior
- **OBSERVED** — seen in runtime (specify environment)
- **STABLE** — verified and no known regressions
- **STALE** — prior proof insufficient after relevant change
- **UNKNOWN** — insufficient evidence
- **BROKEN** / **REGRESSED** — reliable failure evidence

Example overall claim:

```text
Implementation: PRESENT
Automated verification: PASS (18 tests)
Real provider verification: NOT PERFORMED
Overall: IMPLEMENTED, PARTIALLY VERIFIED
```

## Test types

`STATIC` · `TYPECHECK` · `LINT` · `UNIT` · `INTEGRATION` · `CONTRACT` · `E2E` · `SMOKE` · `MANUAL` · `RUNTIME_OBSERVATION` · `SECURITY` · `PERFORMANCE` · `MIGRATION`

Use the project's existing test stack. Do not impose Vitest/Jest/pytest if the repo uses something else.

## Default testing depth

| Level | When |
|---|---|
| 0 — Static | Docs-only, no runtime impact |
| 1 — Targeted | Directly relevant tests |
| **2 — Feature + related** | **Default for meaningful feature changes** |
| 3 — Broad | Auth core, payments, shared contracts, migrations |

Explain when full regression cannot run.

## Evidence freshness

`FRESH` · `STALE` · `UNKNOWN`

Stale when implementation, dependency, contract, config, schema, or environment changed since evidence was produced. Stale ≠ failed.

## Environment labels

`LOCAL` · `CI` · `TEST` · `STAGING` · `PRODUCTION` · `SANDBOX` · `UNKNOWN`

Never imply local pass proves production behavior.

## External services

Distinguish mocked/local from real sandbox/production observation. Record missing credentials as limitations. Never store secret values.

## Proof-of-fix protocol

```text
Reproduce failure → gather evidence → root cause or UNKNOWN
→ implement fix → show failure no longer reproduces
→ add regression coverage → run related tests → resolve
```

## Flaky tests

Alternating PASS/FAIL → `Test health: FLAKY`, `Evidence confidence: LOW`. Do not infer feature broken from flaky test alone.

## Test / regression debt

When coverage is missing:

```markdown
### FG-DEBT-0007
Type: REGRESSION_DEBT
Missing coverage: ...
Risk: MEDIUM
Status: OPEN
```

## Feature completion check

Never complete from implementation alone. Evaluate:

- requirements, implementation, critical paths;
- relevant + dependency tests;
- hard invariants, bugs, regressions;
- evidence freshness, critical unknowns;
- product alignment, migrations, security/privacy.

Outcomes: `VERIFIED_COMPLETE` · `COMPLETE_WITH_KNOWN_RISK` · `NOT_COMPLETE` · `BLOCKED`

Map to feature status appropriately. Example: implementation done but provider unobserved → `COMPLETE_WITH_KNOWN_RISK`, not `VERIFIED_COMPLETE`.

## Third-party limitations

Mocks passing without sandbox credentials → record limitation; no real-provider verification claim.
