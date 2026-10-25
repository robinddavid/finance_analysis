"""Offline tests for the new long-term heuristic factor-weight profile."""
import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).parent
SCRIPT = ROOT / "project_purple.py"
if not SCRIPT.exists():
    SCRIPT = ROOT / "project_purple_weighted.py"

# Keep this test import-free so optional app dependencies and API keys are not required.
source = SCRIPT.read_text(encoding="utf-8")
tree = ast.parse(source)
assignments = [n for n in tree.body if isinstance(n, ast.Assign)]
weights_ast = next(n.value for n in assignments if any(isinstance(t, ast.Name) and t.id == "WEIGHTS" for t in n.targets))
weights = ast.literal_eval(weights_ast)
order_ast = next(n.value for n in assignments if any(isinstance(t, ast.Name) and t.id == "COMP_ORDER" for t in n.targets))
order = ast.literal_eval(order_ast)
version_ast = next(n.value for n in assignments if any(isinstance(t, ast.Name) and t.id == "SCORE_MODEL_VERSION" for t in n.targets))
version = ast.literal_eval(version_ast)

class WeightTests(unittest.TestCase):
    def test_100_percent(self):
        self.assertEqual(sum(weights.values()), 100)
        self.assertEqual(set(weights), set(order))
        self.assertTrue(all(v > 0 for v in weights.values()))

    def test_fundamental_research_focus(self):
        self.assertEqual(sum(weights[k] for k in ("valuation", "growth", "profitability", "balance")), 77)
        self.assertLessEqual(weights["insider"] + weights["analysts"], 5)
        self.assertNotIn("macro", weights)

    def test_version_reset_guard(self):
        self.assertIn("SCORE_MODEL_VERSION", source)
        self.assertIn('data.get("scoring_model_version") != SCORE_MODEL_VERSION', source)
        self.assertEqual(version, "no_fred_quality_growth_v2")

if __name__ == "__main__":
    unittest.main(verbosity=2)
