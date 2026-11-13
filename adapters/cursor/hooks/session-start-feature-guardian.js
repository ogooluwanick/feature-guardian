#!/usr/bin/env node
/**
 * Session reminder when any workspace root has Feature Guardian memory.
 */
const fs = require('fs');
const path = require('path');
const { readStdin } = require('./adapter');

function workspaceRoots(input) {
  const roots = input.workspace_roots;
  if (Array.isArray(roots) && roots.length > 0) {
    return roots.filter((r) => typeof r === 'string' && r.trim());
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

readStdin()
  .then((raw) => {
    let input = {};
    try {
      input = JSON.parse(raw || '{}');
    } catch {
      input = {};
    }

    const fgRoots = workspaceRoots(input).filter(hasFeatureGuardianMemory);
    if (fgRoots.length === 0) {
      console.log(JSON.stringify({}));
      return;
    }

    const brief = [
      '[Feature Guardian — session]',
      'Repo has `.feature-guardian/`. Load `.cursor/skills/feature-guardian/SKILL.md` before product code.',
      'Preflight first; use unlazy gates, council when ambiguous, impeccable/emil for UI.',
    ].join('\n');

    console.log(JSON.stringify({ additional_context: brief }));
  })
  .catch(() => process.exit(0));
