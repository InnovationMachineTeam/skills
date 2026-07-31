#!/usr/bin/env python3
"""Execute agentkit command routing against locked donors in an isolated fixture."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROUTES = {
    "scout": "agent-scout", "context": "agent-context", "architect": "agent-architect",
    "evaluate": "agent-evaluator", "doctor": "agent-doctor", "optimize": "agent-optimizer",
    "refactor": "agent-refactor", "manage": "agent-manager", "run": "agent-builder",
    "practices": "agent-best-practices",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    run = args.run.resolve()
    if not run.is_dir() or run.is_symlink():
        raise ValueError("run must be an existing real directory")
    manifest = load(args.manifest)
    locked = {item["name"]: item for item in manifest.get("donors", [])}
    suite = load(run / "cases.json")
    state = load(run / "run-state.json")
    if state.get("status") != "planned" or any(item.get("status") != "pending" for item in state.get("cases", [])):
        raise ValueError("router fixture only runs once from a planned state")

    raw = run / "raw"
    raw.mkdir()
    state_by_id = {item["id"]: item for item in state["cases"]}
    failures = 0
    for case in suite.get("cases", []):
        command = case["command"]
        expected = case.get("expected_donor")
        selected = ROUTES.get(command)
        verdict = "PASS"
        reasons = []
        if selected != expected:
            verdict = "FAIL"
            reasons.append("router selection differs from frozen case")
        lock = locked.get(selected) if selected else None
        if selected and not lock:
            verdict = "FAIL"
            reasons.append("selected donor missing from lock")
        output = {
            "case_id": case["id"],
            "execution_kind": "deterministic-router-fixture",
            "real_workflow_observation": False,
            "command": command,
            "selected_donor": selected,
            "donor_version": lock.get("version") if lock else None,
            "donor_hash": lock.get("source_tree_sha256") if lock else None,
            "authority_preserved": True,
            "canonical_donor_modified": False,
            "verdict": verdict,
            "reasons": reasons,
        }
        locator = f"raw/{case['id']}.json"
        (run / locator).write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        state_by_id[case["id"]].update({"status": "completed" if verdict == "PASS" else "failed", "verdict": verdict, "output_locator": locator})
        failures += verdict != "PASS"
    state["status"] = "completed" if not failures else "failed"
    state["verdict"] = "PASS" if not failures else "FAIL"
    state["execution_kind"] = "deterministic-router-fixture"
    state["real_workflow_observation"] = False
    state["updated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    (run / "run-state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(state["cases"]), "verdict": state["verdict"], "real_workflow_observation": False}))
    return 0 if not failures else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        raise SystemExit(1)
