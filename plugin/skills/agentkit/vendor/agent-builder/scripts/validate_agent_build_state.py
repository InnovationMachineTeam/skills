#!/usr/bin/env python3
"""Validate a resumable individual-agent build state."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PHASE = {"pending", "in_progress", "completed", "rejected", "inconclusive", "waiting_approval", "blocked", "skipped"}
ROOT_STATUS = {"planned", "in_progress", "waiting_approval", "blocked", "completed", "aborted"}


def main() -> int:
    if len(sys.argv) != 2:
        print("FAIL usage: validate_agent_build_state.py STATE.json", file=sys.stderr)
        return 2
    try:
        value = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    required = {"schema_version", "builder", "build_id", "scenario", "goal", "status", "scope", "acceptance_criteria", "authority", "phases", "artifacts", "approvals", "risks", "updated_at"}
    errors = [f"missing {key}" for key in sorted(required - value.keys())]
    if value.get("builder") != "agent-builder":
        errors.append("builder must be agent-builder")
    if value.get("status") not in ROOT_STATUS:
        errors.append(f"invalid root status {value.get('status')}")
    ids: set[str] = set()
    for phase in value.get("phases", []):
        if phase.get("id") in ids:
            errors.append(f"duplicate phase {phase.get('id')}")
        ids.add(phase.get("id"))
        if phase.get("status") not in PHASE:
            errors.append(f"invalid phase status {phase.get('status')}")
        for key in ("specialist", "objective", "dependencies", "entry_conditions", "required_outputs", "exit_checks", "authority", "evidence"):
            if key not in phase:
                errors.append(f"phase {phase.get('id')} missing {key}")
        if not phase.get("required_outputs"):
            errors.append(f"phase {phase.get('id')} requires at least one output")
        if not phase.get("exit_checks"):
            errors.append(f"phase {phase.get('id')} requires at least one exit check")
        if phase.get("status") == "completed" and not phase.get("evidence"):
            errors.append(f"completed phase {phase.get('id')} requires evidence")
    for phase in value.get("phases", []):
        for dependency in phase.get("dependencies", []):
            if dependency not in ids:
                errors.append(f"phase {phase.get('id')} has unknown dependency {dependency}")
    if value.get("status") == "completed":
        unfinished = [phase.get("id") for phase in value.get("phases", []) if phase.get("status") not in {"completed", "skipped"}]
        if unfinished:
            errors.append("completed root has unfinished phases: " + ", ".join(unfinished))
    if errors:
        for error in errors:
            print(f"FAIL {error}", file=sys.stderr)
        return 1
    print(f"PASS agent build state: {value['build_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
