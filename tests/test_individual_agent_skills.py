#!/usr/bin/env python3
"""Structural, routing and deterministic forward gates for individual-agent skills."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "agent-architect",
    "agent-best-practices",
    "agent-builder",
    "agent-context",
    "agent-doctor",
    "agent-evaluator",
    "agent-manager",
    "agent-optimizer",
    "agent-refactor",
    "agent-scout",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class IndividualAgentSkillTests(unittest.TestCase):
    def test_all_requested_donors_are_versioned_and_agentkit_is_deferred(self) -> None:
        root = ROOT / "skills" / "agent-skills"
        for name in SKILLS:
            text = (root / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(f"name: {name}", text)
            self.assertIn('version: "1.0.0"', text)
            self.assertIn(f"${name}", (root / name / "agents" / "openai.yaml").read_text(encoding="utf-8"))
        self.assertFalse((root / "agentkit" / "SKILL.md").exists())
        self.assertTrue((ROOT / "docs" / "prompts" / "agentkit-composite-skill.md").is_file())

    def test_each_skill_has_positive_negative_and_behavior_cases(self) -> None:
        prompts: list[str] = []
        for name in SKILLS:
            skill = ROOT / "skills" / "agent-skills" / name
            routing = load(skill / "evals" / "routing.json")
            behavior = load(skill / "evals" / "behavior.json")
            cases = routing["cases"]
            self.assertTrue(any(case["expected_trigger"] is True for case in cases), name)
            self.assertTrue(any(case["expected_trigger"] is False for case in cases), name)
            self.assertTrue(all(case.get("split") in {"train", "validation", "regression"} for case in cases), name)
            self.assertTrue(all(case.get("grader") for case in cases), name)
            self.assertTrue(all(case.get("expected_route") for case in cases if case["expected_trigger"] is False), name)
            self.assertGreaterEqual(len(behavior["cases"]), 3, name)
            self.assertTrue(all(case.get("split") in {"train", "validation", "regression"} for case in behavior["cases"]), name)
            self.assertTrue(all(case.get("grader") for case in behavior["cases"]), name)
            prompts.extend(case["input"].casefold() for case in cases)
        self.assertEqual(len(prompts), len(set(prompts)))

    def test_single_agent_boundaries_name_team_and_os_neighbors(self) -> None:
        architect = (ROOT / "skills/agent-skills/agent-architect/SKILL.md").read_text(encoding="utf-8")
        builder = (ROOT / "skills/agent-skills/agent-builder/SKILL.md").read_text(encoding="utf-8")
        evaluator = (ROOT / "skills/agent-skills/agent-evaluator/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("agent-team-architect", architect)
        self.assertIn("agent-os-architect", architect)
        self.assertIn("agent-team-manager", builder)
        self.assertIn("agent-os-evaluator", evaluator)

    def test_documentation_schema_accepts_contract_and_rejects_escape(self) -> None:
        script = ROOT / "skills/agent-skills/agent-architect/scripts/validate_agent_candidate.py"
        candidate = {
            "schema_version": 1,
            "id": "asset://project/agent/software-architect",
            "name": "software-architect",
            "version": "1.0.0",
            "accountable_owner": "architecture-team",
            "mission": {"goal": "Propose software architecture decisions", "non_goals": []},
            "risk_tier": "R1",
            "model_policy": {},
            "tools": ["read", "write-docs"],
            "permissions": ["docs:write"],
            "documentation": {
                "read_roots": ["docs/architecture"],
                "write_roots": ["docs/decisions/architecture"],
                "artifacts": [],
                "indexes_to_update": ["docs/decisions/README.md"],
                "freshness_rules": ["review on architecture change"],
                "validation": ["human accepts high-impact ADR"],
            },
            "runtime": {},
            "lifecycle": {},
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "agent.json"
            path.write_text(json.dumps(candidate), encoding="utf-8")
            self.assertEqual(0, subprocess.run([str(script), str(path)], check=False).returncode)
            candidate["documentation"]["write_roots"] = ["docs/../outside"]
            path.write_text(json.dumps(candidate), encoding="utf-8")
            self.assertNotEqual(0, subprocess.run([str(script), str(path)], check=False).returncode)
            candidate["documentation"]["write_roots"] = ["docs/decisions/architecture"]
            candidate["documentation"]["artifacts"] = [{"type": "adr", "path_pattern": "docs/decisions/architecture/*.md"}]
            path.write_text(json.dumps(candidate), encoding="utf-8")
            self.assertNotEqual(0, subprocess.run([str(script), str(path)], check=False).returncode)

    def test_eval_plan_requires_protected_holdout_and_layer_criteria(self) -> None:
        script = ROOT / "skills/agent-skills/agent-evaluator/scripts/validate_agent_eval_plan.py"
        plan = {
            "schema_version": 1,
            "evaluation_id": "software-architect-v1",
            "target": {"id": "asset://project/agent/software-architect", "version": "1.0.0", "hash": "sha256:test"},
            "environment": {"host": "codex"},
            "authority": {"read": True, "write": False},
            "layers": ["routing", "documentation"],
            "acceptance": {"criteria": {"routing": "all blocking cases pass", "documentation": "all blocking cases pass"}},
            "holdout_policy": {"protected": True},
            "artifacts": {"raw_output_dir": "work/evals"},
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            path.write_text(json.dumps(plan), encoding="utf-8")
            self.assertEqual(0, subprocess.run([str(script), str(path)], check=False).returncode)
            del plan["acceptance"]["criteria"]["documentation"]
            path.write_text(json.dumps(plan), encoding="utf-8")
            self.assertNotEqual(0, subprocess.run([str(script), str(path)], check=False).returncode)

    def test_corpus_and_portfolio_state_validators_pass(self) -> None:
        corpus = ROOT / "skills/agent-skills/agent-best-practices"
        self.assertEqual(0, subprocess.run([str(corpus / "scripts/validate_corpus.py"), str(corpus)], check=False).returncode)
        builder = ROOT / "skills/agent-skills/agent-builder/scripts/validate_agent_build_state.py"
        state = load(ROOT / "docs/AGENT-SKILLS-PORTFOLIO-STATE.json")
        state["builder"] = "agent-builder"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            path.write_text(json.dumps(state), encoding="utf-8")
            self.assertEqual(0, subprocess.run([str(builder), str(path)], check=False).returncode)
            state["phases"][0]["evidence"] = []
            path.write_text(json.dumps(state), encoding="utf-8")
            self.assertNotEqual(0, subprocess.run([str(builder), str(path)], check=False).returncode)
            state["phases"][0]["status"] = "pending"
            state["status"] = "completed"
            path.write_text(json.dumps(state), encoding="utf-8")
            self.assertNotEqual(0, subprocess.run([str(builder), str(path)], check=False).returncode)

    def test_portfolio_eval_fixture_harness_passes(self) -> None:
        harness = ROOT / "scripts/validate_individual_agent_evals.py"
        self.assertEqual(0, subprocess.run([str(harness), str(ROOT)], check=False).returncode)


if __name__ == "__main__":
    unittest.main()
