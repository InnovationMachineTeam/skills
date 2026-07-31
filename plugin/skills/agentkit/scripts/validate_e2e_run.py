#!/usr/bin/env python3
"""Validate agentkit E2E plans, case state, findings, and false completion."""

from __future__ import annotations

import json
import sys
from pathlib import Path, PurePosixPath


CASE_STATUSES = {"pending", "running", "completed", "failed", "blocked", "not_evaluated"}
VERDICTS = {"PASS", "FAIL", "INCONCLUSIVE", "BLOCKED", "NOT_EVALUATED"}
FINDING_OWNERS = {"agentkit", "environment", "test"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def contained(locator: str) -> bool:
    path = PurePosixPath(locator)
    return not path.is_absolute() and ".." not in path.parts and bool(path.parts)


def validate(run: Path) -> list[str]:
    failures = []
    try:
        plan = load(run / "evaluation-plan.json")
        suite = load(run / "cases.json")
        state = load(run / "run-state.json")
        findings_doc = load(run / "findings.json")
    except (OSError, json.JSONDecodeError) as exc:
        return [str(exc)]
    cases = suite.get("cases", [])
    states = state.get("cases", [])
    if not cases or len(cases) != len(states):
        failures.append("cases and run-state must be non-empty and aligned")
    ids = [item.get("id") for item in cases]
    if len(ids) != len(set(ids)) or None in ids:
        failures.append("case ids must be present and unique")
    if set(plan.get("commands", [])) != {item.get("command") for item in cases}:
        failures.append("plan command coverage differs from cases")
    state_by_id = {item.get("id"): item for item in states}
    for case in cases:
        item = state_by_id.get(case.get("id"), {})
        if item.get("status") not in CASE_STATUSES:
            failures.append(f"{case.get('id')}: invalid status")
        if item.get("verdict") not in VERDICTS:
            failures.append(f"{case.get('id')}: invalid verdict")
        locator = item.get("output_locator")
        if item.get("status") == "completed":
            if not isinstance(locator, str) or not contained(locator) or not (run / locator).is_file():
                failures.append(f"{case.get('id')}: completed case needs a contained output file")
        if item.get("verdict") == "PASS" and item.get("status") != "completed":
            failures.append(f"{case.get('id')}: PASS requires completed status")
    findings = findings_doc.get("findings", [])
    for finding in findings:
        owner = finding.get("owner")
        if owner not in FINDING_OWNERS and not (isinstance(owner, str) and owner.startswith("agent-")):
            failures.append(f"{finding.get('id')}: invalid finding owner")
        for key in ("id", "kind", "severity", "evidence", "proposed_change"):
            if not finding.get(key):
                failures.append(f"finding missing {key}")
    if state.get("verdict") == "PASS":
        if any(item.get("verdict") != "PASS" for item in states):
            failures.append("root PASS requires every case to PASS")
        if any(item.get("severity") in {"BLOCK", "HIGH"} for item in findings):
            failures.append("root PASS cannot contain blocking findings")
    if state.get("real_workflow_observation") is True:
        if state.get("execution_kind") != "semantic-donor-run":
            failures.append("real workflow requires semantic-donor-run execution")
        observation_path = run / "workflow-observation.json"
        if not observation_path.is_file():
            failures.append("real workflow requires workflow-observation.json")
        else:
            try:
                observation = load(observation_path)
                if observation.get("workflow_id") != state.get("workflow_id"):
                    failures.append("workflow observation identity differs from run-state")
                if observation.get("outcome", {}).get("verdict") != "PASS":
                    failures.append("real workflow observation requires a PASS outcome")
                if len(observation.get("evidence", [])) != len(cases):
                    failures.append("real workflow observation evidence must cover every case")
            except (OSError, json.JSONDecodeError) as exc:
                failures.append(str(exc))
    return failures


def main() -> int:
    run = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    failures = validate(run)
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    print(f"PASS agentkit E2E run contract: {run.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
