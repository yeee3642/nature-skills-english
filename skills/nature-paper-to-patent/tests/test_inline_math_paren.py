import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "scripts" / "disclosure"


def load(name, filename):
    sys.path.insert(0, str(ROOT.parent))
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


MATH_RENDER = load("patent_math_render", "math_render.py")
MD_TO_DOCX = load("patent_md_to_docx", "md_to_docx.py")


class InlineParenMathTests(unittest.TestCase):
    def test_math_with_an_inner_parenthesis_matches(self):
        match = MATH_RENDER._INLINE_PAREN_RE.search(r"" "\u8bbe" r" \(f(x)\) " "\u4e3a" r"" "\u51fd" r"" "\u6570" r"")
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "f(x)")

    def test_simple_math_still_matches(self):
        self.assertEqual(MATH_RENDER._INLINE_PAREN_RE.search(r"" "\u4ee4" r" \(\sigma\) " "\u4e3a" r"").group(1), r"\sigma")

    def test_two_formulas_on_one_line_stay_separate(self):
        found = [m.group(1) for m in MATH_RENDER._INLINE_PAREN_RE.finditer(r"\(a\) " "\u4e0e" r" \(g(b)\)")]
        self.assertEqual(found, ["a", "g(b)"])

    def test_hidden_image_variant_handles_inner_parenthesis(self):
        text = r"" "\u8bbe" r" \(f(x)\)<!-- ![eq](img/e1.png) --> " "\u4e3a" r"" "\u51fd" r"" "\u6570" r""
        match = MD_TO_DOCX._INLINE_MATH_PAREN_WITH_HIDDEN_IMG_RE.search(text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "f(x)")

    def test_hidden_image_variant_does_not_swallow_a_neighbouring_formula(self):
        text = r"\(a\) " "\u4e0e" r" \(g(b)\)<!-- ![eq](img/e2.png) -->"
        match = MD_TO_DOCX._INLINE_MATH_PAREN_WITH_HIDDEN_IMG_RE.search(text)
        self.assertEqual(match.group(1), "g(b)")


if __name__ == "__main__":
    unittest.main()
