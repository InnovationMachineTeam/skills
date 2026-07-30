#!/usr/bin/env python3
"""Run allowlisted fixture-only self-evals for bundled evaluator utilities."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ALLOWED = {
    "scripts/validate_eval_plan.py",
    "scripts/validate_eval_suite.py",
    "scripts/score_routing.py",
    "scripts/compare_eval_runs.py",
}
SAFE_POLICIES = {"read-only", "stderr-only", "stdout-only unless explicit output"}


def contained(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def json_contains(actual: Any, expected: Any) -> bool:
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(key in actual and json_contains(actual[key], value) for key, value in expected.items())
    if isinstance(expected, list):
        return actual == expected
    return actual == expected


def run(suite_path: Path) -> tuple[list[dict[str, Any]], int]:
    package = Path(__file__).resolve().parent.parent
    fixture_root = (package / "evals" / "fixtures").resolve()
    suite = json.loads(suite_path.read_text(encoding="utf-8"))
    cases = suite.get("cases") if isinstance(suite, dict) else None
    if not isinstance(cases, list) or not cases:
        raise ValueError("suite must contain a non-empty cases array")
    results: list[dict[str, Any]] = []
    failures = 0
    seen: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise ValueError(f"case {index} must be an object")
        case_id = case.get("id")
        script = case.get("script")
        args = case.get("args")
        expected_exit = case.get("expected_exit")
        side_effect_policy = case.get("side_effect_policy")
        if not isinstance(case_id, str) or not case_id or case_id in seen:
            raise ValueError(f"case {index} needs a unique id")
        seen.add(case_id)
        if script not in ALLOWED:
            raise ValueError(f"case {case_id} references non-allowlisted script")
        script_path = (package / script).resolve()
        if not contained(script_path, (package / "scripts").resolve()) or not script_path.is_file():
            raise ValueError(f"case {case_id} script escapes the bundled scripts directory")
        if not isinstance(args, list) or not args or any(not isinstance(item, str) or item.startswith("-") for item in args):
            raise ValueError(f"case {case_id} args must be non-option fixture paths")
        resolved_args: list[str] = []
        for item in args:
            resolved = (package / item).resolve()
            if not contained(resolved, fixture_root):
                raise ValueError(f"case {case_id} argument escapes evals/fixtures")
            resolved_args.append(str(resolved))
        if not isinstance(expected_exit, int) or isinstance(expected_exit, bool):
            raise ValueError(f"case {case_id} needs integer expected_exit")
        if side_effect_policy not in SAFE_POLICIES:
            raise ValueError(f"case {case_id} has a non-allowlisted side_effect_policy")
        completed = subprocess.run(
            [sys.executable, str(script_path), *resolved_args],
            cwd=package,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        passed = completed.returncode == expected_exit
        expected_json = case.get("expected_json")
        if expected_json is not None:
            try:
                observed_json = json.loads(completed.stdout)
            except json.JSONDecodeError:
                passed = False
            else:
                passed = passed and json_contains(observed_json, expected_json)
        if not passed:
            failures += 1
        results.append({
            "id": case_id,
            "passed": passed,
            "expected_exit": expected_exit,
            "observed_exit": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        })
    return results, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("suite", type=Path, nargs="?", default=Path(__file__).resolve().parent.parent / "evals" / "scripts.json")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    try:
        results, failures = run(args.suite.expanduser().resolve())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"Fixture eval run failed: {exc}", file=sys.stderr)
        return 1
    if args.format == "json":
        print(json.dumps({"passed": not failures, "failures": failures, "cases": results}, ensure_ascii=False, indent=2))
    else:
        print(f"Cases: {len(results)}; failures: {failures}")
        for item in results:
            print(f"[{'PASS' if item['passed'] else 'FAIL'}] {item['id']}: exit {item['observed_exit']} (expected {item['expected_exit']})")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
