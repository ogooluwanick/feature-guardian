# Preflight Protocol

Mandatory ordering before product code changes when `.feature-guardian/` exists. This is the v0.1.1+ activation layer; blind-test evidence showed implementation-first paths bypass memory unless preflight is explicit.

## Behavioral gates

| Gate | Rule |
|------|------|
| **A** | No product-code modification before FG preflight completes. |
| **B** | No implementation decision on risky changes before failed approaches, active issues, and hard invariants are checked in feature memory. |
| **C** | No completion claim before affected completed features are reconciled (`REVIEW_REQUIRED` where required). |
| **D** | No historical claim in the user report unless it was retrieved from authoritative feature memory this session. |

## Preflight steps

Run in order. Do not open implementation files for editing until step 6 passes.

```text
1. EXISTS     — `.feature-guardian/PRODUCT.md` present? If no, bootstrap or skip FG (tooling-only tasks).
2. REGISTRY   — Identify primary owning feature (slug) from user intent, paths, APIs, registry, aliases.
3. RELATED    — **Peer graph:** PRODUCT.md FEATURE RELATIONSHIP MAP + CROSS-FEATURE CONTRACTS;
                primary feature RELATED FEATURES, DEPENDENCIES, CONTRACTS.
                List upstream, downstream, and shared-infra peers (see FEATURE_PEER_AWARENESS.md).
4. PEERS      — Skim peer FAST CONTEXT (+ open issues/regressions) for the peer set (~5 cap default).
                Note COMPLETED downstream peers at risk from the planned change.
5. ACTIVE     — Read primary feature: FAST CONTEXT, CURRENT STATE, **ACTIVE WORK** (open FG-TODO ids),
                INVARIANTS, ACTIVE ISSUES, ACTIVE REGRESSIONS, TEST SUMMARY.
6. HISTORY    — Search that feature's history for terms from the user request (status names, flows,
                rejected approaches). Load FG-FAIL-* / FG-DEC-* only when relevant.
7. DEPENDENTS — For shared helpers, contracts, or payment/auth paths: note completed dependents
                that may need REVIEW_REQUIRED after the change.
8. PARITY     — Read the owning parity **card index** (missing = UNKNOWN). Note STALE/FAIL items and whether
                the task intersects provider/`check_here` paths. Escalate investigation only then (PARITY.md).
9. MARKER     — Emit internal checkpoint (see below), then inspect code and tests.
```

## Internal checkpoint (for testing and self-audit)

After preflight, record privately before editing product code:

```text
FG PREFLIGHT COMPLETE
Primary feature: <slug>
Peer features: <slug> (upstream|downstream|shared) — or standalone (explicit)
Completed peers at risk: <slug> | none
Related features: <slug>, ...
Historical matches: <FG-FAIL-...> | none
Completed dependents at risk: <slug> | none
Active todos: <FG-TODO-... statuses> | none
Parity: <card ids; OK|STALE|FAIL|UNKNOWN; path intersection yes/no; escalate yes/no>
Companion: unlazy=<solo|orchestrated|exempt> council=<yes|no> taste=<yes|no>
```

Do not spam the user with this block every turn; use it when work is substantial or when verifying activation in dogfood.

## After preflight

Follow [OPERATING_PROTOCOL.md](OPERATING_PROTOCOL.md) from code inspection through memory reconciliation.

## Exemptions

- Pure conversation, definitions, or read-only questions with no artifact.
- User excluded feature (`Monitoring: EXCLUDED`).
- Changes confined to `feature-guardian-evaluation/` or the FG package outside product repos.

## Failure mode (dogfood)

If the agent refactors or ships behavior before steps 1–6, activation failed regardless of later memory updates.
