# Feature todos

Feature-scoped work queue inside each feature file. **Not** a company-wide task manager or Jira replacement.

## Purpose

- Track **what is left to build, fix, or verify** for one feature across sessions.
- Survive chat restarts (unlike Cursor session todos alone).
- Link work to requirements, tests, and evidence.
- Stay small: actionable items with IDs, not an unbounded backlog.

## Where todos live

Section **ACTIVE WORK** in `.feature-guardian/features/<slug>.md`:

```markdown
<!-- FG:ACTIVE_WORK:START -->
## ACTIVE WORK

### FG-TODO-000042

Title: Add regression test for concurrent quote conversion
Status: OPEN
Priority: HIGH
Added: 2026-11-04
Maps to: FG-REQ-..., C10 in ENGINEERING-STATUS
Acceptance: Mongo integration proves single winner under parallel accept

### FG-TODO-000043

Title: Reconcile report cohort filter with API
Status: IN_PROGRESS
Priority: MEDIUM
Added: 2026-11-03
Started: 2026-11-04
Maps to: FG-REQ-...
<!-- FG:ACTIVE_WORK:END -->
```

## ID prefix

`FG-TODO-######` — same six-digit discipline as other FG ids. Never reuse.

## Status

| Status | Meaning |
|--------|---------|
| `OPEN` | Not started |
| `IN_PROGRESS` | Current session or owner actively working |
| `BLOCKED` | Waiting on dependency, user, or external |
| `DONE` | Completed with evidence |
| `CANCELLED` | No longer needed; reason required |

At most **one** `IN_PROGRESS` per feature unless user explicitly parallelizes.

## When to create a todo

- User asks to track follow-ups on a feature.
- Agent splits a multi-step feature task into durable steps.
- Closure plan items (e.g. C01–C12) worth tracking in FG should become `FG-TODO` rows (optional link to external plan ids in **Maps to**).
- `FG-DEBT` covers missing tests; use `FG-TODO` for general engineering work (UI, API, docs, migration steps).

## When **not** to create a todo

- One-shot steps finished in the same session with a `FG-CHG` record.
- Generic housekeeping unrelated to the feature boundary.
- Duplicating every line of an external plan; summarize or link instead.

## Completion

Mark `DONE` only with:

- `Completed:` date
- `Evidence:` test run, `FG-CHG-...`, commit scope, or manual verification note
- Append immutable event: `TODO_COMPLETED` with `FG-TODO-...`

Do not mark `DONE` from intent alone.

## Todo as its own feature

Some work is large enough to become a **separate feature file** while staying linked to the parent.

**Promote when:**

- The todo has its own lifecycle, constitution, or release boundary (not a single PR task).
- User names it as a new product area (“build X as its own feature”).
- Blast radius and testing depth differ enough that one file would hide risk.

**Workflow:**

1. Create `.feature-guardian/features/<new-slug>.md` (`FG-FEAT-...`, `status: PLANNED` or `IN_DEVELOPMENT`).
2. Register in `PRODUCT.md` with **Spawned from:** parent `FG-FEAT-...` / `FG-TODO-...`.
3. Move remaining scope into the new feature’s **ACTIVE WORK** (optional child `FG-TODO` rows).
4. On parent: set original `FG-TODO` to `DONE` with `Evidence: spawned feature <slug> (FG-FEAT-...)`.
5. Append `TODO_COMPLETED` on parent and `FEATURE_CREATED` on child.

**Small follow-ups stay on the parent** as `FG-TODO` only; do not create a feature file for every checkbox.

## Cursor TodoWrite

| Use | Tool |
|-----|------|
| Ephemeral steps this turn only | Cursor todos (optional) |
| Must persist across sessions | **FG-TODO** in ACTIVE WORK |

When both are used, **mirror** durable items: each open `FG-TODO` should appear in session todos while `OPEN` or `IN_PROGRESS`.

## Preflight

After FAST CONTEXT, read **ACTIVE WORK** and list open `FG-TODO` ids. Prefer finishing or updating todos before opening new scope unless the user redirects.

Include in `FG PREFLIGHT COMPLETE`:

```text
Active todos: FG-TODO-000042 OPEN (HIGH), FG-TODO-000043 IN_PROGRESS
```

## Unlazy

A focused todo can be one solo `GATES.md` scope. Orchestrated builds can assign one leaf per `FG-TODO`.

## Reporting

In user checkpoints, include:

```text
Active todos: FG-TODO-000042 OPEN (HIGH), FG-TODO-000043 IN_PROGRESS
Completed this session: FG-TODO-000041 DONE (evidence: ...)
```

## PRODUCT.md

Do not duplicate every todo at product level. Optional registry column **Open todos** count per feature during health sweeps only.
