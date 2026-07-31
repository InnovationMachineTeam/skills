#!/usr/bin/env python3
"""Validate executable contracts for the individual-agent portfolio eval fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path


SKILLS = (
    "agent-architect", "agent-best-practices", "agent-builder", "agent-context",
    "agent-doctor", "agent-evaluator", "agent-manager", "agent-optimizer",
    "agent-refactor", "agent-scout",
)
SPLITS = {"train", "validation", "regression"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(root: Path) -> list[str]:
    failures: list[str] = []
    inputs: set[str] = set()
    for skill in SKILLS:
        evals = root / "skills" / "agent-skills" / skill / "evals"
        for kind in ("routing", "behavior"):
            path = evals / f"{kind}.json"
            try:
                document = load(path)
            except (OSError, json.JSONDecodeError) as exc:
                failures.append(f"{path}: {exc}")
                continue
            if document.get("skill") != skill:
                failures.append(f"{path}: wrong skill identity")
            cases = document.get("cases")
            if not isinstance(cases, list) or not cases:
                failures.append(f"{path}: cases must be non-empty")
                continue
            ids: set[str] = set()
            for case in cases:
                case_id = case.get("id")
                if not case_id or case_id in ids:
                    failures.append(f"{path}: missing/duplicate case id {case_id}")
                ids.add(case_id)
                text = case.get("input")
                if not isinstance(text, str) or not text.strip():
                    failures.append(f"{path}:{case_id}: input is required")
                elif text.casefold() in inputs:
                    failures.append(f"{path}:{case_id}: duplicate portfolio input")
                else:
                    inputs.add(text.casefold())
                if case.get("split") not in SPLITS:
                    failures.append(f"{path}:{case_id}: bundled split must be train/validation/regression")
                if not case.get("grader"):
                    failures.append(f"{path}:{case_id}: grader is required")
                if kind == "routing":
                    if not isinstance(case.get("expected_trigger"), bool):
                        failures.append(f"{path}:{case_id}: expected_trigger must be boolean")
                    if case.get("expected_trigger") is False and not case.get("expected_route"):
                        failures.append(f"{path}:{case_id}: negative case must name neighboring route")
                else:
                    if not case.get("expected_properties") or not case.get("forbidden_properties"):
                        failures.append(f"{path}:{case_id}: behavior properties are required")
    return failures


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    failures = validate(root)
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    print(f"PASS individual-agent eval fixtures: {len(SKILLS)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
