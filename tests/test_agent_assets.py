#!/usr/bin/env python3
"""Forward and negative tests for agent assets and generated host adapters."""

from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_agent_adapters import expected_outputs  # noqa: E402
from manage_agent_assets import content_hash, load_object, transaction, validate  # noqa: E402


FIXTURE = ROOT / "tests" / "fixtures" / "agent-assets"


class AgentAssetTests(unittest.TestCase):
    def copy_fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        target = Path(temporary.name) / "project"
        shutil.copytree(FIXTURE, target)
        return temporary, target

    def test_walking_skeleton_passes(self) -> None:
        self.assertEqual([], validate(FIXTURE, require_catalog=False))
        for path, expected in expected_outputs(FIXTURE).items():
            self.assertEqual(expected, path.read_text(encoding="utf-8"))

    def test_private_capability_denies_another_agent(self) -> None:
        temporary, target = self.copy_fixture()
        self.addCleanup(temporary.cleanup)
        mapping = load_object(target / "docs" / "AGENT-SKILLS-MAP.json")
        mapping["bindings"][1]["agent_ref"] = "asset://project/agent/other-agent@1.0.0"
        (target / "docs" / "AGENT-SKILLS-MAP.json").write_text(json.dumps(mapping), encoding="utf-8")
        failures = validate(target, check_views=False, require_catalog=False)
        self.assertTrue(any("unauthorized private capability binding" in item for item in failures), failures)

    def test_private_capability_outside_owner_root_is_rejected(self) -> None:
        temporary, target = self.copy_fixture()
        self.addCleanup(temporary.cleanup)
        source = target / ".agents/definitions/code-reviewer/skills/private-check"
        misplaced = target / ".agents/skills/private-check"
        shutil.copytree(source, misplaced)
        registry = load_object(target / "docs" / "AGENT-ASSET-REGISTRY.json")
        asset = next(item for item in registry["assets"] if item["id"].endswith("/private-check"))
        asset["locator"] = ".agents/skills/private-check"
        asset["content_sha256"] = content_hash(misplaced)
        (target / "docs" / "AGENT-ASSET-REGISTRY.json").write_text(json.dumps(registry), encoding="utf-8")
        failures = validate(target, check_views=False, require_catalog=False)
        self.assertTrue(any("outside canonical agent root" in item for item in failures), failures)

    def test_missing_private_owner_fails_closed(self) -> None:
        temporary, target = self.copy_fixture()
        self.addCleanup(temporary.cleanup)
        registry = load_object(target / "docs" / "AGENT-ASSET-REGISTRY.json")
        asset = next(item for item in registry["assets"] if item["id"].endswith("/private-check"))
        asset["owner_agent_ref"] = None
        asset["allowed_consumers"] = []
        (target / "docs" / "AGENT-ASSET-REGISTRY.json").write_text(json.dumps(registry), encoding="utf-8")
        failures = validate(target, check_views=False, require_catalog=False)
        self.assertTrue(any("private owner_agent_ref is required" in item for item in failures), failures)

    def test_capability_budget_and_map_parity_are_enforced(self) -> None:
        temporary, target = self.copy_fixture()
        self.addCleanup(temporary.cleanup)
        definition_path = target / ".agents/definitions/code-reviewer/agent.json"
        definition = load_object(definition_path)
        definition["runtime"]["budgets"]["max_capabilities"] = 2
        definition_path.write_text(json.dumps(definition), encoding="utf-8")
        registry = load_object(target / "docs" / "AGENT-ASSET-REGISTRY.json")
        agent = next(item for item in registry["assets"] if item["kind"] == "agent")
        agent["content_sha256"] = content_hash(definition_path)
        (target / "docs" / "AGENT-ASSET-REGISTRY.json").write_text(json.dumps(registry), encoding="utf-8")
        failures = validate(target, check_views=False, require_catalog=False)
        self.assertTrue(any("capability budget exceeded" in item for item in failures), failures)

    def test_generated_adapter_drift_is_detectable(self) -> None:
        temporary, target = self.copy_fixture()
        self.addCleanup(temporary.cleanup)
        adapter = target / ".codex/agents/code-reviewer.toml"
        adapter.write_text(adapter.read_text(encoding="utf-8") + "# drift\n", encoding="utf-8")
        expected = expected_outputs(target)[adapter]
        self.assertNotEqual(expected, adapter.read_text(encoding="utf-8"))

    def test_transaction_checks_revisions_and_updates_both_documents(self) -> None:
        temporary, target = self.copy_fixture()
        self.addCleanup(temporary.cleanup)
        registry = load_object(target / "docs" / "AGENT-ASSET-REGISTRY.json")
        mapping = load_object(target / "docs" / "AGENT-SKILLS-MAP.json")
        operation = {
            "schema_version": 1,
            "id": "transaction://tests/no-op",
            "expected_revisions": {"registry": registry["revision"], "map": mapping["revision"]},
            "assets": {"upsert": [], "remove": []},
            "bindings": {"upsert": [], "remove": []},
        }
        operation_path = target / "transaction.json"
        operation_path.write_text(json.dumps(operation), encoding="utf-8")
        self.assertEqual(0, transaction(target, operation_path, True))
        self.assertEqual(registry["revision"] + 1, load_object(target / "docs" / "AGENT-ASSET-REGISTRY.json")["revision"])
        self.assertEqual(mapping["revision"] + 1, load_object(target / "docs" / "AGENT-SKILLS-MAP.json")["revision"])
        self.assertEqual([], validate(target, require_catalog=False))
        with self.assertRaisesRegex(ValueError, "revision conflict"):
            transaction(target, operation_path, False)


if __name__ == "__main__":
    unittest.main()
