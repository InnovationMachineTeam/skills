#!/usr/bin/env python3
"""Validate an agent workspace/worktree ledger and isolation boundaries."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath

POLICIES = {"SHARED_READ_ONLY", "SEQUENTIAL_SHARED", "WORKTREE_PER_TASK", "REJECT_PARALLELISM"}
STATUSES = {"PLANNED", "ALLOCATED", "ACTIVE", "READY", "INTEGRATED", "FAILED", "CANCELLED", "ABANDONED", "ARCHIVED", "RELEASED"}
ACTIVE = {"ALLOCATED", "ACTIVE", "READY"}
SHA = re.compile(r"^[0-9a-f]{7,64}$")


def text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def safe_path(value: object) -> bool:
    if not text(value):
        return False
    path = PurePosixPath(str(value))
    return not path.is_absolute() and ".." not in path.parts and len(path.parts) >= 2


def validate(data: object) -> list[str]:
    failures: list[str] = []
    if not isinstance(data, dict):
        return ["root must be an object"]
    if data.get("schema_version") != 1 or not isinstance(data.get("revision"), int):
        failures.append("schema_version 1 and integer revision are required")
    if data.get("policy") not in POLICIES:
        failures.append("policy is invalid")
    for key in ("repository", "integration_owner_ref", "collision_policy"):
        if not text(data.get(key)):
            failures.append(f"{key} is required")
    baseline = data.get("baseline")
    if not isinstance(baseline, dict) or not SHA.fullmatch(str(baseline.get("revision", ""))) or baseline.get("user_changes_preserved") is not True:
        failures.append("baseline requires revision and preserved user changes")
    workspaces = data.get("workspaces")
    if not isinstance(workspaces, list):
        failures.append("workspaces must be an array")
        workspaces = []
    ids: set[str] = set()
    paths: set[str] = set()
    branches: set[str] = set()
    active_write_sets: list[tuple[str, set[str]]] = []
    for index, workspace in enumerate(workspaces):
        label = f"workspaces[{index}]"
        if not isinstance(workspace, dict):
            failures.append(f"{label} must be an object")
            continue
        workspace_id = workspace.get("workspace_id")
        if not text(workspace_id) or workspace_id in ids:
            failures.append(f"{label}.workspace_id must be unique")
        else:
            ids.add(str(workspace_id))
        for key in ("task_id", "owner_agent_ref", "branch"):
            if not text(workspace.get(key)):
                failures.append(f"{label}.{key} is required")
        path = workspace.get("path")
        if not safe_path(path) or path in paths:
            failures.append(f"{label}.path must be safe and unique")
        else:
            paths.add(str(path))
        branch = workspace.get("branch")
        if text(branch) and branch in branches:
            failures.append(f"{label}.branch must be unique")
        elif text(branch):
            branches.add(str(branch))
        if not SHA.fullmatch(str(workspace.get("base_revision", ""))):
            failures.append(f"{label}.base_revision is invalid")
        write_set = workspace.get("write_set")
        if not isinstance(write_set, list) or not all(safe_path(item) for item in write_set):
            failures.append(f"{label}.write_set must contain safe relative paths")
            write_set = []
        if workspace.get("status") not in STATUSES:
            failures.append(f"{label}.status is invalid")
        lease = workspace.get("lease")
        if not isinstance(lease, dict) or not all(text(lease.get(k)) for k in ("owner", "expires_at", "token")):
            failures.append(f"{label}.lease is incomplete")
        quota = workspace.get("quota")
        if not isinstance(quota, dict) or not isinstance(quota.get("max_bytes"), int) or quota["max_bytes"] < 0:
            failures.append(f"{label}.quota.max_bytes is invalid")
        for key in ("tests", "artifacts"):
            if not isinstance(workspace.get(key), list):
                failures.append(f"{label}.{key} must be an array")
        if workspace.get("status") in ACTIVE:
            active_write_sets.append((str(workspace_id), set(write_set)))
        cleanup = workspace.get("cleanup")
        if not isinstance(cleanup, dict) or cleanup.get("authorized") not in {True, False} or not text(cleanup.get("retention")):
            failures.append(f"{label}.cleanup authorization and retention are required")
        elif cleanup["authorized"] and workspace.get("status") not in {"INTEGRATED", "CANCELLED", "ABANDONED", "ARCHIVED", "RELEASED"}:
            failures.append(f"{label} cleanup authorized for non-terminal workspace")
    for left_index, (left_id, left) in enumerate(active_write_sets):
        for right_id, right in active_write_sets[left_index + 1:]:
            overlap = left & right
            if overlap:
                failures.append(f"active workspaces {left_id} and {right_id} overlap: {sorted(overlap)}")
    if data.get("policy") == "WORKTREE_PER_TASK" and len(workspaces) < 2:
        failures.append("WORKTREE_PER_TASK requires at least two workspaces")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.ledger.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    failures = validate(data)
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        return 1
    print("PASS agent workspace ledger is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
