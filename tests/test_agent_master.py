#!/usr/bin/env python3
"""Contracts for agent-master and the final Agentic OS specialist prompts."""
from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    assert spec and spec.loader
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


MASTER = module(
    "agent_master_state",
    "skills/agent-master/agent-master/scripts/validate_agent_master_state.py",
)
MODEL = module(
    "agent_model_router_policy",
    "skills/agent-os-skills/agent-model-router/scripts/validate_model_routing_policy.py",
)
PROTOCOL = module(
    "agent_protocol_contract",
    "skills/agent-os-skills/agent-protocol-manager/scripts/validate_protocol_contract.py",
)


def authority() -> dict:
    return {
        "write": True,
        "external_research": False,
        "install": False,
        "publish": False,
        "runtime_activate": False,
        "production": False,
        "destructive": False,
        "spend": False,
    }


class AgentMasterTests(unittest.TestCase):
    def test_master_state_accepts_bounded_dag_and_rejects_false_completion(self) -> None:
        phase_ids = [
            "analyze", "research-harness", "select-harness", "design-harness",
            "design-orchestrator", "design-role-agents", "design-role-skills",
            "implement-components", "integrate-evaluate", "improve",
            "document-handoff",
        ]
        phases = []
        for index, phase_id in enumerate(phase_ids):
            phases.append({
                "id": phase_id,
                "owner": "agent-master",
                "objective": f"Complete {phase_id}",
                "status": "completed",
                "dependencies": [] if index == 0 else [phase_ids[index - 1]],
                "entry_conditions": ["prior gate passed"],
                "required_outputs": [f"artifact://{phase_id}"],
                "exit_checks": ["artifact validates"],
                "authority": authority(),
                "retry_count": 0,
                "evidence": [f"artifact://{phase_id}"],
            })
        state = {
            "schema_version": 2,
            "master": "agent-master",
            "run_id": "agent-master-test",
            "goal": "Create one verified private Agent Harness",
            "status": "completed",
            "visibility": {
                "mode": "private",
                "selected_at": "2026-08-01T00:00:00Z",
                "selected_by": "user",
            },
            "execution_mode": "supervised",
            "scope": ["fixture"],
            "acceptance_criteria": ["end-to-end path validates"],
            "authority": authority(),
            "phases": phases,
            "components": [{
                "id": "component://private/process-orchestrator-architect",
                "kind": "skill",
                "name": "process-orchestrator-architect",
                "version": "1.0.0",
                "owner": "agent-master",
                "visibility": "package_private",
                "allowed_consumers": ["agent-master"],
                "locator": "private-skills/process-orchestrator-architect",
                "status": "Validated",
                "evidence": ["eval://process-orchestrator-architect"],
            }],
            "artifacts": [],
            "decisions": [],
            "findings": [],
            "assumptions": [],
            "human_decisions": [],
            "risks": [],
            "updated_at": "2026-08-01T00:00:00Z",
        }
        self.assertEqual([], MASTER.validate(state))
        state["phases"][-1]["status"] = "pending"
        self.assertTrue(any("completed root" in item for item in MASTER.validate(state)))

    def test_master_state_requires_user_visibility_and_closed_human_gates(self) -> None:
        phase_ids = list(MASTER.REQUIRED_PHASES)
        state = {
            "schema_version": 2,
            "master": "agent-master",
            "run_id": "visibility-test",
            "goal": "Review one harness",
            "status": "in_progress",
            "visibility": {"mode": "private", "selected_at": "now", "selected_by": "agent"},
            "execution_mode": "review-only",
            "scope": ["fixture"],
            "acceptance_criteria": ["review exists"],
            "authority": authority(),
            "phases": [{
                "id": phase_id,
                "owner": "agent-master",
                "objective": phase_id,
                "status": "pending",
                "dependencies": [],
                "entry_conditions": [],
                "required_outputs": [],
                "exit_checks": [],
                "authority": authority(),
                "retry_count": 0,
                "evidence": [],
            } for phase_id in phase_ids],
            "components": [],
            "artifacts": [],
            "decisions": [],
            "findings": [],
            "assumptions": [],
            "human_decisions": [{
                "id": "decision-visibility",
                "operation": "select visibility",
                "reason": "mandatory",
                "status": "open",
                "blocking": True,
            }],
            "risks": [],
            "updated_at": "now",
        }
        findings = MASTER.validate(state)
        self.assertTrue(any("selected_by" in item for item in findings))
        self.assertTrue(any("awaiting_human_decision" in item for item in findings))

    def test_model_policy_rejects_unapproved_fallback(self) -> None:
        policy = {
            "schema_version": 1,
            "policy_id": "model-policy-test",
            "version": "1.0.0",
            "status": "candidate",
            "mode": "tiered",
            "owner": "platform-team",
            "checked_at": "2026-08-01",
            "policy_ref": "policy://models/1",
            "rollback_ref": "policy://models/previous",
            "feature_schema": {"risk_tier": "enum"},
            "evaluation_refs": ["eval://model-routing/1"],
            "drift_signals": ["quality_floor_breach"],
            "approved_models": [{
                "ref": "model://approved/1",
                "provider": "provider",
                "model_id": "model-id",
                "version": "pinned-version",
                "evidence_ref": "evidence://provider/model-id",
                "checked_at": "2026-08-01",
                "hosts": ["host"],
                "data_classes": ["internal"],
                "tools": [],
                "modalities": ["text"],
            }],
            "routes": [{
                "id": "route-low-risk",
                "task_class": "summary",
                "risk_tier": "R1",
                "model_ref": "model://approved/1",
                "quality_floor": "eval score >= 0.9",
                "hard_stop": "no eligible model",
                "confidence_threshold": 0.8,
                "max_latency_ms": 3000,
                "max_cost_usd": 0.1,
                "fallback_refs": [],
            }],
        }
        self.assertEqual([], MODEL.validate(policy))
        policy["routes"][0]["fallback_refs"] = ["model://unapproved/2"]
        self.assertTrue(any("unapproved model" in item for item in MODEL.validate(policy)))

    def test_protocol_contract_requires_explicit_unsupported_features(self) -> None:
        contract = {
            "schema_version": 1,
            "contract_id": "protocol-contract-test",
            "version": "1.0.0",
            "status": "candidate",
            "owner": "platform-team",
            "checked_at": "2026-08-01",
            "canonical_contract_ref": "schema://agent-boundary/1",
            "upgrade_ref": "plan://protocol-upgrade/1",
            "rollback_ref": "plan://protocol-rollback/1",
            "conformance_refs": ["eval://protocol/1"],
            "adapters": [{
                "id": "adapter-mcp-host",
                "boundary": "mcp",
                "protocol": "MCP",
                "version": "pinned-version",
                "direction": "bidirectional",
                "outcome": "native",
                "authentication": "scoped-token-reference",
                "error_model": "typed-errors",
                "retry_policy": "transient-only",
                "idempotency": "request-key",
                "credential_ref": "secret://mcp/test",
                "capabilities": ["tools"],
                "unsupported_features": [],
                "schemas": ["schema://mcp/tool-call"],
                "data_classes": ["internal"],
                "conformance_cases": ["success", "denial", "disconnect"],
                "streaming": True,
                "cancellation": True,
                "provenance_required": True,
                "timeout_ms": 30000,
                "max_payload_bytes": 1000000,
                "retry_budget": 2,
            }],
        }
        self.assertEqual([], PROTOCOL.validate(contract))
        contract["adapters"][0]["outcome"] = "unsupported"
        self.assertTrue(any("requires unsupported_features" in item for item in PROTOCOL.validate(contract)))

    def test_new_skills_have_neighbor_routes_and_no_placeholders(self) -> None:
        roots = (
            ROOT / "skills/agent-master/agent-master",
            ROOT / "skills/agent-os-skills/agent-model-router",
            ROOT / "skills/agent-os-skills/agent-protocol-manager",
        )
        for root in roots:
            text = (root / "SKILL.md").read_text(encoding="utf-8")
            self.assertNotIn("TODO", text)
            routing = json.loads((root / "evals/routing.json").read_text(encoding="utf-8"))
            self.assertTrue(any(case.get("expected_trigger") is True for case in routing["cases"]))
            self.assertTrue(any(case.get("expected_trigger") is False for case in routing["cases"]))
            self.assertTrue(all(case.get("expected_route") for case in routing["cases"]))

    def test_agent_master_private_subskills_are_complete_and_parent_only(self) -> None:
        master = ROOT / "skills/agent-master/agent-master"
        registry = json.loads((master / "references/private-skill-registry.json").read_text(encoding="utf-8"))
        self.assertEqual("package_private", registry["visibility"])
        self.assertEqual(["agent-master"], registry["allowed_consumers"])
        self.assertEqual(4, len(registry["skills"]))
        for item in registry["skills"]:
            root = master / item["locator"]
            self.assertTrue((root / "SKILL.md").is_file())
            self.assertTrue((root / "references/output-contract.md").is_file())
            self.assertTrue((root / "evals/routing.json").is_file())
            self.assertTrue((root / "evals/behavior.json").is_file())
            self.assertFalse((root / "agents/openai.yaml").exists())
            text = (root / "SKILL.md").read_text(encoding="utf-8")
            self.assertNotIn("TODO", text)
            self.assertIn(f'metadata:\n  version: "{item["version"]}"', text)
            routing = json.loads((root / "evals/routing.json").read_text(encoding="utf-8"))
            self.assertTrue(any(case["expected_trigger"] is True for case in routing["cases"]))
            self.assertTrue(any(case["expected_trigger"] is False for case in routing["cases"]))

    def test_agent_master_declares_mandatory_visibility_and_private_pipeline(self) -> None:
        text = (ROOT / "skills/agent-master/agent-master/SKILL.md").read_text(encoding="utf-8")
        first_question = "Which structure mode should be used: public or private?"
        self.assertIn(first_question, text)
        for name in (
            "process-orchestrator-architect",
            "role-agent-architect",
            "role-skill-architect",
            "skill-implementation-engineer",
        ):
            self.assertIn(f"private-skills/{name}/SKILL.md", text)


if __name__ == "__main__":
    unittest.main()
