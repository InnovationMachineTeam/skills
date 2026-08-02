import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "prompt-skills" / "prompt-master"


class PromptMasterTests(unittest.TestCase):
    def test_bundle_is_complete(self):
        required = [
            SKILL / "SKILL.md",
            SKILL / "agents" / "openai.yaml",
            SKILL / "references" / "mode-and-depth-contract.md",
            SKILL / "references" / "delivery-and-evaluation-contract.md",
            SKILL / "evals" / "routing.json",
            SKILL / "evals" / "behavior.json",
        ]
        self.assertTrue(all(path.is_file() for path in required))

    def test_all_modes_and_depths_are_operationalized(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for mode in ("improve", "reconstruct", "generalize", "specialize", "merge", "decompose", "audit", "optimize"):
            self.assertIn(f"`{mode}`", text)
        for depth in ("Compact", "Standard", "Production"):
            self.assertIn(depth, text)

    def test_reconstruction_never_claims_hidden_original(self):
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        modes = (SKILL / "references" / "mode-and-depth-contract.md").read_text(encoding="utf-8")
        self.assertIn("exact_original_recovered", skill)
        self.assertIn("exact_original_recovered: false", modes)
        self.assertIn("functional_equivalence_targeted: true", modes)

    def test_routing_covers_modes_and_neighbors(self):
        data = json.loads((SKILL / "evals" / "routing.json").read_text(encoding="utf-8"))
        routes = {case["expected_route"] for case in data["cases"]}
        for mode in ("improve", "reconstruct", "generalize", "specialize", "merge", "decompose", "audit", "optimize"):
            self.assertIn(f"prompt-master:{mode}", routes)
        self.assertIn("prompt-optimize", routes)

    def test_behavior_covers_authority_and_false_evidence(self):
        data = json.loads((SKILL / "evals" / "behavior.json").read_text(encoding="utf-8"))
        joined = json.dumps(data, ensure_ascii=False)
        for phrase in ("untrusted data", "verbatim recovery", "publication gates", "marks semantic validation not evaluated"):
            self.assertIn(phrase, joined)

    def test_category_instructions_are_synchronized(self):
        self.assertEqual(
            (ROOT / "skills" / "prompt-skills" / "AGENTS.md").read_bytes(),
            (ROOT / "skills" / "prompt-skills" / "CLAUDE.md").read_bytes(),
        )


if __name__ == "__main__":
    unittest.main()
