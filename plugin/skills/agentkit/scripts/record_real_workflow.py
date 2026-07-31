#!/usr/bin/env python3
"""Finalize a semantic agentkit E2E run as a verifiable real workflow observation."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


VERDICTS = {"PASS", "FAIL", "INCONCLUSIVE", "BLOCKED", "NOT_EVALUATED"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def contained(locator: object) -> bool:
    if not isinstance(locator, str) or not locator:
        return False
    value = PurePosixPath(locator)
    return not value.is_absolute() and ".." not in value.parts


def file_hash(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--spec", type=Path, required=True)
    args = parser.parse_args()

    run = args.run.resolve()
    if not run.is_dir() or run.is_symlink():
        raise ValueError("run must be an existing real directory")
    state = load(run / "run-state.json")
    suite = load(run / "cases.json")
    manifest = load(args.manifest.resolve())
    spec = load(args.spec.resolve())
    if state.get("status") != "planned":
        raise ValueError("real workflow finalization requires a planned run")
    if spec.get("schema_version") != 1 or not spec.get("workflow_id") or not spec.get("task"):
        raise ValueError("workflow spec requires schema_version=1, workflow_id and task")
    context = spec.get("execution_context", {})
    if context.get("semantic_execution") is not True or not context.get("executor"):
        raise ValueError("workflow spec must identify a semantic executor")
    outcome = spec.get("outcome", {})
    if outcome.get("verdict") != "PASS" or not outcome.get("observable_result"):
        raise ValueError("a maturity observation requires a PASS workflow outcome and observable result")

    locked = {item.get("name"): item for item in manifest.get("donors", [])}
    cases = suite.get("cases", [])
    spec_cases = spec.get("cases", [])
    if len(cases) != len(spec_cases) or [item.get("case_id") for item in spec_cases] != [item.get("id") for item in cases]:
        raise ValueError("workflow spec cases must align exactly with the frozen suite")

    state_by_id = {item.get("id"): item for item in state.get("cases", [])}
    evidence = []
    commands = []
    for frozen, recorded in zip(cases, spec_cases):
        locator = recorded.get("output_locator")
        if not contained(locator):
            raise ValueError(f"{frozen.get('id')}: unsafe output locator")
        output_path = run / str(locator)
        output = load(output_path)
        expected_donor = frozen.get("expected_donor")
        lock = locked.get(expected_donor) if expected_donor else None
        required = {
            "case_id": frozen.get("id"),
            "command": frozen.get("command"),
            "selected_donor": expected_donor,
            "execution_kind": "semantic-donor-run",
            "real_workflow_observation": True,
            "authority_preserved": True,
            "canonical_donor_modified": False,
            "vendored_donor_modified": False,
            "verdict": "PASS",
        }
        for key, expected in required.items():
            if output.get(key) != expected:
                raise ValueError(f"{frozen.get('id')}: {key} differs from the real workflow contract")
        if lock and (output.get("donor_version") != lock.get("version") or output.get("donor_hash") != lock.get("source_tree_sha256")):
            raise ValueError(f"{frozen.get('id')}: donor identity differs from the lock")
        if not output.get("semantic_result"):
            raise ValueError(f"{frozen.get('id')}: semantic_result is required")
        locators = output.get("evidence", [])
        if not isinstance(locators, list) or not locators:
            raise ValueError(f"{frozen.get('id')}: at least one evidence locator is required")
        hashed = []
        for item in locators:
            if not contained(item) or not (run / item).is_file():
                raise ValueError(f"{frozen.get('id')}: invalid evidence locator {item!r}")
            hashed.append({"locator": item, "sha256": file_hash(run / item)})
        evidence.append({"case_id": frozen.get("id"), "output": locator, "output_sha256": file_hash(output_path), "artifacts": hashed})
        commands.append({"command": frozen.get("command"), "donor": expected_donor})
        state_by_id[frozen.get("id")].update({"status": "completed", "verdict": "PASS", "output_locator": locator})

    observed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    state.update({
        "status": "completed",
        "verdict": "PASS",
        "execution_kind": "semantic-donor-run",
        "real_workflow_observation": True,
        "workflow_id": spec["workflow_id"],
        "updated_at": observed_at,
    })
    observation = {
        "schema_version": 1,
        "workflow_id": spec["workflow_id"],
        "user_request_ref": spec.get("user_request_ref"),
        "task": spec["task"],
        "target": spec.get("target"),
        "observed_at": observed_at,
        "execution_context": context,
        "commands": commands,
        "outcome": outcome,
        "evidence": evidence,
        "donor_manifest_sha256": file_hash(args.manifest.resolve()),
    }
    (run / "run-state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (run / "workflow-observation.json").write_text(json.dumps(observation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"workflow_id": spec["workflow_id"], "commands": len(commands), "verdict": "PASS", "observed_at": observed_at}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        raise SystemExit(1)
