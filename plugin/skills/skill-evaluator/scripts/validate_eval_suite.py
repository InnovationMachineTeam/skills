#!/usr/bin/env python3
"""Validate routing, behavior, and optional script evaluation datasets."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


SPLITS = {"train", "validation", "regression", "holdout"}


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
    if not isinstance(value, dict) or value.get("schema_version") not in {1, "1.0"} or not isinstance(value.get("cases"), list):
        findings.append(Finding("root", "dataset requires schema_version and cases array", str(path)))
        return None
    return value


def common_cases(value: dict[str, Any], path: Path, findings: list[Finding]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    ids: set[str] = set()
    for index, case in enumerate(value["cases"]):
        if not isinstance(case, dict):
            findings.append(Finding("case", f"case {index} must be an object", str(path)))
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id or case_id in ids:
            findings.append(Finding("case-id", f"case {index} needs a unique id", str(path)))
        else:
            ids.add(case_id)
        if case.get("split") not in SPLITS:
            findings.append(Finding("split", f"case {case_id or index} needs train, validation, regression, or holdout split", str(path)))
        result.append(case)
    if not result:
        findings.append(Finding("cases", "dataset must contain at least one case", str(path)))
    return result


def validate_holdout_policy(value: dict[str, Any], items: list[dict[str, Any]], path: Path, findings: list[Finding]) -> None:
    policy = value.get("holdout_policy")
    external = isinstance(policy, dict) and policy.get("mode") == "external-protected" and isinstance(policy.get("exposure_rule"), str) and bool(policy["exposure_rule"].strip())
    local_holdout = any(case.get("split") == "holdout" for case in items)
    if not external and not local_holdout:
        findings.append(Finding("holdout", "declare external-protected holdout policy or include holdout cases", str(path)))
    if external and local_holdout:
        findings.append(Finding("holdout", "external-protected datasets must not bundle answer-bearing holdout cases", str(path)))


def validate(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    routing_path = root / "routing.json"
    routing = load(routing_path, findings)
    if routing:
        items = common_cases(routing, routing_path, findings)
        for case in items:
            if not isinstance(case.get("input"), str) or not case["input"].strip() or not isinstance(case.get("expected_trigger"), bool):
                findings.append(Finding("routing", f"case {case.get('id', '?')} needs input and boolean expected_trigger", str(routing_path)))
            if not isinstance(case.get("expected_action"), str) or not case["expected_action"]:
                findings.append(Finding("routing", f"case {case.get('id', '?')} needs expected_action", str(routing_path)))
        observed = {case.get("expected_trigger") for case in items}
        if not {True, False}.issubset(observed):
            findings.append(Finding("routing-coverage", "routing dataset needs positive and negative cases", str(routing_path)))
        validate_holdout_policy(routing, items, routing_path, findings)
    behavior_path = root / "behavior.json"
    behavior = load(behavior_path, findings)
    if behavior:
        items = common_cases(behavior, behavior_path, findings)
        for case in items:
            request = case.get("request", case.get("input"))
            if not isinstance(request, str) or not request.strip():
                findings.append(Finding("behavior", f"case {case.get('id', '?')} needs request or input", str(behavior_path)))
            for key in ("expected_properties", "forbidden_properties"):
                if not isinstance(case.get(key), list) or not case[key] or any(not isinstance(item, str) or not item for item in case[key]):
                    findings.append(Finding("behavior", f"case {case.get('id', '?')} needs non-empty {key}", str(behavior_path)))
        validate_holdout_policy(behavior, items, behavior_path, findings)
    script_path = root / "scripts.json"
    if script_path.exists():
        scripts = load(script_path, findings)
        if scripts:
            items = common_cases(scripts, script_path, findings)
            for case in items:
                if not isinstance(case.get("script"), str) or not case["script"]:
                    findings.append(Finding("script", f"case {case.get('id', '?')} needs script", str(script_path)))
                if not isinstance(case.get("args"), list) or any(not isinstance(item, str) for item in case["args"]):
                    findings.append(Finding("script", f"case {case.get('id', '?')} needs an array of string args", str(script_path)))
                if not isinstance(case.get("expected_exit"), int) or isinstance(case.get("expected_exit"), bool) or not isinstance(case.get("side_effect_policy"), str) or not case["side_effect_policy"].strip():
                    findings.append(Finding("script", f"case {case.get('id', '?')} needs expected_exit and side_effect_policy", str(script_path)))
                if "expected_json" in case and not isinstance(case["expected_json"], dict):
                    findings.append(Finding("script", f"case {case.get('id', '?')} expected_json must be an object", str(script_path)))
            validate_holdout_policy(scripts, items, script_path, findings)
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
            print("Evaluation datasets are structurally complete.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
