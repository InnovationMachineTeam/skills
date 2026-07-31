#!/usr/bin/env python3
"""Forward and adversarial tests for Phase 5 runtime metaskills."""

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


ORCHESTRATOR = module("phase5_orchestrator", "skills/agent-team-skills/agent-team-orchestrator/scripts/validate_run_plan.py")
WORKSPACE = module("phase5_workspace", "skills/agent-team-skills/agent-workspace-manager/scripts/validate_workspace_ledger.py")


def node(node_id: str, depends_on: list[str], write_set: list[str]) -> dict:
    return {
        "id": node_id,
        "owner_ref": f"asset://project/agent/{node_id}",
        "depends_on": depends_on,
        "input_refs": ["artifact://input"],
        "output_refs": [f"artifact://{node_id}"],
        "write_set": write_set,
        "allowed_capabilities": ["asset://repository/skill/review"],
        "max_attempts": 2,
        "exit_gate": "tests pass",
        "checkpoint_policy": "after completion",
    }


def workspace(workspace_id: str, write_set: list[str], status: str = "ACTIVE") -> dict:
    return {
        "workspace_id": workspace_id,
        "task_id": f"task-{workspace_id}",
        "owner_agent_ref": f"asset://project/agent/{workspace_id}",
        "path": f".worktrees/{workspace_id}",
        "branch": f"agent/{workspace_id}",
        "base_revision": "a" * 40,
        "write_set": write_set,
        "lease": {"owner": workspace_id, "expires_at": "2026-08-01T00:00:00Z", "token": f"lease-{workspace_id}"},
        "quota": {"max_bytes": 1000000},
        "status": status,
        "tests": [],
        "artifacts": [],
        "cleanup": {"authorized": False, "retention": "keep branch until integration"},
    }


class Phase5RuntimeSkillTests(unittest.TestCase):
    def test_sequential_run_plan_passes(self) -> None:
        plan = {
            "schema_version": 1,
            "run_id": "run://review/1",
            "team_ref": "asset://project/team/review@1.0.0",
            "team_status": "active",
            "registry_revision": "4",
            "map_revision": "1",
            "integration_owner_ref": "asset://project/agent/lead",
            "state_locator": ".agents/state/review-1.json",
            "task": {"objective": "review change", "authority_scope": "read repository", "data_class": "internal", "idempotency_key": "review-1", "deadline": "2026-08-01T00:00:00Z", "input_refs": ["artifact://diff"], "acceptance_checks": ["findings cited"]},
            "budgets": {"max_steps": 10, "max_retries": 1, "max_parallel": 1},
            "workflow": {"pattern": "sequential", "nodes": [node("lead", [], ["reports/draft.md"]), node("verify", ["lead"], ["reports/final.md"])]},
            "verification": {"verifier_ref": "asset://project/agent/verify", "checks": ["acceptance criteria"]},
            "cancellation": {"procedure": "stop dispatch and checkpoint"},
            "recovery": {"procedure": "resume from verified checkpoint"},
        }
        self.assertEqual([], ORCHESTRATOR.validate(plan))

    def test_run_plan_rejects_cycle_stale_team_and_unverified_completion(self) -> None:
        plan = {
            "schema_version": 1, "run_id": "run://bad", "team_ref": "asset://project/team/review@1.0.0", "team_status": "approved",
            "registry_revision": "4", "map_revision": "1", "integration_owner_ref": "lead", "state_locator": ".agents/state/bad.json",
            "task": {"objective": "x", "authority_scope": "read", "data_class": "internal", "idempotency_key": "bad", "deadline": "soon", "input_refs": ["a"], "acceptance_checks": ["b"]},
            "budgets": {"max_steps": 2, "max_retries": 0, "max_parallel": 2},
            "workflow": {"pattern": "dag", "merge_protocol": "owner merge", "nodes": [node("a", ["b"], ["src/a.py"]), node("b", ["a"], ["src/b.py"])]},
            "verification": {"verifier_ref": "", "checks": []},
            "cancellation": {"procedure": "stop"}, "recovery": {"procedure": "rollback"},
        }
        failures = ORCHESTRATOR.validate(plan)
        self.assertTrue(any("active" in item for item in failures), failures)
        self.assertTrue(any("cycle" in item for item in failures), failures)
        self.assertTrue(any("verification" in item for item in failures), failures)

    def test_disjoint_workspace_ledger_passes(self) -> None:
        ledger = {
            "schema_version": 1,
            "revision": 1,
            "policy": "WORKTREE_PER_TASK",
            "repository": "InnovationMachineTeam/skills",
            "integration_owner_ref": "asset://project/agent/lead",
            "collision_policy": "stop and escalate",
            "baseline": {"revision": "a" * 40, "user_changes_preserved": True},
            "workspaces": [workspace("writer-a", ["src/a.py"]), workspace("writer-b", ["src/b.py"])],
        }
        self.assertEqual([], WORKSPACE.validate(ledger))

    def test_workspace_ledger_rejects_overlap_broad_path_and_unsafe_cleanup(self) -> None:
        ledger = {
            "schema_version": 1,
            "revision": 1,
            "policy": "WORKTREE_PER_TASK",
            "repository": "InnovationMachineTeam/skills",
            "integration_owner_ref": "lead",
            "collision_policy": "stop",
            "baseline": {"revision": "a" * 40, "user_changes_preserved": True},
            "workspaces": [workspace("a", ["src/shared.py"]), workspace("b", ["src/shared.py"])],
        }
        ledger["workspaces"][0]["path"] = "/"
        ledger["workspaces"][1]["cleanup"] = {"authorized": True, "retention": "none"}
        failures = WORKSPACE.validate(ledger)
        self.assertTrue(any("overlap" in item for item in failures), failures)
        self.assertTrue(any("path" in item for item in failures), failures)
        self.assertTrue(any("non-terminal" in item for item in failures), failures)


if __name__ == "__main__":
    unittest.main()
