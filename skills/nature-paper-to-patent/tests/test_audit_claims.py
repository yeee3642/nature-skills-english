import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("audit_claims", ROOT / "scripts" / "audit_claims.py")
AUDIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDIT
SPEC.loader.exec_module(AUDIT)


def codes(text):
    return [finding.code for finding in AUDIT.audit(text)]


class AntecedentBasisTests(unittest.TestCase):
    def test_term_used_with_suo_shu_but_never_introduced_is_flagged(self):
        self.assertIn("ANTECEDENT_BASIS", codes("1. \u4e00\u79cd\u88c5\u7f6e，\u5176\u7279\u5f81\u5728\u4e8e，\u5305\u62ec\u6240\u8ff0\u7535\u6781。\n"))

    def test_term_introduced_earlier_in_the_same_claim_is_not_flagged(self):
        self.assertNotIn(
            "ANTECEDENT_BASIS", codes("1. \u4e00\u79cd\u68c0\u6d4b\u88c5\u7f6e，\u5176\u7279\u5f81\u5728\u4e8e，\u5305\u62ec\u7535\u6781\u548c\u57fa\u677f，\u6240\u8ff0\u7535\u6781\u8bbe\u7f6e\u4e8e\u6240\u8ff0\u57fa\u677f\u4e0a。\n")
        )

    def test_term_introduced_in_a_referenced_claim_is_not_flagged(self):
        text = "1. \u4e00\u79cd\u68c0\u6d4b\u88c5\u7f6e，\u5176\u7279\u5f81\u5728\u4e8e，\u5305\u62ec\u7535\u6781\u548c\u57fa\u677f。\n2. \u6839\u636e\u6743\u5229\u8981\u6c421\u6240\u8ff0\u7684\u88c5\u7f6e，\u5176\u7279\u5f81\u5728\u4e8e，\u6240\u8ff0\u7535\u6781\u4e3a\u91d1\u5c5e\u7535\u6781。\n"
        self.assertNotIn("ANTECEDENT_BASIS", codes(text))


class GenericReferenceTests(unittest.TestCase):
    def test_reference_phrase_in_a_dependent_claim_is_not_a_term(self):
        text = "1. \u4e00\u79cd\u68c0\u6d4b\u88c5\u7f6e，\u5176\u7279\u5f81\u5728\u4e8e，\u5305\u62ec\u7535\u6781\u548c\u57fa\u677f，\u6240\u8ff0\u7535\u6781\u8bbe\u7f6e\u4e8e\u6240\u8ff0\u57fa\u677f\u4e0a。\n2. \u6839\u636e\u6743\u5229\u8981\u6c421\u6240\u8ff0\u7684\u68c0\u6d4b\u88c5\u7f6e，\u5176\u7279\u5f81\u5728\u4e8e，\u6240\u8ff0\u7535\u6781\u4e3a\u91d1\u5c5e\u7535\u6781。\n"
        self.assertNotIn("ANTECEDENT_BASIS", codes(text))


if __name__ == "__main__":
    unittest.main()
