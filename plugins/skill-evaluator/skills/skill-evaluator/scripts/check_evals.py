#!/usr/bin/env python3
"""Validate skill-evaluator routing and behavioral self-evals."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROUTES = {"evaluation-plan", "routing-and-triggers", "behavior-and-quality", "script-and-tooling", "security-and-authority", "catalog-and-coexistence", "agent-assets-and-access", "run-evaluation", "audit-evaluation", "compare-evaluations"}


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
    if not isinstance(value, dict) or value.get("skill") != "skill-evaluator" or not isinstance(value.get("cases"), list):
        findings.append(Finding("root", "eval root must identify skill-evaluator and contain cases", str(path)))
        return None
    return value


def validate(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    routing_path = root / "routing.json"
    routing = load(routing_path, findings)
    if routing:
        ids: set[str] = set()
        covered: set[str] = set()
        triggers: set[bool] = set()
        splits: set[str] = set()
        for index, case in enumerate(routing["cases"]):
            if not isinstance(case, dict) or not isinstance(case.get("id"), str) or case["id"] in ids:
                findings.append(Finding("case-id", f"routing case {index} needs unique id", str(routing_path)))
                continue
            ids.add(case["id"])
            if isinstance(case.get("expected_route"), str):
                covered.add(case["expected_route"])
            if isinstance(case.get("expected_trigger"), bool):
                triggers.add(case["expected_trigger"])
            if case.get("split") not in {"train", "validation", "regression"}:
                findings.append(Finding("split", f"routing case {case['id']} needs split", str(routing_path)))
            else:
                splits.add(case["split"])
        if ROUTES - covered:
            findings.append(Finding("route-coverage", "missing routes: " + ", ".join(sorted(ROUTES - covered)), str(routing_path)))
        if triggers != {True, False}:
            findings.append(Finding("trigger-coverage", "include positive and negative triggers", str(routing_path)))
        if "regression" not in splits:
            findings.append(Finding("regression", "routing self-evals need public regression coverage", str(routing_path)))
        policy = routing.get("holdout_policy")
        if not isinstance(policy, dict) or policy.get("mode") != "external-protected":
            findings.append(Finding("holdout", "routing self-evals must declare an external-protected holdout", str(routing_path)))
    behavior_path = root / "behavior.json"
    behavior = load(behavior_path, findings)
    if behavior:
        ids: set[str] = set()
        splits: set[str] = set()
        for index, case in enumerate(behavior["cases"]):
            if not isinstance(case, dict) or not isinstance(case.get("id"), str) or case["id"] in ids:
                findings.append(Finding("case-id", f"behavior case {index} needs unique id", str(behavior_path)))
                continue
            ids.add(case["id"])
            for key in ("expected_properties", "forbidden_properties"):
                if not isinstance(case.get(key), list) or not case[key]:
                    findings.append(Finding("behavior", f"case {case['id']} needs {key}", str(behavior_path)))
            if case.get("split") not in {"train", "validation", "regression"}:
                findings.append(Finding("split", f"behavior case {case['id']} needs split", str(behavior_path)))
            else:
                splits.add(case["split"])
        if "regression" not in splits:
            findings.append(Finding("regression", "behavior self-evals need public regression coverage", str(behavior_path)))
        policy = behavior.get("holdout_policy")
        if not isinstance(policy, dict) or policy.get("mode") != "external-protected":
            findings.append(Finding("holdout", "behavior self-evals must declare an external-protected holdout", str(behavior_path)))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("eval_dir", type=Path, nargs="?", default=Path("evals"))
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    findings = validate(args.eval_dir.expanduser().resolve())
    payload = {"valid": not findings, "count": len(findings), "findings": [asdict(item) for item in findings]}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Findings: {len(findings)}")
        for item in findings:
            print(f"[ERROR] {item.code}: {item.message} ({item.path})")
        if not findings:
            print("Routing and behavior eval datasets are structurally complete.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
