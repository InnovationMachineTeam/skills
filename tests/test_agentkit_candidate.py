#!/usr/bin/env python3
"""Candidate-only, donor-lock, E2E, and approval gates for agentkit."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "candidates" / "agentkit"
DONORS = {
    "agent-architect", "agent-best-practices", "agent-builder", "agent-context",
    "agent-doctor", "agent-evaluator", "agent-manager", "agent-optimizer",
    "agent-refactor", "agent-scout",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class AgentkitCandidateTests(unittest.TestCase):
    def test_candidate_is_not_discoverable_or_packaged(self) -> None:
        self.assertTrue((CANDIDATE / "SKILL.md").is_file())
        self.assertFalse((ROOT / "skills/agent-skills/agentkit/SKILL.md").exists())
        catalog = {item["name"] for item in load(ROOT / "catalog/entries.json")["entries"]}
        self.assertNotIn("agentkit", catalog)
        self.assertFalse((ROOT / "plugins/agentkit").exists())
        for path in (
            ROOT / ".claude-plugin/marketplace.json",
            ROOT / ".agents/plugins/marketplace.json",
            ROOT / ".cursor-plugin/marketplace.json",
        ):
            self.assertNotIn("agentkit", {item["name"] for item in load(path)["plugins"]})

    def test_lock_and_vendor_are_exact_and_read_only(self) -> None:
        manifest = load(CANDIDATE / "donors.json")
        self.assertEqual(DONORS, {item["name"] for item in manifest["donors"]})
        self.assertEqual(10, len(manifest["donors"]))
        self.assertFalse(any((CANDIDATE / "vendor").rglob("SKILL.md")))
        script = CANDIDATE / "scripts/check_donors.py"
        result = subprocess.run([
            str(script), "--manifest", str(CANDIDATE / "donors.json"),
            "--vendor-root", str(CANDIDATE / "vendor"),
            "--source-root", str(ROOT / "skills/agent-skills"),
        ], check=False, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        with tempfile.TemporaryDirectory() as directory:
            drift = load(CANDIDATE / "donors.json")
            drift["donors"][0]["vendor_tree_sha256"] = "sha256:drift"
            path = Path(directory) / "donors.json"
            path.write_text(json.dumps(drift), encoding="utf-8")
            result = subprocess.run([
                str(script), "--manifest", str(path), "--vendor-root", str(CANDIDATE / "vendor")
            ], check=False)
            self.assertEqual(2, result.returncode)

    def test_routing_is_explicit_and_does_not_claim_direct_agent_tasks(self) -> None:
        routing = load(CANDIDATE / "evals/routing.json")["cases"]
        self.assertTrue(any(item["expected_trigger"] is True and item["expected_route"] == "e2e" for item in routing))
        negatives = [item for item in routing if item["expected_trigger"] is False]
        self.assertTrue(negatives)
        self.assertTrue(all(item.get("expected_route") for item in negatives))
        body = (CANDIDATE / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("explicit `$agentkit` invocation", body)
        self.assertIn("Ask for explicit approval", (CANDIDATE / "references/e2e-contract.md").read_text(encoding="utf-8"))

    def test_e2e_scaffold_and_false_completion_gate(self) -> None:
        scaffold = CANDIDATE / "scripts/scaffold_e2e_run.py"
        validate = CANDIDATE / "scripts/validate_e2e_run.py"
        with tempfile.TemporaryDirectory() as directory:
            run = Path(directory) / "run-1"
            result = subprocess.run([
                str(scaffold), "--output", str(run), "--scope", "workflow",
                "--task", "design and evaluate a software architect agent",
            ], check=False, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(0, subprocess.run([str(validate), str(run)], check=False).returncode)
            cases = load(run / "cases.json")["cases"]
            self.assertEqual({"scout", "context", "architect", "evaluate", "manage"}, {item["command"] for item in cases})
            runner = CANDIDATE / "scripts/run_router_fixture.py"
            self.assertEqual(0, subprocess.run([
                str(runner), "--run", str(run), "--manifest", str(CANDIDATE / "donors.json")
            ], check=False).returncode)
            self.assertEqual(0, subprocess.run([str(validate), str(run)], check=False).returncode)
            completed = load(run / "run-state.json")
            self.assertEqual("PASS", completed["verdict"])
            self.assertFalse(completed["real_workflow_observation"])
            self.assertTrue(all(load(run / item["output_locator"])["canonical_donor_modified"] is False for item in completed["cases"]))
            self.assertNotEqual(0, subprocess.run([
                str(runner), "--run", str(run), "--manifest", str(CANDIDATE / "donors.json")
            ], check=False).returncode)
            run = Path(directory) / "run-false-completion"
            self.assertEqual(0, subprocess.run([
                str(scaffold), "--output", str(run), "--scope", "command", "--command", "status"
            ], check=False).returncode)
            state = load(run / "run-state.json")
            state["verdict"] = "PASS"
            (run / "run-state.json").write_text(json.dumps(state), encoding="utf-8")
            self.assertNotEqual(0, subprocess.run([str(validate), str(run)], check=False).returncode)
            state["verdict"] = "INCONCLUSIVE"
            state["cases"][0].update({"status": "completed", "verdict": "PASS", "output_locator": "../escape.json"})
            (run / "run-state.json").write_text(json.dumps(state), encoding="utf-8")
            self.assertNotEqual(0, subprocess.run([str(validate), str(run)], check=False).returncode)

    def test_real_workflow_and_release_contracts_fail_closed(self) -> None:
        scaffold = CANDIDATE / "scripts/scaffold_e2e_run.py"
        finalize = CANDIDATE / "scripts/record_real_workflow.py"
        verify = CANDIDATE / "scripts/verify_release_contracts.py"
        rollback = CANDIDATE / "scripts/build_rollback_plan.py"
        self.assertEqual(0, subprocess.run([
            str(verify), "--pack-root", str(CANDIDATE), "--repository-root", str(ROOT)
        ], check=False).returncode)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run = root / "run"
            self.assertEqual(0, subprocess.run([
                str(scaffold), "--output", str(run), "--scope", "command", "--command", "status",
                "--task", "report the exact agentkit donor lock state",
            ], check=False).returncode)
            spec = root / "spec.json"
            spec.write_text(json.dumps({
                "schema_version": 1,
                "workflow_id": "synthetic-relabel",
                "task": "report the exact agentkit donor lock state",
                "execution_context": {"executor": "test", "semantic_execution": True},
                "cases": [{"case_id": "e2e-01-status", "output_locator": "raw/e2e-01-status.json"}],
                "outcome": {"verdict": "PASS", "observable_result": "status reported"},
            }), encoding="utf-8")
            runner = CANDIDATE / "scripts/run_router_fixture.py"
            self.assertEqual(0, subprocess.run([
                str(runner), "--run", str(run), "--manifest", str(CANDIDATE / "donors.json")
            ], check=False).returncode)
            self.assertNotEqual(0, subprocess.run([
                str(finalize), "--run", str(run), "--manifest", str(CANDIDATE / "donors.json"), "--spec", str(spec)
            ], check=False).returncode)
            plan = root / "rollback.json"
            self.assertEqual(0, subprocess.run([
                str(rollback), "--manifest", str(CANDIDATE / "donors.json"), "--output", str(plan),
                "--reason", "release rehearsal",
            ], check=False).returncode)
            payload = load(plan)
            self.assertEqual("direct-donor-dispatch", payload["fallback_mode"])
            self.assertFalse(payload["mutates_host"])
            self.assertEqual(10, len(payload["routes"]))

    def test_donor_finding_requires_matching_user_approval(self) -> None:
        classify = CANDIDATE / "scripts/classify_e2e_findings.py"
        render = CANDIDATE / "scripts/render_improvement_prompt.py"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            findings = root / "findings.json"
            classification = root / "classification.json"
            findings.write_text(json.dumps({
                "schema_version": 1,
                "run_id": "run-approval",
                "findings": [{
                    "id": "donor-1", "owner": "agent-optimizer", "kind": "improvement",
                    "severity": "MEDIUM", "evidence": "Comparable output missed one invariant",
                    "proposed_change": "Preserve the invariant in optimization reports",
                }],
            }), encoding="utf-8")
            self.assertEqual(0, subprocess.run([
                str(classify), "--findings", str(findings), "--manifest", str(CANDIDATE / "donors.json"),
                "--output", str(classification),
            ], check=False).returncode)
            decision = load(classification)["decisions"][0]
            self.assertEqual("ask-user-then-dispatch", decision["action"])
            self.assertEqual("optimize-existing", decision["scenario"])

            denied = root / "denied.json"
            denied.write_text(json.dumps({"status": "denied"}), encoding="utf-8")
            prompt = root / "improve.md"
            base_args = [
                str(render), "--classification", str(classification), "--finding-id", "donor-1",
                "--candidate-destination", str(root / "staged-agent-optimizer"), "--output", str(prompt),
            ]
            self.assertNotEqual(0, subprocess.run(base_args + ["--approval", str(denied)], check=False).returncode)
            self.assertFalse(prompt.exists())

            approved = root / "approved.json"
            approved.write_text(json.dumps({
                "status": "approved",
                "finding_id": "donor-1",
                "donor": "agent-optimizer",
                "scope": decision["approval"]["scope"],
                "subject": decision["approval"]["subject"],
                "source": "user approval in the active task",
            }), encoding="utf-8")
            self.assertEqual(0, subprocess.run(base_args + ["--approval", str(approved)], check=False).returncode)
            text = prompt.read_text(encoding="utf-8")
            self.assertIn("optimize-existing", text)
            self.assertIn("canonical and vendored donor sources: read-only", text)
            self.assertIn("installation, replacement, publication and retirement: unauthorized", text)


if __name__ == "__main__":
    unittest.main()
