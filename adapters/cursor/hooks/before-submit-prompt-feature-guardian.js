#!/usr/bin/env node
/**
 * Inject Feature Guardian preflight mandate when a workspace root has product memory.
 * Install: copy to ~/.cursor/hooks/ and register in ~/.cursor/hooks.json (beforeSubmitPrompt).
 * Canonical copy: feature-guardian/adapters/cursor/hooks/before-submit-prompt-feature-guardian.js
 */
const fs = require('fs');
const path = require('path');
const { readStdin } = require('./adapter');

function workspaceRoots(input) {
  const roots = input.workspace_roots;
  if (Array.isArray(roots) && roots.length > 0) {
    return roots.filter((r) => typeof r === 'string' && r.trim());
  }
  if (typeof input.cwd === 'string' && input.cwd.trim()) {
    return [input.cwd.trim()];
  }
  return [];
}

function hasFeatureGuardianMemory(projectRoot) {
  try {
    return fs.existsSync(path.join(projectRoot, '.feature-guardian', 'PRODUCT.md'));
  } catch {
    return false;
  }
}

const MANDATE = [
  '[Feature Guardian — mandatory for this repo]',
  'This workspace has `.feature-guardian/`. Product and feature work is governed by the Feature Guardian stack.',
  '',
  'Before editing product code (lib/, app/, components/, emails, mobile UI, API behavior, tests, schema):',
  '1. Read the feature-guardian skill: `.cursor/skills/feature-guardian/SKILL.md`',
  '2. Run preflight: `references/PREFLIGHT_PROTOCOL.md` (no code edits until complete)',
'3. Peer pass: PRODUCT relationship map + primary RELATED FEATURES; skim peer FAST CONTEXT',
'4. Emit internal checkpoint: FG PREFLIGHT COMPLETE (primary feature, peers, historical matches)',
'5. Read ACTIVE WORK; track FG-TODO ids; mirror open todos in Cursor TodoWrite when working a list',
'',
  'Companions (same session):',
  '- unlazy: GATES.md before substantial work; no done until gates pass',
  '- council: ambiguous scope or alignment conflict before committing direction',
  '- impeccable + emil-design-eng: any user-facing surface',
  '',
  'Apply cross-surface data/logic/prop parity from `references/PARITY.md`; trace canonical providers and consumers, preserve intentional differences, and report unknown/stale evidence.',
  'Full stack: `.cursor/skills/feature-guardian/references/COMPANION_SKILLS.md`',
  '',
  'End of work: reconcile memory, REVIEW_REQUIRED for affected completed features, validate_memory.py, pass gates.',
].join('\n');

readStdin()
  .then((raw) => {
    let input = {};
    try {
      input = JSON.parse(raw || '{}');
    } catch {
      input = {};
    }

    const roots = workspaceRoots(input);
    const fgRoots = roots.filter(hasFeatureGuardianMemory);
    if (fgRoots.length === 0) {
      console.log(JSON.stringify({ continue: true }));
      return;
    }

    const scope = fgRoots.map((r) => path.basename(r) || r).join(', ');
    console.log(
      JSON.stringify({
        continue: true,
        additional_context: `${MANDATE}\n\nActive FG roots: ${scope}`,
      }),
    );
  })
  .catch(() => {
    console.log(JSON.stringify({ continue: true }));
  });
