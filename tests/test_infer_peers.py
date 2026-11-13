#!/usr/bin/env python3
"""Tests for infer_peers and fg_memory_lib."""

import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from fg_memory_lib import parse_related_features, split_peer_list  # noqa: E402
from infer_peers import infer_from_product_map, merge_suggestions, PeerSuggestion  # noqa: E402


class TestPeerListParsing(unittest.TestCase):
    def test_split_peer_list(self):
        self.assertEqual(split_peer_list("None recorded."), [])
        self.assertEqual(
            split_peer_list("wallet-and-funding, payroll-payouts"),
            ["wallet-and-funding", "payroll-payouts"],
        )

    def test_parse_related_block(self):
        text = """
<!-- FG:RELATED_FEATURES:START -->
## RELATED FEATURES
- **Depends On:** authentication
- **Feeds Into:** payroll-payouts, gifts
<!-- FG:RELATED_FEATURES:END -->
"""
        rel = parse_related_features(text)
        self.assertEqual(rel["depends_on"], ["authentication"])
        self.assertEqual(rel["feeds_into"], ["payroll-payouts", "gifts"])


class TestProductMapInfer(unittest.TestCase):
    def test_arrow_feeds(self):
        product = """
## FEATURE RELATIONSHIP MAP
```text
payment-provider-integration → payroll-payouts | gifts
```
"""
        known = {"payment-provider-integration", "payroll-payouts", "gifts"}
        dep, feeds = infer_from_product_map(
            product, "payment-provider-integration", known
        )
        feed_slugs = {f.slug for f in feeds}
        self.assertIn("payroll-payouts", feed_slugs)
        self.assertIn("gifts", feed_slugs)

    def test_merge_observed_wins(self):
        a = PeerSuggestion("x", "map", "ASSUMED", "depends_on")
        b = PeerSuggestion("x", "import", "OBSERVED", "depends_on")
        merged = merge_suggestions([a, b])
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0].confidence, "OBSERVED")


class TestReciprocalPeers(unittest.TestCase):
    def test_fg036_feeds_without_depends(self):
        from validate_memory import ValidationResult, validate_reciprocal_peers  # noqa: E402

        related = {
            "provider": {"feeds_into": ["consumer"], "depends_on": [], "shares": []},
            "consumer": {"feeds_into": [], "depends_on": [], "shares": []},
        }
        result = ValidationResult()
        validate_reciprocal_peers(related, {"consumer": Path("consumer.md")}, result)
        codes = [w.code for w in result.warnings]
        self.assertIn("FG036", codes)


if __name__ == "__main__":
    unittest.main()
