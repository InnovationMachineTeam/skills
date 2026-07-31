#!/usr/bin/env python3
"""Validate a reviewable agent-team specification."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
RISKS = {"R0", "R1", "R2", "R3"}
ROLE_KINDS = {"orchestrator", "specialist", "integrator", "verifier", "curator", "operator"}
PATTERNS = {"sequential", "pipeline", "fork-join", "dag", "manager", "handoff", "blackboard", "competing-hypotheses"}
PLACEMENTS = {"INLINE", "PRIVATE_COMMAND", "PRIVATE_SKILL", "PUBLIC_SKILL", "TOOL_SCRIPT", "WORKFLOW", "USE_EXISTING", "REJECT"}


def text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(data: object) -> list[str]:
    failures: list[str] = []
    if not isinstance(data, dict):
        return ["root must be an object"]
    if data.get("schema_version") != 1:
        failures.append("schema_version must be 1")
    if not text(data.get("id")) or not str(data.get("id", "")).startswith("asset://"):
        failures.append("id must be an asset:// reference")
    if not text(data.get("name")) or not isinstance(data.get("version"), str) or not SEMVER.fullmatch(data["version"]):
        failures.append("name and SemVer version are required")
    if data.get("status") not in {"draft", "candidate", "verified", "approved"}:
        failures.append("design status must be draft, candidate, verified or approved")
    if not text(data.get("accountable_owner")) or not text(data.get("goal")):
        failures.append("accountable_owner and goal are required")
    if data.get("risk_tier") not in RISKS:
        failures.append("risk_tier is invalid")
    for key in ("non_goals", "capability_placement", "model_policy_refs", "human_checkpoints", "evaluation", "rollback", "retirement"):
        if not isinstance(data.get(key), list):
            failures.append(f"{key} must be an array")
    roles = data.get("roles")
    role_ids: set[str] = set()
    if not isinstance(roles, list) or len(roles) < 2:
        failures.append("a team spec requires at least two roles")
        roles = []
    for index, role in enumerate(roles):
        if not isinstance(role, dict):
            failures.append(f"roles[{index}] must be an object")
            continue
        role_id = role.get("id")
        if not text(role_id) or role_id in role_ids:
            failures.append(f"roles[{index}].id must be non-empty and unique")
        else:
            role_ids.add(str(role_id))
        if role.get("kind") not in ROLE_KINDS:
            failures.append(f"roles[{index}].kind is invalid")
        for key in ("mission", "accountable_owner"):
            if not text(role.get(key)):
                failures.append(f"roles[{index}].{key} is required")
        for key in ("non_goals", "boundary_evidence", "inputs", "outputs", "tools", "permissions", "data_classes", "write_set", "stop_conditions", "escalation"):
            if not isinstance(role.get(key), list):
                failures.append(f"roles[{index}].{key} must be an array")
        if not role.get("boundary_evidence"):
            failures.append(f"roles[{index}] needs boundary evidence")
        if not text(role.get("model_policy_ref")):
            failures.append(f"roles[{index}].model_policy_ref is required")
        if not isinstance(role.get("budgets"), dict) or not isinstance(role["budgets"].get("max_capabilities"), int):
            failures.append(f"roles[{index}].budgets.max_capabilities is required")
    workflow = data.get("workflow")
    if not isinstance(workflow, dict):
        failures.append("workflow must be an object")
    else:
        if workflow.get("pattern") not in PATTERNS:
            failures.append("workflow.pattern is invalid")
        for key in ("integration_owner_ref", "conflict_policy", "cancellation", "partial_failure"):
            if not text(workflow.get(key)):
                failures.append(f"workflow.{key} is required")
        if workflow.get("integration_owner_ref") not in role_ids:
            failures.append("workflow integration owner must resolve to a role")
        stages = workflow.get("stages")
        stage_ids: set[str] = set()
        if not isinstance(stages, list) or not stages:
            failures.append("workflow.stages must be non-empty")
        else:
            for index, stage in enumerate(stages):
                if not isinstance(stage, dict) or not text(stage.get("id")):
                    failures.append(f"workflow.stages[{index}] requires id")
                    continue
                if stage["id"] in stage_ids:
                    failures.append(f"duplicate stage id: {stage['id']}")
                stage_ids.add(stage["id"])
                if stage.get("role_ref") not in role_ids:
                    failures.append(f"stage {stage['id']} has unknown role_ref")
                for key in ("depends_on", "artifact_outputs"):
                    if not isinstance(stage.get(key), list):
                        failures.append(f"stage {stage['id']}.{key} must be an array")
            for stage in stages:
                if isinstance(stage, dict):
                    unknown = set(stage.get("depends_on", [])) - stage_ids
                    if unknown:
                        failures.append(f"stage {stage.get('id')} has unknown dependencies {sorted(unknown)}")
    for index, placement in enumerate(data.get("capability_placement", [])):
        if not isinstance(placement, dict) or placement.get("decision") not in PLACEMENTS:
            failures.append(f"capability_placement[{index}] has invalid decision")
            continue
        if placement.get("decision") in {"PRIVATE_COMMAND", "PRIVATE_SKILL"}:
            owner = placement.get("owner_agent_ref")
            consumers = placement.get("allowed_consumers")
            if not text(owner) or consumers != [owner]:
                failures.append(f"capability_placement[{index}] private owner/consumer mismatch")
    if data.get("worktree_policy") not in {"none", "single", "per-worker", "dynamic"}:
        failures.append("worktree_policy is invalid")
    if not data.get("evaluation") or not data.get("rollback") or not data.get("retirement"):
        failures.append("evaluation, rollback and retirement must be non-empty")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.spec.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    failures = validate(data)
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        return 1
    print("PASS agent team specification is structurally valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
