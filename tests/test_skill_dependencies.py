#!/usr/bin/env python3
"""Dependency graph, runtime warning, and generated package gates."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location(
    "manage_skill_dependencies", ROOT / "scripts" / "manage_skill_dependencies.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SkillDependencyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.document = json.loads((ROOT / "catalog" / "dependencies.json").read_text(encoding="utf-8"))
        self.graph = self.document["skills"]

    def test_dependency_graph_is_valid_and_intentionally_bounded(self) -> None:
        self.assertEqual([], MODULE.validate_graph(ROOT))
        self.assertEqual(
            {
                "agent-architect",
                "agent-builder",
                "agent-context",
                "agent-doctor",
                "agent-manager",
                "agent-master",
                "agent-model-router",
                "agent-optimizer",
                "agent-protocol-manager",
                "agent-refactor",
                "agent-scout",
                "agent-team-manager",
                "prompt-master",
                "skill-builder",
            },
            set(self.graph),
        )
        self.assertEqual(
            {"claude-code": True, "codex": False, "cursor": False},
            self.document["policy"]["native_plugin_dependencies"],
        )

    def test_required_install_plan_is_dependency_first_and_unique(self) -> None:
        plan = MODULE.ordered_plan(self.graph, "skill-builder")
        self.assertEqual("skill-builder", plan[-1])
        self.assertEqual(len(plan), len(set(plan)))
        self.assertEqual(
            {item["name"] for item in self.graph["skill-builder"]["required"]},
            set(plan[:-1]),
        )

    def test_recommended_dependencies_are_opt_in(self) -> None:
        required = MODULE.ordered_plan(self.graph, "agent-team-manager")
        expanded = MODULE.ordered_plan(self.graph, "agent-team-manager", include_recommended=True)
        self.assertNotIn("agent-workspace-manager", required)
        self.assertIn("agent-workspace-manager", expanded)

    def test_missing_or_outdated_required_companions_produce_visible_warning(self) -> None:
        declaration = self.graph["agent-team-manager"]
        missing, outdated = MODULE.required_findings(
            declaration,
            {"agent-model-selector": "0.9.0"},
        )
        warning = MODULE.warning_text(missing, outdated)
        self.assertTrue(missing)
        self.assertEqual(["agent-model-selector=0.9.0<1.0.0"], outdated)
        self.assertIn("DEPENDENCY WARNING", warning)
        self.assertIn("Missing required companion plugins", warning)
        self.assertIn("Outdated required companion plugins", warning)

    def test_generated_runtime_references_are_current_and_linked(self) -> None:
        self.assertEqual([], MODULE.render_references(ROOT, check=True))
        for name in self.graph:
            skill = next((ROOT / "skills").glob(f"*/{name}/SKILL.md"))
            reference = skill.parent / "references" / "skill-dependencies.md"
            self.assertIn("DEPENDENCY WARNING", reference.read_text(encoding="utf-8"))
            self.assertIn("references/skill-dependencies.md", skill.read_text(encoding="utf-8"))

    def test_generated_packages_warn_and_match_canonical_declarations(self) -> None:
        catalog = json.loads((ROOT / "catalog" / "entries.json").read_text(encoding="utf-8"))["entries"]
        for entry in catalog:
            name = entry["name"]
            package = ROOT / "plugins" / name
            metadata = package / "skill-dependencies.json"
            if name in self.graph:
                payload = json.loads(metadata.read_text(encoding="utf-8"))
                self.assertEqual(self.graph[name]["required"], payload["required"])
                self.assertEqual(self.graph[name]["recommended"], payload["recommended"])
                self.assertIn("DEPENDENCY WARNING", (package / "README.md").read_text(encoding="utf-8"))
                claude = json.loads((package / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
                self.assertEqual([item["name"] for item in self.graph[name]["required"]], claude.get("dependencies", []))
                for host in ("codex", "cursor"):
                    manifest = json.loads((package / f".{host}-plugin" / "plugin.json").read_text(encoding="utf-8"))
                    self.assertNotIn("dependencies", manifest)
            else:
                self.assertFalse(metadata.exists(), name)


if __name__ == "__main__":
    unittest.main()
