#!/usr/bin/env python3
"""Validate an approved agent-team runtime plan."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PATTERNS = {"sequential", "pipeline", "fork-join", "dag", "dynamic"}


def text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(data: object) -> list[str]:
    failures: list[str] = []
    if not isinstance(data, dict):
        return ["root must be an object"]
    if data.get("schema_version") != 1 or not text(data.get("run_id")):
        failures.append("schema_version 1 and run_id are required")
    if data.get("team_status") != "active":
        failures.append("team_status must be active")
    for key in ("team_ref", "registry_revision", "map_revision", "integration_owner_ref", "state_locator"):
        if not text(data.get(key)):
            failures.append(f"{key} is required")
    task = data.get("task")
    if not isinstance(task, dict):
        failures.append("task must be an object")
    else:
        for key in ("objective", "authority_scope", "data_class", "idempotency_key", "deadline"):
            if not text(task.get(key)):
                failures.append(f"task.{key} is required")
        for key in ("input_refs", "acceptance_checks"):
            if not isinstance(task.get(key), list) or not task[key]:
                failures.append(f"task.{key} must be non-empty")
    budgets = data.get("budgets")
    if not isinstance(budgets, dict) or not all(isinstance(budgets.get(k), int) and budgets[k] >= 0 for k in ("max_steps", "max_retries", "max_parallel")):
        failures.append("budgets require non-negative max_steps, max_retries and max_parallel")
    workflow = data.get("workflow")
    nodes = []
    if not isinstance(workflow, dict) or workflow.get("pattern") not in PATTERNS:
        failures.append("workflow.pattern is invalid")
    else:
        nodes = workflow.get("nodes")
        if not isinstance(nodes, list) or not nodes:
            failures.append("workflow.nodes must be non-empty")
            nodes = []
    node_ids: set[str] = set()
    by_id: dict[str, dict] = {}
    for index, node in enumerate(nodes):
        label = f"workflow.nodes[{index}]"
        if not isinstance(node, dict) or not text(node.get("id")) or node.get("id") in node_ids:
            failures.append(f"{label}.id must be non-empty and unique")
            continue
        node_id = str(node["id"])
        node_ids.add(node_id)
        by_id[node_id] = node
        for key in ("owner_ref", "exit_gate", "checkpoint_policy"):
            if not text(node.get(key)):
                failures.append(f"{label}.{key} is required")
        for key in ("depends_on", "input_refs", "output_refs", "write_set", "allowed_capabilities"):
            if not isinstance(node.get(key), list):
                failures.append(f"{label}.{key} must be an array")
        if not isinstance(node.get("max_attempts"), int) or node["max_attempts"] < 1:
            failures.append(f"{label}.max_attempts must be positive")
    for node_id, node in by_id.items():
        unknown = set(node.get("depends_on", [])) - node_ids
        if unknown:
            failures.append(f"node {node_id} has unknown dependencies {sorted(unknown)}")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visiting:
            failures.append(f"workflow contains a cycle at {node_id}")
            return
        if node_id in visited:
            return
        visiting.add(node_id)
        for dep in by_id.get(node_id, {}).get("depends_on", []):
            if dep in by_id:
                visit(dep)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in node_ids:
        visit(node_id)
    if isinstance(workflow, dict) and workflow.get("pattern") in {"fork-join", "dag", "dynamic"}:
        if not text(workflow.get("merge_protocol")):
            failures.append("parallel-capable workflow requires merge_protocol")
    verification = data.get("verification")
    if not isinstance(verification, dict) or not text(verification.get("verifier_ref")) or not isinstance(verification.get("checks"), list) or not verification["checks"]:
        failures.append("independent verification and checks are required")
    if not isinstance(data.get("cancellation"), dict) or not text(data["cancellation"].get("procedure")):
        failures.append("cancellation.procedure is required")
    if not isinstance(data.get("recovery"), dict) or not text(data["recovery"].get("procedure")):
        failures.append("recovery.procedure is required")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.plan.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    failures = validate(data)
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        return 1
    print("PASS agent-team runtime plan is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
