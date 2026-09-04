#!/usr/bin/env python3
"""Unit tests for validate_memory.py"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PKG_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = PKG_ROOT / "scripts"
VALIDATOR = SCRIPTS / "validate_memory.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run_validator(project_root: Path) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(project_root)],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout + result.stderr


def copy_fixture(name: str, tmp: Path) -> Path:
    src = FIXTURES / name
    shutil.copytree(src, tmp, dirs_exist_ok=True)
    return tmp


class ValidateMemoryTests(unittest.TestCase):
    def test_valid_product_and_feature_memory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_fixture("valid", Path(tmp))
            code, output = run_validator(root)
            self.assertEqual(code, 0, output)
            self.assertIn("OK", output)

    def test_duplicate_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_fixture("valid", Path(tmp))
            features = root / ".feature-guardian/features"
            dup = features / "auth-dup.md"
            shutil.copy(features / "auth.md", dup)
            dup.write_text(
                dup.read_text(encoding="utf-8").replace(
                    "slug: auth", "slug: auth-dup"
                ),
                encoding="utf-8",
            )
            product = root / ".feature-guardian/PRODUCT.md"
            product.write_text(
                product.read_text(encoding="utf-8")
                + "\n| FG-FEAT-000001 | Auth Dup | COMPLETED | HEALTHY | HIGH | DORMANT | 2026-09-01 |\n",
                encoding="utf-8",
            )
            code, output = run_validator(root)
            self.assertNotEqual(code, 0)
            self.assertIn("FG007", output)

    def test_registry_missing_feature_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_fixture("valid", Path(tmp))
            (root / ".feature-guardian/features/auth.md").unlink()
            code, output = run_validator(root)
            self.assertNotEqual(code, 0)
            self.assertIn("FG008", output)

    def test_feature_missing_registry_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_fixture("valid", Path(tmp))
            product = root / ".feature-guardian/PRODUCT.md"
            product.write_text(
                product.read_text(encoding="utf-8").replace(
                    "| FG-FEAT-000001 | Auth | COMPLETED | HEALTHY | HIGH | DORMANT | 2026-09-01 |",
                    "",
                ),
                encoding="utf-8",
            )
            code, output = run_validator(root)
            self.assertNotEqual(code, 0)
            self.assertIn("FG009", output)

    def test_invalid_feature_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_fixture("valid", Path(tmp))
            feat = root / ".feature-guardian/features/auth.md"
            feat.write_text(
                feat.read_text(encoding="utf-8").replace(
                    "status: COMPLETED", "status: NOT_A_REAL_STATUS"
                ),
                encoding="utf-8",
            )
            code, output = run_validator(root)
            self.assertNotEqual(code, 0)
            self.assertIn("FG018", output)

    def test_duplicate_slug(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_fixture("valid", Path(tmp))
            features = root / ".feature-guardian/features"
            dup = features / "auth-duplicate.md"
            shutil.copy(features / "auth.md", dup)
            dup.write_text(
                dup.read_text(encoding="utf-8").replace(
                    "feature-id: FG-FEAT-000001", "feature-id: FG-FEAT-000002"
                ),
                encoding="utf-8",
            )
            product = root / ".feature-guardian/PRODUCT.md"
            product.write_text(
                product.read_text(encoding="utf-8").replace(
                    "| FG-FEAT-000001 | Auth | COMPLETED | HEALTHY | HIGH | DORMANT | 2026-09-01 |",
                    "| FG-FEAT-000001 | Auth | COMPLETED | HEALTHY | HIGH | DORMANT | 2026-09-01 |\n| FG-FEAT-000002 | Auth Dup | COMPLETED | HEALTHY | HIGH | DORMANT | 2026-09-01 |",
                ),
                encoding="utf-8",
            )
            code, output = run_validator(root)
            self.assertNotEqual(code, 0)
            self.assertIn("FG031", output)

    def test_broken_referenced_test_id_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_fixture("valid", Path(tmp))
            feat = root / ".feature-guardian/features/auth.md"
            feat.write_text(
                feat.read_text(encoding="utf-8")
                + "\nDepends on test FG-TEST-999999 for orphan check.\n",
                encoding="utf-8",
            )
            code, output = run_validator(root)
            self.assertIn("FG029", output)

    def test_completed_with_open_critical_regression(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_fixture("valid", Path(tmp))
            feat = root / ".feature-guardian/features/auth.md"
            feat.write_text(
                feat.read_text(encoding="utf-8")
                + """

<!-- FG:ACTIVE_REGRESSIONS:START -->
## ACTIVE REGRESSIONS

### FG-REG-000099

Severity:
CRITICAL
Status:
OPEN
<!-- FG:ACTIVE_REGRESSIONS:END -->
""",
                encoding="utf-8",
            )
            code, output = run_validator(root)
            self.assertNotEqual(code, 0)
            self.assertIn("FG024", output)

    def test_malformed_schema_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_fixture("valid", Path(tmp))
            feat = root / ".feature-guardian/features/auth.md"
            feat.write_text(
                feat.read_text(encoding="utf-8").replace(
                    'memory-revision: 1', 'memory-revision: not-a-number'
                ),
                encoding="utf-8",
            )
            code, output = run_validator(root)
            self.assertNotEqual(code, 0)
            self.assertIn("FG022", output)

    def test_missing_fg_schema_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_fixture("valid", Path(tmp))
            feat = root / ".feature-guardian/features/auth.md"
            feat.write_text(
                feat.read_text(encoding="utf-8").replace('fg-schema: "0.1"\n', ""),
                encoding="utf-8",
            )
            code, output = run_validator(root)
            self.assertNotEqual(code, 0)
            self.assertIn("FG015", output)


if __name__ == "__main__":
    unittest.main()
