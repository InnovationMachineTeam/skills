#!/usr/bin/env python3
"""Validate a versioned skill evaluation plan."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


LAYERS = {"routing", "behavior", "structure", "scripts-tools", "security-authority", "catalog-coexistence", "portability", "lifecycle", "user-outcome"}
RISKS = {"low", "medium", "high", "critical"}
HASH = re.compile(r"^sha256:[0-9a-f]{64}$")


@dataclass
class Finding:
    code: str
    message: str
    path: str


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonnegative_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0


def nonempty_strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(nonempty_string(item) for item in value)


def meaningful_criterion(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, dict):
        return bool(value)
    if isinstance(value, list):
        return bool(value)
    return isinstance(value, (int, float, bool))


def validate(value: Any, path: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not isinstance(value, dict) or value.get("schema_version") != "1.0":
        return [Finding("root", "plan must be an object with schema_version 1.0", str(path))]
    for key in ("evaluation_id", "objective"):
        if not nonempty_string(value.get(key)):
            findings.append(Finding("field", f"{key} must be a non-empty string", str(path)))
    if value.get("risk") not in RISKS:
        findings.append(Finding("risk", "risk must be low, medium, high, or critical", str(path)))
    target = value.get("target")
    if not isinstance(target, dict) or not nonempty_string(target.get("identity")) or not HASH.fullmatch(target.get("hash", "")):
        findings.append(Finding("target", "target requires identity and sha256 hash", str(path)))
    environment = value.get("environment")
    if not isinstance(environment, dict) or not nonempty_string(environment.get("host")):
        findings.append(Finding("environment", "environment requires at least host", str(path)))
    authority = value.get("authority")
    if not isinstance(authority, dict) or any(not isinstance(authority.get(key), bool) for key in ("read", "write", "external")):
        findings.append(Finding("authority", "authority requires boolean read, write, and external", str(path)))
    layers = value.get("layers")
    if not isinstance(layers, list) or not layers or any(layer not in LAYERS for layer in layers) or len(layers) != len(set(layers)):
        findings.append(Finding("layers", "layers must be a non-empty unique list of known layers", str(path)))
    baselines = value.get("baselines")
    if not isinstance(baselines, list) or not baselines or any(not nonempty_string(item) for item in baselines):
        findings.append(Finding("baselines", "baselines must contain at least one named baseline", str(path)))
    metrics = value.get("metrics")
    if not isinstance(metrics, list) or not metrics or any(not nonempty_string(item) for item in metrics):
        findings.append(Finding("metrics", "metrics must contain at least one metric", str(path)))
    if not nonempty_strings(value.get("datasets")):
        findings.append(Finding("datasets", "datasets must contain at least one versioned dataset or fixture identity", str(path)))
    if not nonempty_strings(value.get("graders")):
        findings.append(Finding("graders", "graders must identify deterministic, rubric, model, or human graders", str(path)))
    repetitions = value.get("repetitions")
    if not isinstance(repetitions, int) or isinstance(repetitions, bool) or repetitions < 1:
        findings.append(Finding("repetitions", "repetitions must be a positive integer", str(path)))
    timeouts = value.get("timeouts")
    if not isinstance(timeouts, dict) or not nonnegative_number(timeouts.get("max_case_seconds")):
        findings.append(Finding("timeouts", "timeouts requires non-negative max_case_seconds", str(path)))
    budget = value.get("budget")
    if not isinstance(budget, dict) or any(not nonnegative_number(budget.get(key)) for key in ("max_runs", "max_seconds", "max_cost")):
        findings.append(Finding("budget", "budget requires non-negative max_runs, max_seconds, and max_cost", str(path)))
    acceptance = value.get("acceptance")
    if not isinstance(acceptance, dict) or not isinstance(acceptance.get("blocking_layers"), list) or not isinstance(acceptance.get("criteria"), dict):
        findings.append(Finding("acceptance", "acceptance requires blocking_layers and criteria object", str(path)))
    else:
        if any(layer not in (layers or []) for layer in acceptance["blocking_layers"]):
            findings.append(Finding("acceptance", "blocking_layers must be selected evaluation layers", str(path)))
        missing_criteria = set(layers or []) - set(acceptance["criteria"])
        if missing_criteria:
            findings.append(Finding("acceptance", "missing criteria for layers: " + ", ".join(sorted(missing_criteria)), str(path)))
        if any(not meaningful_criterion(criterion) for criterion in acceptance["criteria"].values()):
            findings.append(Finding("acceptance", "every layer criterion must be meaningful", str(path)))
    holdout = value.get("holdout_policy")
    if not isinstance(holdout, dict) or not isinstance(holdout.get("protected"), bool) or not nonempty_string(holdout.get("exposure_rule")):
        findings.append(Finding("holdout", "holdout_policy requires protected and exposure_rule", str(path)))
    artifacts = value.get("artifacts")
    if not isinstance(artifacts, dict) or not nonempty_string(artifacts.get("raw_output_dir")):
        findings.append(Finding("artifacts", "artifacts requires raw_output_dir", str(path)))
    execution = value.get("execution_policy")
    if not isinstance(execution, dict) or not nonempty_string(execution.get("side_effects")) or not nonempty_strings(execution.get("abort_conditions")) or not nonempty_string(execution.get("cleanup")):
        findings.append(Finding("execution", "execution_policy requires side_effects, abort_conditions, and cleanup", str(path)))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    path = args.plan.expanduser().resolve()
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        findings = validate(value, path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        findings = [Finding("json", f"cannot read valid JSON: {exc}", str(path))]
    payload = {"valid": not findings, "count": len(findings), "findings": [asdict(item) for item in findings]}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Findings: {len(findings)}")
        for item in findings:
            print(f"[ERROR] {item.code}: {item.message} ({item.path})")
        if not findings:
            print("Evaluation plan is structurally valid.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
