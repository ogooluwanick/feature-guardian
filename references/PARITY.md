# Cross-surface parity (lean index)

Parity stops silent drift across providers and consumers. Prefer a **cheap index** every related turn, and **forced investigation** only when the index says STALE/FAIL or the task touches listed paths.

## Goals

- High assurance that listed contracts did not silently diverge.
- Low token use: read the card; do not re-discover the whole repo each turn.
- User visibility: always report discovered drifts and what was done; ask when the fix is not obvious or needs a business decision.

## Parity card (default)

Keep a short indexed list under `FG:PARITY` in the owning feature file. Prefer **schema_version 2**:

```json
{
  "schema_version": 2,
  "items": [
    {
      "id": "invoice-status-labels",
      "contract": "Invoice status labels match the canonical API enum",
      "provider": "lib/invoicing/status.ts",
      "check_here": [
        "components/invoices/InvoiceStatusBadge.tsx",
        "__tests__/lib/invoicing/status.test.ts"
      ],
      "intentional_diffs": "none",
      "prove_with": "__tests__/lib/invoicing/status.test.ts",
      "status": "UNKNOWN",
      "source_hashes": {},
      "evidence": []
    }
  ]
}
```

| Field | Purpose |
|-------|---------|
| `contract` | One-sentence shared fact |
| `provider` | Canonical path |
| `check_here` | 2–5 paths/tests to open when this contract is in play |
| `intentional_diffs` | Known allowed differences, or `none` |
| `prove_with` | Where deeper proof lives (test path or evidence id); metadata only |
| `status` | `OK` / `STALE` / `UNKNOWN` / `FAIL` / `NOT_APPLICABLE` |
| `source_hashes` | SHA-256 of provider + every `check_here` path after verification |

Schema 1 unit manifests remain valid for legacy records. New work should use schema 2 cards. Optional deep unit detail belongs in linked evidence or tests, not in the hot path.

## Forced rules (non-negotiable)

1. **Preflight:** read the parity index for the primary feature (missing = UNKNOWN). Do not invent a clean slate.
2. **Related prompt:** if the task intersects a card’s `provider` or `check_here`, open those paths. No random whole-repo search unless a card is missing and you must add one.
3. **Hash gate:** when status is `OK`/`PASS` and any listed hash no longer matches disk, the checker **demotes to STALE**.
4. **STALE/FAIL blocks done** for the affected feature task. Run `check_parity.py --feature <slug> --check`. Do not claim completion, VERIFIED, or “parity fine” while `blocks_done` is true for contracts you touched.
5. **Clear STALE only with proof:** open check-here paths, fix or confirm intentional diff, run the decisive product test(s), refresh hashes, attach FRESH evidence, set `OK`.
6. **User report (mandatory when drift appears):** tell the user what drifted, what you changed, and what remains. Use the checker’s drift list.
7. **Ask the user** when the fix is not obvious, or when a product/business/privacy choice is required. Do not invent the decision. Record the answer as `FG-DEC-...` when durable.
8. **Money / auth / public surfaces:** on touch, require fresh check evidence even if hashes still match, when the change alters meaning or visibility.
9. **Grow the index when you miss:** if you find an unlisted consumer that should share the contract, add it to `check_here` once. That is how assurance climbs without scanning everything every turn.

Unrelated documented debt does not authorize a product-wide refactor or block unrelated work, but it also does not authorize claiming full parity.

## Claims

`parity-claim: UNKNOWN` (default), `PARTIAL`, or `VERIFIED`.

- `VERIFIED` only when the checker status is `PASS` (all applicable items OK/PASS, hashes current, evidence present).
- Empty inventory is never 100% parity.

## Commands

```sh
python3 <skill>/scripts/check_parity.py . --feature <slug>
python3 <skill>/scripts/check_parity.py . --feature <slug> --check
python3 <skill>/scripts/check_parity.py . --feature <slug> --report
python3 <skill>/scripts/validate_memory.py .
```

The checker reads manifests and hashes only; it does not run product tests. `--check` fails on errors or non-PASS / `blocks_done`. `--report` prints a human drift summary on stderr.

## Lifecycle

- **Preflight:** read cards; note STALE/FAIL/UNKNOWN; list path intersections with the task.
- **During work:** update provider and check-here together within scope; mark STALE when sources change before proof is refreshed.
- **On confirmed drift:** fix if mechanical and safe; otherwise stop and ask the user.
- **Completion:** run scoped product tests + `check_parity.py --feature <slug> --check`; report drifts and remediations to the user; leave unresolved items as STALE/FAIL/FG-TODO, never silent.

## User-facing drift message (required shape)

```text
Parity drift:
- [STALE|FAIL] <id>: <contract>
  Provider: <path>
  Check here: <paths>
  What changed: ...
  What I did: ... | waiting on your decision: ...
```

Ask explicitly when a fundamental or business choice is needed before continuing.
