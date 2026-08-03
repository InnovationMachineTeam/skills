from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_skill_context.py"
SPEC = importlib.util.spec_from_file_location("audit_skill_context", SCRIPT)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class ContextEngineeringTests(unittest.TestCase):
    def test_hard_rules_are_classified_by_reason(self) -> None:
        self.assertEqual(AUDIT.classify_line("Never publish without approval."), "authority_safety")
        self.assertEqual(AUDIT.classify_line("Must verify the artifact before completion."), "verification_recovery")
        self.assertEqual(AUDIT.classify_line("Always emit the required JSON schema."), "deterministic_interface")
        self.assertEqual(AUDIT.classify_line("Always prefer headings."), "judgment_candidate")
        self.assertIsNone(AUDIT.classify_line("Prefer the surrounding project style."))

    def test_entry_skills_have_both_capability_profiles(self) -> None:
        targets = (
            ROOT / "skills" / "agent-master" / "agent-master",
            ROOT / "skills" / "prompt-skills" / "prompt-master",
            ROOT / "skills" / "metaskills" / "skill-builder",
        )
        for target in targets:
            skill = (target / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("constrained", skill)
            self.assertIn("standard", skill)
            self.assertTrue((target / "references" / "model-capability-profiles.md").is_file())


if __name__ == "__main__":
    unittest.main()
