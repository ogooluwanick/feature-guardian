import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('check_parity', ROOT / 'scripts/check_parity.py')
parity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parity)


class ParityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.feature = self.root / '.feature-guardian/features/summary.md'
        self.feature.parent.mkdir(parents=True)
        for name in ['provider.py', 'consumer.py']:
            (self.root / name).write_text('shared_contract = 1\n')
        self.unit = {
            'id': 'currency-prop', 'contract': 'Summary receives the declared currency',
            'provider': 'provider.py', 'consumer': 'consumer.py', 'variant': 'non-default currency',
            'aspect': 'props', 'status': 'PASS', 'evidence': ['FG-EVID-000001'],
            'source_hashes': {name: hashlib.sha256((self.root / name).read_bytes()).hexdigest() for name in ['provider.py', 'consumer.py']},
        }

    def write(self, units=None, reviewed=True, claim='PARTIAL', evidence_result='PASS'):
        data = {'schema_version': 1, 'scope_reviewed': reviewed, 'units': [self.unit] if units is None else units}
        self.feature.write_text(f'''---
parity-claim: {claim}
---
<!-- FG:PARITY:START -->
```json
{json.dumps(data)}
```
<!-- FG:PARITY:END -->
### FG-EVID-000001

Type: CONTRACT
Environment: LOCAL
Result: {evidence_result}
Timestamp: 2026-11-13T00:00:00Z
Freshness: FRESH
''')
        return parity.inspect_feature(self.feature, self.root)

    def test_fresh_reviewed_contract_and_intended_difference(self):
        na = {**self.unit, 'id': 'admin-private-fields', 'status': 'NOT_APPLICABLE', 'reason': 'Public summary intentionally excludes private admin fields.'}
        result = self.write([self.unit, na], claim='VERIFIED')
        self.assertEqual(result['status'], 'PASS', result)
        self.assertEqual(result['parity_percent'], 100)
        self.assertEqual(result['not_applicable'], 1)

    def test_changed_consumer_or_shared_dependency_invalidates_proof(self):
        self.write(claim='VERIFIED')
        (self.root / 'consumer.py').write_text('shared_contract = 2\n')
        result = parity.inspect_feature(self.feature, self.root)
        self.assertEqual(result['stale'], 1)
        self.assertNotEqual(result['status'], 'PASS')
        self.assertTrue(result['errors'])

    def test_missing_evidence_or_mismatched_outcome_cannot_pass(self):
        self.assertTrue(self.write(evidence_result='FAIL')['errors'])
        self.unit['evidence'] = []
        self.assertTrue(self.write()['errors'])

    def test_provider_and_consumer_must_both_be_fingerprinted(self):
        del self.unit['source_hashes']['consumer.py']
        self.assertEqual(self.write()['stale'], 1)

    def test_no_false_100_on_empty_unknown_stale_or_unreviewed_scope(self):
        self.assertIsNone(self.write([])['parity_percent'])
        self.assertEqual(self.write(reviewed=False)['status'], 'UNKNOWN')
        self.unit['status'] = 'UNKNOWN'
        result = self.write(claim='VERIFIED')
        self.assertEqual(result['parity_percent'], 0)
        self.assertTrue(result['errors'])
        self.assertEqual(parity.summarize(['PASS', 'UNKNOWN'], True)['parity_percent'], 50)
        self.assertEqual(parity.summarize(['NOT_APPLICABLE'], True)['status'], 'UNKNOWN')

    def test_exclusion_requires_reason_and_ids_are_unique(self):
        self.unit['status'] = 'NOT_APPLICABLE'
        self.assertTrue(self.write()['errors'])
        self.unit['reason'] = 'Different authorized audience'
        self.assertTrue(self.write([self.unit, self.unit])['errors'])

    def test_legacy_memory_is_unknown_without_forced_migration(self):
        self.feature.write_text('# Existing completed feature\n')
        result = parity.inspect_feature(self.feature, self.root)
        self.assertFalse(result['errors'])
        self.assertEqual(result['status'], 'UNKNOWN')
        self.feature.write_text('---\nparity-claim: VERIFIED\n---\n')
        self.assertTrue(parity.inspect_feature(self.feature, self.root)['errors'])

    def test_cli_check_fails_for_unknown_and_report_succeeds(self):
        self.unit['status'] = 'UNKNOWN'
        self.write()
        cmd = [sys.executable, str(ROOT / 'scripts/check_parity.py'), str(self.root), '--feature', 'summary']
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run(cmd + ['--check'], capture_output=True).returncode, 1)
        self.assertEqual(subprocess.run(cmd + ['--feature', 'missing'], capture_output=True).returncode, 2)

    def test_untrusted_commands_are_only_metadata_and_paths_cannot_escape(self):
        self.unit['command'] = 'touch DO_NOT_EXECUTE'
        self.assertEqual(self.write()['status'], 'PASS')
        self.assertFalse((self.root / 'DO_NOT_EXECUTE').exists())
        self.assertFalse(parity.source_is_current(self.root, '../elsewhere', 'anything'))

    def test_memory_validator_rejects_false_verified_claim_but_accepts_unknown_debt(self):
        import shutil
        project = self.root / 'integration'
        shutil.copytree(ROOT / 'tests/fixtures/valid', project)
        feature = project / '.feature-guardian/features/auth.md'
        original = feature.read_text()
        manifest = '\n<!-- FG:PARITY:START -->\n```json\n' + json.dumps({'schema_version': 1, 'scope_reviewed': False, 'units': []}) + '\n```\n<!-- FG:PARITY:END -->\n'
        feature.write_text(original.replace('---\n', '---\nparity-claim: UNKNOWN\n', 1) + manifest)
        cmd = [sys.executable, str(ROOT / 'scripts/validate_memory.py'), str(project)]
        unknown = subprocess.run(cmd, text=True, capture_output=True)
        self.assertEqual(unknown.returncode, 0, unknown.stdout)
        feature.write_text(feature.read_text().replace('parity-claim: UNKNOWN', 'parity-claim: VERIFIED'))
        false_claim = subprocess.run(cmd, text=True, capture_output=True)
        self.assertNotEqual(false_claim.returncode, 0)
        self.assertIn('FG037', false_claim.stdout)

    def test_malformed_manifest_or_marker_pair_is_reported(self):
        self.feature.write_text('<!-- FG:PARITY:END -->\n')
        self.assertTrue(parity.inspect_feature(self.feature, self.root)['errors'])
        self.write()
        self.feature.write_text(self.feature.read_text().replace('"units":', '"units"'))
        self.assertTrue(parity.inspect_feature(self.feature, self.root)['errors'])

    def write_card(self, status='OK', claim='PARTIAL', mutate_consumer=False):
        hashes = {
            name: hashlib.sha256((self.root / name).read_bytes()).hexdigest()
            for name in ['provider.py', 'consumer.py']
        }
        item = {
            'id': 'currency-prop',
            'contract': 'Summary receives the declared currency',
            'provider': 'provider.py',
            'check_here': ['consumer.py'],
            'intentional_diffs': 'none',
            'prove_with': 'consumer.py',
            'status': status,
            'source_hashes': hashes,
            'evidence': ['FG-EVID-000001'],
        }
        data = {'schema_version': 2, 'items': [item]}
        self.feature.write_text(f'''---
parity-claim: {claim}
---
<!-- FG:PARITY:START -->
```json
{json.dumps(data)}
```
<!-- FG:PARITY:END -->
### FG-EVID-000001

Type: CONTRACT
Environment: LOCAL
Result: PASS
Timestamp: 2026-11-13T00:00:00Z
Freshness: FRESH
''')
        if mutate_consumer:
            (self.root / 'consumer.py').write_text('shared_contract = 2\n')
        return parity.inspect_feature(self.feature, self.root)

    def test_schema2_card_ok_and_stale_blocks_done(self):
        result = self.write_card(claim='VERIFIED')
        self.assertEqual(result['status'], 'PASS', result)
        self.assertFalse(result['blocks_done'])
        stale = self.write_card(claim='VERIFIED', mutate_consumer=True)
        self.assertEqual(stale['stale'], 1)
        self.assertTrue(stale['blocks_done'])
        self.assertTrue(stale['drifts'])
        self.assertIn('Parity drift', parity.format_user_drift_report(stale))

    def test_schema2_cli_check_fails_when_stale(self):
        self.write_card(mutate_consumer=True)
        cmd = [sys.executable, str(ROOT / 'scripts/check_parity.py'), str(self.root), '--feature', 'summary', '--check']
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 1)


if __name__ == '__main__':
    unittest.main()
