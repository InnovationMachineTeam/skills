#!/usr/bin/env python3
"""Contracts for the marketplace manager's package-private documentation skill."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "skills/metaskills/skill-marketplace-manager"
PRIVATE = PARENT / "private-skills/skill-documentation-writer"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class SkillMarketplaceDocumentationTests(unittest.TestCase):
    def test_private_skill_is_parent_only_and_complete(self) -> None:
        registry = load(PARENT / "references/private-skill-registry.json")
        self.assertEqual("skill-marketplace-manager", registry["owner_skill"])
        self.assertEqual("package_private", registry["visibility"])
        self.assertEqual(["skill-marketplace-manager"], registry["allowed_consumers"])
        self.assertEqual(1, len(registry["skills"]))
        entry = registry["skills"][0]
        self.assertEqual("skill-documentation-writer", entry["name"])
        self.assertEqual("private-skills/skill-documentation-writer", entry["locator"])

        text = (PRIVATE / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(f'version: "{entry["version"]}"', text)
        self.assertIn("explicit_parent_dispatch_only", json.dumps(registry))
        self.assertFalse((PRIVATE / "agents/openai.yaml").exists())
        for relative in (
            "references/documentation-contract.md",
            "assets/skill-readme-template.md",
            "assets/marketplace-onboarding-template.md",
            "evals/routing.json",
            "evals/behavior.json",
        ):
            self.assertTrue((PRIVATE / relative).is_file(), relative)

    def test_parent_routes_documentation_without_public_discovery(self) -> None:
        parent = (PARENT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("| `documentation` |", parent)
        self.assertIn("private-skills/skill-documentation-writer/SKILL.md", parent)
        self.assertIn("must not alter skill behavior", parent)

        catalog = load(ROOT / "catalog/entries.json")
        names = {item["name"] for item in catalog["entries"]}
        self.assertNotIn("skill-documentation-writer", names)
        self.assertFalse((PRIVATE / "agents/openai.yaml").exists())

    def test_routing_and_behavior_cover_expected_boundaries(self) -> None:
        routing = load(PRIVATE / "evals/routing.json")["cases"]
        behavior = load(PRIVATE / "evals/behavior.json")["cases"]
        self.assertTrue(any(case["expected_trigger"] is True for case in routing))
        self.assertTrue(any(case["expected_trigger"] is False for case in routing))
        self.assertEqual(
            {"skill-documentation", "marketplace-onboarding", "documentation-audit"},
            {case["expected_route"] for case in routing if case["expected_trigger"]},
        )
        forbidden = {item for case in behavior for item in case["forbidden_properties"]}
        self.assertIn("invents installation success", forbidden)
        self.assertIn("rewrites skill behavior", forbidden)
        self.assertIn("uses real credentials", forbidden)

    def test_templates_require_observable_results_and_recovery(self) -> None:
        readme = (PRIVATE / "assets/skill-readme-template.md").read_text(encoding="utf-8")
        onboarding = (PRIVATE / "assets/marketplace-onboarding-template.md").read_text(encoding="utf-8")
        self.assertIn("Expected result", readme)
        self.assertIn("Verification", readme)
        self.assertIn("First verified success", onboarding)
        self.assertIn("rollback", onboarding.casefold())


if __name__ == "__main__":
    unittest.main()
