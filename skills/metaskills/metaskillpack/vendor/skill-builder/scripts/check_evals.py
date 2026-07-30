#!/usr/bin/env python3
"""Validate skill-builder routing and behavior eval datasets."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


SCENARIOS = {
    "full-lifecycle",
    "create-from-spec",
    "discover-opportunities",
    "research-to-skill",
    "external-skill-adoption",
    "evaluate-skill",
    "repair-and-improve",
    "optimize-existing",
    "compare-and-refactor",
    "split-and-migrate",
    "portfolio-governance",
    "master-prompt-development",
    "agent-system-capability",
    "specialist-dispatch",
    "resume-build",
}


@dataclass
class Finding:
    code: str
    message: str
    path: str


def load(path: Path, findings: list[Finding]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        findings.append(Finding("json", f"cannot read valid JSON: {exc}", str(path)))
        return None
    if not isinstance(value, dict) or value.get("skill") != "skill-builder":
        findings.append(Finding("shape", "eval root must identify skill-builder", str(path)))
        return None
    return value


def get_cases(value: dict[str, Any], path: Path, findings: list[Finding]) -> list[dict[str, Any]]:
    raw = value.get("cases")
    if not isinstance(raw, list) or not raw:
        findings.append(Finding("cases", "cases must be a non-empty array", str(path)))
        return []
    result: list[dict[str, Any]] = []
    ids: set[str] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            findings.append(Finding("case", f"case {index} must be an object", str(path)))
            continue
        case_id = item.get("id")
        if not isinstance(case_id, str) or not case_id or case_id in ids:
            findings.append(Finding("case-id", f"case {index} needs a unique id", str(path)))
        else:
            ids.add(case_id)
        result.append(item)
    return result


def validate(eval_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    routing_path = eval_dir / "routing.json"
    routing = load(routing_path, findings)
    if routing is not None:
        cases = get_cases(routing, routing_path, findings)
        covered = {item.get("expected_scenario") for item in cases if item.get("expected_scenario")}
        missing = SCENARIOS - covered
        if missing:
            findings.append(Finding("scenario-coverage", "missing scenarios: " + ", ".join(sorted(missing)), str(routing_path)))
        actions = {item.get("expected_action") for item in cases}
        for required in ("route", "clarify", "do-not-trigger"):
            if required not in actions:
                findings.append(Finding("action-coverage", f"missing action: {required}", str(routing_path)))
        triggers = {item.get("expected_trigger") for item in cases}
        if not {True, False}.issubset(triggers):
            findings.append(Finding("trigger-coverage", "include positive and negative trigger cases", str(routing_path)))
        if not any(item.get("explicit_scenario") for item in cases):
            findings.append(Finding("explicit-coverage", "include explicit scenario invocation", str(routing_path)))
        if not any(item.get("expected_action") == "route" and not item.get("explicit_scenario") for item in cases):
            findings.append(Finding("implicit-coverage", "include context-inferred routing", str(routing_path)))

    behavior_path = eval_dir / "behavior.json"
    behavior = load(behavior_path, findings)
    if behavior is not None:
        for item in get_cases(behavior, behavior_path, findings):
            for key in ("expected_properties", "forbidden_properties"):
                if not isinstance(item.get(key), list) or not item[key]:
                    findings.append(Finding("behavior", f"case {item.get('id', '?')} requires {key}", str(behavior_path)))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("eval_dir", type=Path, nargs="?", default=Path("evals"))
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    findings = validate(args.eval_dir.expanduser().resolve())
    if args.format == "json":
        print(json.dumps({"count": len(findings), "findings": [asdict(item) for item in findings]}, ensure_ascii=False, indent=2))
    else:
        print(f"Findings: {len(findings)}")
        for item in findings:
            print(f"[ERROR] {item.code}: {item.message} ({item.path})")
        if not findings:
            print("Routing and behavior eval datasets are structurally complete.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
