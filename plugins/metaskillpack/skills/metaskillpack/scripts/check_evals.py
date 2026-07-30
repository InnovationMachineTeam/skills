#!/usr/bin/env python3
"""Validate metaskillpack routing and behavior fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("cases"), list):
        raise ValueError(f"cases[] required: {path}")
    return value


def main() -> int:
    eval_root = Path(sys.argv[1] if len(sys.argv) > 1 else "evals").resolve()
    skill_root = Path(__file__).resolve().parents[1]
    failures = []
    try:
        routing = load(eval_root / "routing.json")
        behavior = load(eval_root / "behavior.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL {exc}")
        return 1

    ids = []
    covered_modes = set()
    for case in routing["cases"]:
        ids.append(case.get("id"))
        command = case.get("command")
        if not isinstance(command, list) or not all(isinstance(item, str) for item in command):
            failures.append(f"{case.get('id')}: command must be a string array")
            continue
        result = subprocess.run(
            [sys.executable, str(skill_root / "scripts" / "route_command.py"), *command],
            text=True,
            capture_output=True,
            check=False,
        )
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError:
            failures.append(f"{case.get('id')}: route output is not JSON")
            continue
        for field in ("status", "canonical_mode", "donor", "donor_route"):
            expected_key = f"expected_{field}"
            if expected_key in case and payload.get(field) != case[expected_key]:
                failures.append(f"{case.get('id')}: {field}={payload.get(field)!r}, expected {case[expected_key]!r}")
        if result.returncode != case.get("expected_exit", 0):
            failures.append(f"{case.get('id')}: exit={result.returncode}, expected {case.get('expected_exit', 0)}")
        if payload.get("status") == "ready":
            covered_modes.add(payload.get("canonical_mode"))

    for case in behavior["cases"]:
        ids.append(case.get("id"))
        if not isinstance(case.get("expected_properties"), list) or not case["expected_properties"]:
            failures.append(f"{case.get('id')}: expected_properties required")
        if not isinstance(case.get("forbidden_properties"), list) or not case["forbidden_properties"]:
            failures.append(f"{case.get('id')}: forbidden_properties required")

    if any(not isinstance(value, str) or not value for value in ids) or len(ids) != len(set(ids)):
        failures.append("case ids must be unique non-empty strings")
    required_modes = {"create", "scout", "research", "optimize", "doctor", "manage", "harvest", "refactor", "evaluate", "run", "compare", "intake", "prompt", "practices", "marketplace", "status", "route", "upgrade", "help"}
    missing = sorted(required_modes - covered_modes)
    if missing:
        failures.append(f"routing coverage missing modes: {missing}")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print(f"PASS {len(routing['cases'])} routing cases and {len(behavior['cases'])} behavior cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
