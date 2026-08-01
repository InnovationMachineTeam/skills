#!/usr/bin/env python3
"""Portfolio collision and selective-package gates for the private canary."""

from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT_OS_SKILLS = {
    "agent-model-router",
    "agent-observer",
    "agent-os-architect",
    "agent-os-bootstrapper",
    "agent-os-evaluator",
    "agent-policy-manager",
    "agent-protocol-manager",
    "agent-registry-manager",
    "agent-runtime-manager",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def frontmatter_value(path: Path, key: str) -> str:
    text = path.read_text(encoding="utf-8")
    block = text.split("\n---\n", 1)[0].removeprefix("---\n")
    match = re.search(rf"^\s*{re.escape(key)}:\s*(.*?)\s*$", block, re.MULTILINE)
    if not match:
        raise AssertionError(f"missing {key} in {path}")
    return match.group(1).strip().strip("\"'")


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(
        item
        for item in root.rglob("*")
        if item.is_file()
        and "__pycache__" not in item.parts
        and item.suffix not in {".pyc", ".pyo"}
        and item.name != ".DS_Store"
    ):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


class PortfolioReleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_dirs = {
            path.parent.name: path.parent
            for path in (ROOT / "skills").glob("*/*/SKILL.md")
        }
        self.catalog = load(ROOT / "catalog" / "entries.json")["entries"]

    def test_names_descriptions_and_catalog_are_collision_free(self) -> None:
        names = list(self.skill_dirs)
        descriptions = [frontmatter_value(path / "SKILL.md", "description") for path in self.skill_dirs.values()]
        catalog_names = [entry["name"] for entry in self.catalog]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(descriptions), len(set(descriptions)))
        self.assertEqual(len(catalog_names), len(set(catalog_names)))
        self.assertEqual(set(names), set(catalog_names))
        self.assertTrue(any(name.startswith("skill-") for name in names))
        self.assertTrue(any(name.startswith("agent-") for name in names))

    def test_catalog_categories_match_canonical_layout(self) -> None:
        configured = {entry["name"]: entry["category"] for entry in self.catalog}
        actual = {name: path.parent.name for name, path in self.skill_dirs.items()}
        self.assertEqual(actual, configured)
        self.assertEqual(
            {"agent-master", "agent-os-skills", "agent-team-skills", "agent-skills", "metaskills", "prompt-skills"},
            set(actual.values()),
        )
        self.assertEqual("prompt-skills", actual["prompt-optimize"])
        self.assertNotIn("optimize-prompts", actual)
        self.assertNotIn("optimize-master-prompts", actual)

    def test_agent_os_skills_have_explicit_neighbor_non_triggers(self) -> None:
        prompts: list[str] = []
        for name in AGENT_OS_SKILLS:
            routing = load(self.skill_dirs[name] / "evals" / "routing.json")
            cases = routing["cases"]
            negative = [case for case in cases if case.get("expected_trigger") is False]
            self.assertTrue(negative, f"{name} lacks a collision/non-trigger case")
            self.assertTrue(
                all(case.get("expected_route") for case in negative),
                f"{name} must name the neighboring route for every non-trigger",
            )
            for case in cases:
                prompt = case.get("prompt") or case.get("input")
                self.assertIsInstance(prompt, str)
                prompts.append(prompt.casefold())
        self.assertEqual(len(prompts), len(set(prompts)), "routing prompts must be distinct")

    def test_openai_interfaces_use_literal_skill_invocation(self) -> None:
        for name, skill_dir in self.skill_dirs.items():
            adapter = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertIn(f"${name}", adapter, name)

    def test_registry_versions_hashes_and_provenance_match_canonical(self) -> None:
        registry = load(ROOT / "docs" / "AGENT-ASSET-REGISTRY.json")
        registered = {
            asset["name"]: asset
            for asset in registry["assets"]
            if asset.get("kind") == "skill" and asset.get("scope") == "repository"
        }
        self.assertEqual(set(self.skill_dirs), set(registered))
        for name, skill_dir in self.skill_dirs.items():
            asset = registered[name]
            self.assertEqual("public", asset["visibility"])
            self.assertEqual("global", asset["discoverability"])
            self.assertEqual("InnovationMachineTeam/skills", asset["provenance"]["repository"])
            self.assertEqual(frontmatter_value(skill_dir / "SKILL.md", "version"), asset["version"])
            self.assertEqual(tree_hash(skill_dir), asset["content_sha256"])

    def test_every_individual_package_contains_exactly_one_public_skill(self) -> None:
        package_names = {path.name for path in (ROOT / "plugins").iterdir() if path.is_dir()}
        self.assertEqual(set(self.skill_dirs), package_names)
        for name, source_dir in self.skill_dirs.items():
            package = ROOT / "plugins" / name
            bundled = list((package / "skills").glob("*/SKILL.md"))
            self.assertEqual([name], [path.parent.name for path in bundled], name)
            self.assertFalse(any(".agents" in path.parts for path in package.rglob("*")), name)
            for host in ("claude", "codex", "cursor"):
                manifest = load(package / f".{host}-plugin" / "plugin.json")
                self.assertEqual(name, manifest["name"])
                self.assertEqual(frontmatter_value(source_dir / "SKILL.md", "version"), manifest["version"])

    def test_marketplaces_offer_the_same_selective_inventory(self) -> None:
        expected = set(self.skill_dirs)
        manifests = (
            ROOT / ".claude-plugin" / "marketplace.json",
            ROOT / ".agents" / "plugins" / "marketplace.json",
            ROOT / ".cursor-plugin" / "marketplace.json",
        )
        for path in manifests:
            names = {entry["name"] for entry in load(path)["plugins"]}
            self.assertEqual(expected, names, path.as_posix())

    def test_agent_os_slice_is_independently_selectable(self) -> None:
        catalog_names = {entry["name"] for entry in self.catalog}
        self.assertTrue(AGENT_OS_SKILLS <= catalog_names)
        for name in AGENT_OS_SKILLS:
            package = ROOT / "plugins" / name
            self.assertTrue((package / ".codex-plugin" / "plugin.json").is_file())
            self.assertTrue((package / ".claude-plugin" / "plugin.json").is_file())
            self.assertTrue((package / ".cursor-plugin" / "plugin.json").is_file())


if __name__ == "__main__":
    unittest.main()
