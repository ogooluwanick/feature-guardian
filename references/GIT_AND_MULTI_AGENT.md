# Git and Multi-Agent Reconciliation

## Git as evidence

Allowed automatically (read-only unless user requests writes):

- current branch, status, diff, changed files;
- commit history relevant to feature;
- merge base when useful.

Record when relevant:

```text
Branch: feature/payroll-idempotency
Git state: WORKING_TREE
Introduced commit: abc1234
Last verified commit: def5678
```

Use `Git state: WORKING_TREE` when no commit exists yet. Never invent hashes.

## Last-known-good baselines

```text
Feature: Payroll
Last known good commit: 4f33a9c
Verified release: v1.9.0
```

Useful when investigating regressions since a known-good point.

## Multi-branch memory disagreement

If Branch A records `FG-TEST-0021 PASS` and Branch B records `FG-TEST-0021 FAIL`:

- preserve **both** with branch/commit context in event history;
- do not delete either historical result.

After merge:

1. Reconcile current implementation.
2. Mark current result `UNKNOWN` or `STALE` if needed.
3. Rerun relevant verification.
4. Update current state.
5. Append memory reconciliation event (`MEMORY_CORRECTION` or `TEST_RUN`).

Ordinary Git conflict resolution must not erase engineering events.

## Multi-agent sessions

Different agents or sessions may update memory. Use:

- `memory-revision` increments;
- immutable event history;
- validator after updates;
- evidence re-verification after merges.

## Commits and pushes

Do not commit, push, force-push, or rewrite history unless the user asked.

Feature Guardian memory updates are part of the engineering task but follow the user's Git workflow preferences.
