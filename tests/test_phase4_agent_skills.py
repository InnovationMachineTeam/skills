#!/usr/bin/env python3
"""Forward and adversarial tests for Phase 4 agent-team metaskills."""

from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    assert spec and spec.loader
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


MODEL = module("phase4_model", "skills/metaskills/agent-model-selector/scripts/validate_model_policy.py")
ARCHITECT = module("phase4_architect", "skills/metaskills/agent-team-architect/scripts/validate_team_spec.py")
MAPPER = module("phase4_mapper", "skills/metaskills/agent-skill-mapper/scripts/validate_mapping.py")
BUILDER = module("phase4_builder", "skills/metaskills/agent-team-builder/scripts/validate_build_manifest.py")
MANAGER = module("phase4_manager", "skills/metaskills/agent-team-manager/scripts/validate_run_state.py")


def role(role_id: str, kind: str) -> dict:
    return {
        "id": role_id,
        "kind": kind,
        "mission": f"Own {role_id}",
        "non_goals": [],
        "boundary_evidence": [f"{role_id} has a distinct write or verification boundary"],
        "inputs": [],
        "outputs": [],
        "tools": [],
        "permissions": [],
        "data_classes": [],
        "model_policy_ref": f"model-policy://project/{role_id}@1.0.0",
        "write_set": [],
        "budgets": {"max_capabilities": 4},
        "stop_conditions": [],
        "escalation": [],
        "accountable_owner": "team",
    }


class Phase4AgentSkillTests(unittest.TestCase):
    def test_model_policy_requires_current_evidence_and_benchmark(self) -> None:
        policy = {
            "schema_version": 1,
            "policy_id": "model-policy://project/reviewer",
            "version": "1.0.0",
            "checked_at": "2026-07-31",
            "next_review_at": "2026-08-31",
            "accountable_owner": "team",
            "target_hosts": ["codex"],
            "sources": [{"id": "official", "url": "https://example.test", "authority": "official", "checked_at": "2026-07-31", "claims": ["availability"]}],
            "roles": [{"id": "reviewer", "risk_tier": "R1", "decision": "RECOMMEND", "preferred": "model-a", "task_classes": ["review"], "requirements": ["coding"], "fallback": [], "escalate_when": [], "stop_when": [], "evidence_refs": ["official"], "benchmark_refs": ["eval://reviewer-v1"]}],
            "re_evaluate_on": ["model_deprecation"],
        }
        self.assertEqual([], MODEL.validate(policy))
        unsafe = copy.deepcopy(policy)
        unsafe["roles"][0]["benchmark_refs"] = []
        self.assertTrue(any("benchmark" in item for item in MODEL.validate(unsafe)))

    def test_team_architect_enforces_boundary_evidence_and_private_owner(self) -> None:
        spec = {
            "schema_version": 1,
            "id": "asset://project/team/review",
            "name": "review",
            "version": "1.0.0",
            "status": "candidate",
            "accountable_owner": "team",
            "goal": "Review safely",
            "non_goals": [],
            "risk_tier": "R1",
            "roles": [role("lead", "orchestrator"), role("verifier", "verifier")],
            "workflow": {"pattern": "sequential", "stages": [{"id": "lead", "role_ref": "lead", "depends_on": [], "artifact_outputs": []}, {"id": "verify", "role_ref": "verifier", "depends_on": ["lead"], "artifact_outputs": []}], "integration_owner_ref": "lead", "conflict_policy": "single writer", "cancellation": "checkpoint", "partial_failure": "rollback"},
            "capability_placement": [{"capability": "private-check", "decision": "PRIVATE_SKILL", "owner_agent_ref": "lead", "allowed_consumers": ["lead"], "rationale": "one consumer"}],
            "model_policy_refs": [],
            "worktree_policy": "none",
            "human_checkpoints": [],
            "evaluation": ["end-to-end"],
            "rollback": ["disable"],
            "retirement": ["drain"],
        }
        self.assertEqual([], ARCHITECT.validate(spec))
        unsafe = copy.deepcopy(spec)
        unsafe["capability_placement"][0]["allowed_consumers"] = ["lead", "verifier"]
        self.assertTrue(any("private owner/consumer" in item for item in ARCHITECT.validate(unsafe)))

    def test_mapper_rejects_cross_owner_private_binding_and_budget_overflow(self) -> None:
        registry = {"assets": [
            {"id": "asset://project/agent/a", "kind": "agent"},
            {"id": "asset://project/agent/b", "kind": "agent"},
            {"id": "asset://project/skill/a-only", "kind": "skill", "visibility": "private", "owner_agent_ref": "asset://project/agent/a", "allowed_consumers": ["asset://project/agent/a"], "lifecycle": "verified"},
        ]}
        proposal = {"schema_version": 1, "registry_revision": "1", "map_revision": "1", "agents": [{"agent_ref": "asset://project/agent/a", "max_capabilities": 1, "recommendations": [{"capability_ref": "asset://project/skill/a-only", "decision": "MATCH", "evidence": ["eval://a"]}]}]}
        self.assertEqual([], MAPPER.validate(proposal, registry))
        unsafe = copy.deepcopy(proposal)
        unsafe["agents"][0]["agent_ref"] = "asset://project/agent/b"
        self.assertTrue(any("private ownership" in item for item in MAPPER.validate(unsafe, registry)))
        overflow = copy.deepcopy(proposal)
        overflow["agents"][0]["max_capabilities"] = 0
        self.assertTrue(any("budget" in item for item in MAPPER.validate(overflow, registry)))

    def test_builder_requires_approved_digest_and_blocks_private_packaging(self) -> None:
        manifest = {
            "schema_version": 1,
            "build_id": "build://review-v1",
            "spec": {"id": "asset://project/team/review", "version": "1.0.0", "status": "approved", "hash": "sha256:" + "a" * 64},
            "destination": ".agents/staging/review",
            "activation": False,
            "expected_revisions": {"registry": "1", "map": "1"},
            "operations": [{"action": "create", "path": ".agents/definitions/reviewer/skills/private-check/SKILL.md", "visibility": "private", "owner_agent_ref": "asset://project/agent/reviewer", "allowed_consumers": ["asset://project/agent/reviewer"], "collision_policy": "absent"}],
            "validations": ["schema", "private-boundary"],
            "rollback": {"backup_path": ".agents/backups/review-v1", "procedure": "restore exact write-set"},
        }
        self.assertEqual([], BUILDER.validate(manifest))
        unsafe = copy.deepcopy(manifest)
        unsafe["operations"][0]["path"] = "skills/metaskills/private-check/SKILL.md"
        failures = BUILDER.validate(unsafe)
        self.assertTrue(any("outside owner" in item or "package" in item for item in failures), failures)

    def test_manager_requires_resumable_checkpoint_and_bounded_budget(self) -> None:
        state = {
            "schema_version": 1,
            "run_id": "run://review/1",
            "team_ref": "asset://project/team/review@1.0.0",
            "spec_ref": "asset://project/team/review@1.0.0#sha256:a",
            "accountable_owner": "team",
            "workflow": "design-build-evaluate",
            "authority_scope": "repository write only",
            "phase": "build",
            "status": "RUNNING",
            "handoffs": [],
            "checkpoints": ["checkpoint://review/build-1"],
            "artifacts": [],
            "expected_revisions": {"registry": "1", "map": "1"},
            "budgets": {"max_steps": 12, "max_retries": 2},
            "risks": [],
            "next_action": "validate staged build",
            "rollback": {"procedure": "restore staged manifest"},
            "created_at": "2026-07-31T00:00:00Z",
            "updated_at": "2026-07-31T00:00:00Z",
        }
        self.assertEqual([], MANAGER.validate(state))
        unsafe = copy.deepcopy(state)
        unsafe["checkpoints"] = []
        self.assertTrue(any("checkpoint" in item for item in MANAGER.validate(unsafe)))


if __name__ == "__main__":
    unittest.main()
