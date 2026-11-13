# Companion Skills

Feature Guardian owns **persistent memory, blast radius, and evidence**. Three companion skills tighten **completion discipline**, **ambiguous decisions**, and **product taste** while the user builds and maintains features.

Load paths (machine-wide):

| Skill | Typical path |
|-------|----------------|
| unlazy | `~/.agents/skills/unlazy/SKILL.md` |
| council | `~/.cursor/skills/council/SKILL.md` |
| impeccable | `~/.agents/skills/impeccable/SKILL.md` |
| emil-design-eng | `~/.agents/skills/emil-design-eng/SKILL.md` |

## Execution stack

```text
USER REQUEST
     ↓
FG PREFLIGHT (mandatory) — PREFLIGHT_PROTOCOL.md
     ↓
COUNCIL (sometimes) — tradeoffs / direction conflict
     ↓
TASTE (when user-facing) — impeccable + emil-design-eng
     ↓
UNLAZY GATES — before substantial implementation
     ↓
IMPLEMENT → VERIFY → FG MEMORY RECONCILIATION
     ↓
UNLAZY GATE CHECK — before completion claim
```

Preflight always precedes implementation. Unlazy gates precede substantial coding and must pass before "done."

---

## Unlazy (completion discipline)

**When:** Any Feature Guardian-covered task that will change product code, tests, config, schema, or `.feature-guardian/` memory and is not a trivial one-line fix.

**When exempt:** Read-only answers, typo-only copy with no behavioral claim, or user explicitly asks for a quick draft with no completion claim.

**How:**

1. After FG preflight, write `GATES.md` at the project root (solo) using [assets/GATES_FEATURE_TEMPLATE.md](../assets/GATES_FEATURE_TEMPLATE.md), or orchestrated `.unlazy/<scope>/` for multi-leaf builds.
2. Lint: `node ~/.agents/skills/unlazy/scripts/gate-lint.mjs GATES.md`
3. Run checks with approval: `gate-check.mjs --approve GATES.md`
4. Do not report done while required gates are unmet (Cursor Stop hook may enforce this).

**FG-specific gates to include:**

- Preflight completed (manual gate with primary feature slug and history IDs checked).
- Project tests at depth from [TESTING_AND_EVIDENCE.md](TESTING_AND_EVIDENCE.md).
- `validate_memory.py` when memory changed.
- Feature completion check outcome recorded in memory.

Keep `GATES.md` and `.unlazy/` out of git (project `.gitignore`).

---

## Council (counsel — ambiguous decisions)

**When (sometimes):**

- Direction conflict `POTENTIAL_CONFLICT` or `STRONG_CONFLICT` in FG alignment check.
- User asks for tradeoffs, second opinions, or go/no-go before committing scope.
- Multiple credible implementation paths with different product risk (ship vs hold, scope cut vs full feature).

**When not:**

- Straight execution with clear requirements and aligned memory.
- Code review, test runs, or memory updates (use FG + code-reviewer instead).

**How:** Follow the `council` skill. Pass only the decision question and compact context (feature FAST CONTEXT + relevant FG-DEC/FAIL snippets), not the full chat. Record the chosen path as `FG-DEC-...` in feature memory when the decision affects future work.

---

## Taste (impeccable + emil-design-eng)

**When:** Work touches user-visible surfaces named in feature memory or code: web/mobile UI, dashboards, modals, emails, marketing, empty/loading states, transactional copy.

**How:**

1. Run `node ~/.agents/skills/impeccable/scripts/context.mjs` from the project root (`--target <path>` when scoped).
2. Honor project `PRODUCT.md` and `DESIGN.md`.
3. Apply emil-design-eng for hierarchy, spacing, motion, and polish.

Record UI verification in feature memory (manual or E2E evidence). Do not mark user-facing features `VERIFIED_COMPLETE` from implementation alone.

---

## Reporting

Combine FG checkpoint format from `SKILL.md` with unlazy gate status when gates were used:

```text
Feature Guardian: preflight complete; memory updated; validator OK
Unlazy: 4/4 gates met (G1 preflight, G2 tests, G3 validate, G4 completion check)
Council: not used | convened — <one-line decision>
Taste: N/A | impeccable context loaded for <surface>
```
