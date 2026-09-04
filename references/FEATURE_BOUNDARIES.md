# Feature Boundaries

## What counts as a feature

A **feature** is a distinct piece of product behavior or capability — not merely a directory or file.

Track even small behaviors: copy button, dark mode, CSV export, table sort persistence.

Do not create fake features from folder structure alone.

## One feature, one file

All memory for a feature lives in `.feature-guardian/features/<slug>.md`.

Forbidden splits:

```text
payroll.md + payroll-tests.md + payroll-errors.md
```

Use internal sections and stable IDs instead.

## Discovery before creation

Search: canonical names, aliases, registry, related features, routes, tests.

Duplicate risk example: `payroll.md`, `monthly-pay.md`, `salary-processing.md` → likely one feature.

## Overlap and merge recommendation

Recommend merge when features substantially overlap in user goal, data model, services, workflow, tests, or product meaning.

**Do not merge automatically.** Explain overlap, benefits, risks, proposed canonical feature. Wait for explicit approval.

### Merge protocol (when approved)

1. Choose canonical surviving `FG-FEAT-...` ID.
2. Preserve former IDs as aliases/historical IDs.
3. Migrate requirements, tests, issues, decisions, regressions, dependencies, contracts, assumptions, unknowns, histories with provenance.
4. Update product registry and related feature references.
5. Append `FEATURE_MERGED` event.
6. Remove obsolete files only after safe preservation.
7. Validate memory.

## Split recommendation

Warn when one feature has mutated into independent domains:

- distinct user goals;
- separate critical paths;
- independent data ownership;
- excessive unrelated dependencies;
- repeated cross-domain regressions.

**Do not split automatically.**

### Split protocol (when approved)

1. Preserve original ID as historical parent if appropriate.
2. Create new feature IDs; migrate records with provenance.
3. Link relationships explicitly.
4. Update registry; append `FEATURE_SPLIT`; validate.

## Scope creep and mutation

Distinguish:

- **Scope expansion** — additional responsibilities.
- **Feature mutation** — practical identity materially changed.

Warn on drift; do not silently rewrite constitution.

## Small features

Concise files are fine. Still record: intent, location, requirement, test/evidence, relationships, current state.

Tracking depth scales with risk; tracking existence does not.

## Opt-out semantics

| User says | Action |
|---|---|
| Stop tracking this feature | `Monitoring: EXCLUDED`; keep memory |
| Never track this feature | Product-level exclusion + `EXCLUDED` |
| Delete history for this feature | Explicit authorization required; update registry |

Casual "ignore for now" ≠ permission to destroy history.
