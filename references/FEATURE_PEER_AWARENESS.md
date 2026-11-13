# Feature peer awareness

Features are **not assumed isolated**. Product behavior is a graph: shared libraries, contracts, and downstream flows mean a change in one feature can affect peers.

Two layers stay in sync:

| Layer | Location | Role |
|-------|----------|------|
| **Product graph** | `PRODUCT.md` → FEATURE RELATIONSHIP MAP, CROSS-FEATURE CONTRACTS | Global view, hubs, known non-dependencies |
| **Local peers** | Each `features/<slug>.md` → **RELATED FEATURES** | This feature’s depends-on, feeds-into, shared infra, conflicts |

If they disagree, reconcile toward evidence (code imports, webhooks, shared modules, docs). Update both when relationships change.

## Peer link types (RELATED FEATURES)

Use **slugs** (and `FG-FEAT-...` when helpful):

| Field | Meaning |
|-------|---------|
| **Depends On** | Upstream features or infra this feature requires to work |
| **Feeds Into** | Downstream features that consume this feature’s outputs or contracts |
| **Shares Infrastructure With** | Same jobs, DB collections, shared `lib/` modules, provider clients |
| **Potentially Mergeable With** | Boundary uncertainty only; not a runtime dependency |
| **Potentially Splittable Into** | Future split candidates |
| **Conflicts With** | Mutually exclusive approaches or product tensions |
| **Known Non-Dependencies** | Explicit “changes here do not affect X” (blast-radius negative knowledge) |

Truly standalone features are allowed. Say so explicitly:

```markdown
- **Peers:** None identified (standalone UI copy experiment).
- **Known Non-Dependencies:** payroll-payouts, payment-provider-integration
```

Empty “None recorded” on an active money or shared-infra feature is a **gap**, not proof of isolation.

## Automatic peer discovery (`infer_peers.py`)

After code inspection in a session (and before claiming done), reconcile peers:

```bash
python3 .cursor/skills/feature-guardian/scripts/infer_peers.py . --feature <slug>
python3 .cursor/skills/feature-guardian/scripts/infer_peers.py . --feature <slug> --apply
```

| Source | Confidence |
|--------|------------|
| TypeScript imports under feature paths | **OBSERVED** |
| PRODUCT relationship map | ASSUMED |
| FG-CONTRACT producer/consumer | ASSUMED |

`--apply` merges **gaps only** into **RELATED FEATURES** (never removes manual links). Then run `validate_memory.py` (reciprocal check **FG036**).

Batch backfill: `infer_peers.py . --all --apply` (review git diff).

## Preflight peer pass (mandatory with preflight)

After identifying the **primary feature** (step 2), before editing code:

```text
1. PRODUCT   — Read FEATURE RELATIONSHIP MAP + relevant FG-CONTRACT rows for the primary slug.
2. LOCAL     — Read primary feature RELATED FEATURES + DEPENDENCIES + CONTRACTS sections.
3. PEERS     — Build a short peer set:
               - Depends On (upstream)
               - Feeds Into (downstream)
               - Shares Infrastructure With
               - Contract producers/consumers from PRODUCT.md
4. COMPLETED — List downstream peers with status COMPLETED or monitoring DORMANT.
               Credible impact from your planned change → plan REVIEW_REQUIRED + tests.
5. SKIM      — For each peer in the peer set (cap ~5 unless user widens scope):
               read peer FAST CONTEXT + open ACTIVE ISSUES / ACTIVE REGRESSIONS only.
               Do not load full peer histories unless debugging cross-feature failure.
6. RECORD    — Include peer set in FG PREFLIGHT COMPLETE (see PREFLIGHT_PROTOCOL.md).
```

Hub features (e.g. shared payment normalization, auth, background jobs) widen the peer set automatically.

## During implementation

- Prefer changes that preserve **FG-CONTRACT** behavior or bump contract + all consumers in one plan.
- After editing shared code under `lib/`, `components/` used by multiple domains, or provider/webhook paths: re-run blast-radius from [IMPACT_AND_REVIEW.md](IMPACT_AND_REVIEW.md).
- Append **BLAST RADIUS** notes on meaningful `FG-CHG-...` entries when peers are affected.
- Update **RELATED FEATURES** on primary and affected peers when you discover a new dependency.

## When creating or splitting features

1. Add registry row in `PRODUCT.md`.
2. Update FEATURE RELATIONSHIP MAP (one line or edge).
3. Fill RELATED FEATURES on the new feature **and** update peers’ Feeds Into / Depends On reciprocally where true.
4. Add or extend **FG-CONTRACT-...** when a stable interface spans features.

## Reporting

User checkpoints should mention peers when relevant:

```text
Peers considered: payment-provider-integration → payroll-payouts, quick-transfers (DOWNSTREAM, HIGH)
Completed features flagged for review: payroll-payouts (REVIEW_REQUIRED after FG-CHG-…)
```

## Relationship to todos and review

- `FG-TODO` work on a feature still runs the **peer pass** if the todo touches shared code or contracts.
- `REVIEW_REQUIRED` on a completed **peer** is how isolation failures are caught; see completed-feature review in IMPACT_AND_REVIEW.md.
