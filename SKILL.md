---
name: feature-guardian
description: >-
  Persistent product and feature engineering memory for AI-assisted development.
  Use whenever creating, modifying, debugging, testing, refactoring, reviewing,
  or completing product behavior, including small features. Tracks feature intent,
  requirements, tests, evidence, dependencies, regressions, failures, decisions,
  blast radius, peer relationships, completed-feature review, and feature-scoped
  todos (FG-TODO), and cross-surface data, logic and prop parity across sessions.
license: MIT
metadata:
  version: "0.1.6"
  schema-version: "0.1"
---

# Feature Guardian

**Nothing is forgotten, nothing is assumed to work, and nothing important changes without understanding what it could affect.**

Feature Guardian is persistent engineering memory for AI coding agents. It tracks every product feature (including small ones), preserves complete history, verifies claims with evidence, detects regressions and blast radius, and protects completed features from silent breakage.

## When this skill applies

Apply automatically for any task that touches:

- product behavior, UX copy with behavioral impact, or feature scope;
- application code, tests, configuration, schemas, or dependencies;
- architecture, contracts, or shared infrastructure;
- bug fixes, refactors, reviews, or completion claims.

Skip only when the user explicitly excluded the feature (`Monitoring: EXCLUDED`) or the task is purely unrelated tooling with zero product impact.

## Companion skills (unlazy, council, taste)

Feature work must be **guarded** (memory before code) and **provably complete** (gates before done). See [COMPANION_SKILLS.md](references/COMPANION_SKILLS.md):

- **unlazy** — write and pass `GATES.md` for substantial product work; no done report while gates fail.
- **council** — convene when direction is ambiguous or FG alignment is `POTENTIAL_CONFLICT` / `STRONG_CONFLICT`.
- **impeccable + emil-design-eng** — user-facing surfaces; load design context before UI/email work.

Preflight is mandatory when `.feature-guardian/` exists: [PREFLIGHT_PROTOCOL.md](references/PREFLIGHT_PROTOCOL.md).

## Non-negotiable rules

1. **One feature = one permanent Markdown file** in `.feature-guardian/features/<slug>.md`. Never split a feature across multiple memory files.
2. **Product memory is separate:** `.feature-guardian/PRODUCT.md` holds product intent, registry, and relationships.
3. **Memory is not evidence.** Evidence hierarchy: runtime observation → executed tests → code/config → build/lint → memory → inference → assumption.
4. **No evidence, no claim.** Never mark FIXED/VERIFIED/STABLE from implementation alone.
5. **Preserve history.** Failures, rejected approaches, regressions, and superseded decisions are append-only.
6. **Blast radius on meaningful changes.** See [IMPACT_AND_REVIEW.md](references/IMPACT_AND_REVIEW.md).
7. **Completed ≠ forgotten.** Credible downstream impact → `REVIEW_REQUIRED`, not silent breakage.
8. **User remains authority.** Recommend and warn; block only on hard invariant violations or unrequested destructive ops.
9. **Track small features.** Copy buttons, dark mode, CSV export — all get memory.
10. **Uncertainty stays explicit.** `UNKNOWN` is valid; never invent root causes.
11. **Feature todos persist in memory.** Track durable work as `FG-TODO-...` under **ACTIVE WORK**; mirror open items in Cursor todos when helpful. See [FEATURE_TODOS.md](references/FEATURE_TODOS.md).
12. **No feature is an island.** Use PRODUCT relationship map + **RELATED FEATURES** on primary and peers; preflight peer pass before shared or contract changes. See [FEATURE_PEER_AWARENESS.md](references/FEATURE_PEER_AWARENESS.md).

13. **Connected contracts stay in parity.** Maintain a lean **parity card index** per feature; read it on related work; force investigation when STALE/FAIL or listed paths are touched. Follow [PARITY.md](references/PARITY.md). STALE/FAIL blocks done for touched contracts. Always report drifts to the user; ask when the fix is ambiguous or needs a business decision.

## Parity is automatic (index first, force when needed)

For every applicable feature task:

1. **Preflight:** read the feature **PARITY** card index (`FG:PARITY`, schema 2 preferred). Missing = UNKNOWN.
2. **Related work:** if the task intersects a card’s provider or `check_here`, open those paths only. Do not randomly re-scan the repo.
3. **Forced gate:** hash mismatch demotes OK → STALE. `check_parity.py --feature <slug> --check` must pass before done for contracts you touched. `blocks_done` forbids completion claims.
4. **User communication:** when drift appears, tell the user what drifted, what you did, and what remains. Ask before choosing among non-obvious or business-critical fixes. Record durable choices as `FG-DEC-...`.
5. **Grow the index** when you discover a missing consumer; that raises assurance without full audits every turn.

Persist cards and evidence in the feature file; link peers via PRODUCT / RELATED FEATURES. Schema 1 unit manifests remain valid. Details: [PARITY.md](references/PARITY.md).

## Runtime memory layout

```text
.feature-guardian/
├── PRODUCT.md
└── features/
    └── <feature-slug>.md
```

Bootstrap if missing: run `scripts/bootstrap_memory.py` from the installed skill package, then inspect the repository and populate memory.

## Operating lifecycle

For every meaningful engineering task, follow [OPERATING_PROTOCOL.md](references/OPERATING_PROTOCOL.md). **Start with** [PREFLIGHT_PROTOCOL.md](references/PREFLIGHT_PROTOCOL.md) when `.feature-guardian/` exists — no product code edits before preflight completes.

```text
Preflight → Identify feature(s) → Load PRODUCT.md + feature memory → Inspect code/tests
→ Reconcile memory with evidence → Check alignment + invariants → Risk + blast radius
→ Select test depth → Implement → Run tests → Check regressions
→ Flag completed features for review → Update memory + append events
→ Validate memory → Concise user report
```

## Start of work (before changing code)

0. **Preflight** — [PREFLIGHT_PROTOCOL.md](references/PREFLIGHT_PROTOCOL.md). Emit `FG PREFLIGHT COMPLETE` checkpoint internally.
1. **Unlazy** — For substantial work, author `GATES.md` from [assets/GATES_FEATURE_TEMPLATE.md](assets/GATES_FEATURE_TEMPLATE.md) before implementation.
2. Load `PRODUCT.md` and relevant feature file(s). Use section markers and IDs — do not dump entire histories blindly.
3. Read constitution, current state, active issues, failed approaches, invariants, dependencies, and test registry.
4. Inspect actual code, tests, and Git state. Reconcile contradictions (evidence wins).
5. Search aliases/registry before creating a new feature file.
6. **Council** — if alignment conflict or ambiguous scope, use `council` skill before committing to implementation.
6a. **Parity** — Read the feature parity **card index**; note STALE/FAIL and path intersections. Escalate only when forced (see [PARITY.md](references/PARITY.md)).
7. **Taste** — if user-facing, load impeccable + emil-design-eng before UI/email edits.

## During work

Update memory after **meaningful events** (implementation milestone, test result, failure, decision, regression, contract change, review trigger). Increment `memory-revision` in frontmatter after successful updates.

Record change IDs (`FG-CHG-...`) for meaningful engineering changes.

### Feature todos (ACTIVE WORK)

When the user asks to track work, you split a multi-step task, or follow-ups remain after a session:

1. Add or update `FG-TODO-######` under `<!-- FG:ACTIVE_WORK:START -->` in the owning feature file (or spawn a new feature; see [FEATURE_TODOS.md](references/FEATURE_TODOS.md)).
2. Set exactly one todo `IN_PROGRESS` per feature unless the user parallelizes.
3. On completion: `Status: DONE`, `Completed:`, `Evidence:`, append `TODO_COMPLETED` event, increment `memory-revision`.
4. On cancel: `Status: CANCELLED` with reason; append `TODO_CANCELLED`.
5. Prefer closing todos the user finished before starting unrelated scope.

Session-only steps may use Cursor TodoWrite; **cross-session** work must use `FG-TODO`.

## End of work (before declaring done)

0. **Unlazy** — Re-run approved gates; all required gates met or explicit handoff.
1. Run relevant tests at appropriate depth (default: Level 2 — feature + related/dependency). See [TESTING_AND_EVIDENCE.md](references/TESTING_AND_EVIDENCE.md).
2. Never claim completion without [completion check](references/TESTING_AND_EVIDENCE.md#feature-completion-check).
3. Mark affected completed features `REVIEW_REQUIRED` with required verification listed.
4. Append session checkpoint and immutable events.
5. Update `PRODUCT.md` registry/health if product-level state changed.
6. **Peer reconciliation** — `infer_peers.py --feature <slug>`; `--apply` if gaps; see [FEATURE_PEER_AWARENESS.md](references/FEATURE_PEER_AWARENESS.md).
7. **Parity gate** — Run `check_parity.py --feature <slug> --check` (and `--report` if drifts). Clear STALE/FAIL for touched cards with proof, or leave documented debt and **do not claim done** for those contracts. Always tell the user what drifted and what was done; ask when a decision is required.
8. Run `validate_memory.py` on the project root.

## Direction conflicts

Evaluate requests against product vision, principles, constitution, non-goals, and invariants:

| Level | Action |
|---|---|
| ALIGNED | Proceed |
| POTENTIAL_CONFLICT | Explain; continue if intent clear |
| STRONG_CONFLICT | Ask before changing constitution |
| INVARIANT_VIOLATION | Stop; require explicit resolution |

Details: [SAFETY_AND_AUTONOMY.md](references/SAFETY_AND_AUTONOMY.md)

## Reference map

| Topic | Document |
|---|---|
| Full lifecycle | [OPERATING_PROTOCOL.md](references/OPERATING_PROTOCOL.md) |
| IDs, events, revisions | [DATA_MODEL.md](references/DATA_MODEL.md) |
| Feature file schema | [FEATURE_MEMORY_SCHEMA.md](references/FEATURE_MEMORY_SCHEMA.md) |
| Product file schema | [PRODUCT_MEMORY_SCHEMA.md](references/PRODUCT_MEMORY_SCHEMA.md) |
| Tests and evidence | [TESTING_AND_EVIDENCE.md](references/TESTING_AND_EVIDENCE.md) |
| Blast radius and review | [IMPACT_AND_REVIEW.md](references/IMPACT_AND_REVIEW.md) |
| Peer awareness (not isolated) | [FEATURE_PEER_AWARENESS.md](references/FEATURE_PEER_AWARENESS.md) |
| Feature boundaries, merge/split | [FEATURE_BOUNDARIES.md](references/FEATURE_BOUNDARIES.md) |
| Git and multi-agent | [GIT_AND_MULTI_AGENT.md](references/GIT_AND_MULTI_AGENT.md) |
| Safety, opt-out, destructive ops | [SAFETY_AND_AUTONOMY.md](references/SAFETY_AND_AUTONOMY.md) |
| Beginner experience | [BEGINNER_EXPERIENCE.md](references/BEGINNER_EXPERIENCE.md) |
| Preflight and gates A–D | [PREFLIGHT_PROTOCOL.md](references/PREFLIGHT_PROTOCOL.md) |
| unlazy, council, taste | [COMPANION_SKILLS.md](references/COMPANION_SKILLS.md) |
| Data, logic and prop parity | [PARITY.md](references/PARITY.md) |
| Feature todos (FG-TODO) | [FEATURE_TODOS.md](references/FEATURE_TODOS.md) |

## Templates and examples

- New feature: [assets/FEATURE_TEMPLATE.md](assets/FEATURE_TEMPLATE.md)
- Feature work gates: [assets/GATES_FEATURE_TEMPLATE.md](assets/GATES_FEATURE_TEMPLATE.md)
- New product: [assets/PRODUCT_TEMPLATE.md](assets/PRODUCT_TEMPLATE.md)
- Examples: [examples/](examples/)

## User report format

After meaningful work, provide a compact checkpoint (not a full memory dump):

```text
✓ [Feature] update completed

Changed: ...
Verification: ... (tests run, results, environments)
Feature health: HEALTHY — HIGH confidence (with reasons)
Active todos: FG-TODO-... OPEN | IN_PROGRESS (list); completed this session: ...
Completed-feature review: ...
Feature Guardian: memory files updated; validator result
Parity: ... (OK | drifts found: …; actions: …; awaiting decision: … | none)
Remaining: ... (explicit unknowns/limitations)
```

## Limitations (v0.1)

- No background execution between sessions; continuity depends on memory files and the next agent turn.
- No hosted dashboard, database, or MCP server.
- Validator checks structure and key consistency; it does not run tests or verify runtime behavior.
- Automatic behavior in Cursor requires both this skill **and** the always-on adapter rule.

## Version

Skill `0.1.6` · Schema `0.1`
