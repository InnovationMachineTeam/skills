#!/usr/bin/env python3
"""Validate durable agent-team lifecycle run state."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

PHASES = {"assess", "design", "build", "map", "approve", "operate", "verify", "close", "change", "recover", "retire"}
STATUSES = {"PENDING", "RUNNING", "WAITING_APPROVAL", "BLOCKED", "COMPLETED", "PARTIAL", "FAILED", "ROLLED_BACK", "RETIRED"}
TERMINAL = {"COMPLETED", "FAILED", "ROLLED_BACK", "RETIRED"}


def text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_timestamp(value: object) -> bool:
    if not text(value):
        return False
    try:
        datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def validate(data: object) -> list[str]:
    failures: list[str] = []
    if not isinstance(data, dict):
        return ["root must be an object"]
    if data.get("schema_version") != 1 or not text(data.get("run_id")):
        failures.append("schema_version 1 and run_id are required")
    for key in ("team_ref", "spec_ref", "accountable_owner", "workflow", "authority_scope", "next_action"):
        if not text(data.get(key)):
            failures.append(f"{key} is required")
    if data.get("phase") not in PHASES or data.get("status") not in STATUSES:
        failures.append("phase or status is invalid")
    for key in ("handoffs", "checkpoints", "artifacts", "risks"):
        if not isinstance(data.get(key), list):
            failures.append(f"{key} must be an array")
    revisions = data.get("expected_revisions")
    if not isinstance(revisions, dict) or not all(text(revisions.get(k)) for k in ("registry", "map")):
        failures.append("expected registry/map revisions are required")
    budgets = data.get("budgets")
    if not isinstance(budgets, dict) or not all(isinstance(budgets.get(k), int) and budgets[k] >= 0 for k in ("max_steps", "max_retries")):
        failures.append("non-negative max_steps and max_retries are required")
    for key in ("created_at", "updated_at"):
        if not validate_timestamp(data.get(key)):
            failures.append(f"{key} must be ISO-8601")
    if not isinstance(data.get("rollback"), dict) or not text(data["rollback"].get("procedure")):
        failures.append("rollback.procedure is required")
    if data.get("status") not in TERMINAL and not data.get("checkpoints"):
        failures.append("non-terminal state requires a checkpoint")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.state.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    failures = validate(data)
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        return 1
    print("PASS agent-team run state is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
