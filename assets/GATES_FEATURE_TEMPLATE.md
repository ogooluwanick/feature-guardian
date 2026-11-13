# Gates: <feature slug or task name>

OWNS: <repository-relative globs this task may write, e.g. lib/services/foo/**, __tests__/foo/**, .feature-guardian/features/foo.md>

Scope: <one sentence — complete deliverable for this session>

- [ ] G1: Feature Guardian preflight completed before product code edits
  EVIDENCE: pending
  <!-- Manual: primary feature slug, related features, FG-FAIL/DEC ids searched, dependents noted -->

- [ ] G2: Direct and dependency tests run at selected depth (Level 2 default)
  CHECK: <project test command, e.g. npm run test:run -- __tests__/path/to/feature.test.ts>
  EXPECT: passed
  EVIDENCE: pending

- [ ] G3: Feature Guardian memory valid when updated
  CHECK: python3 <path-to-feature-guardian>/scripts/validate_memory.py .
  EXPECT: OK
  CWD: <project root>
  EVIDENCE: pending

- [ ] G4: Feature completion check recorded (not implementation-only done)
  EVIDENCE: pending
  <!-- Manual: VERIFIED_COMPLETE | COMPLETE_WITH_KNOWN_RISK | NOT_COMPLETE; REVIEW_REQUIRED applied if needed -->

<!--
Optional G5 (user-facing): impeccable/emil review — manual gate with surface + responsive check noted.

Replace CHECK paths for your repo. Lint before use:
  node ~/.agents/skills/unlazy/scripts/gate-lint.mjs GATES.md
-->
