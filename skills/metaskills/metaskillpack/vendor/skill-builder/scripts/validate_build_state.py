#!/usr/bin/env python3
"""Validate a skill-builder orchestration state file."""

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
    "specialist-dispatch",
    "resume-build",
}
ROOT_STATUSES = {"planned", "in_progress", "waiting_approval", "blocked", "completed", "aborted"}
PHASE_STATUSES = {
    "pending",
    "in_progress",
    "completed",
    "rejected",
    "inconclusive",
    "waiting_approval",
    "blocked",
    "skipped",
}
SPECIALISTS = {
    "skill-scout",
    "skill-harvester",
    "skill-architect",
    "skill-evaluator",
    "skill-doctor",
    "skill-optimizer",
    "skill-refactor",
    "skill-manager",
    "prompt-optimize",
    "skill-builder",
}
AUTHORITY_KEYS = {"write", "external_research", "install", "publish", "retire"}


@dataclass
class Finding:
    code: str
    message: str
    path: str


def add(findings: list[Finding], code: str, message: str, path: str) -> None:
    findings.append(Finding(code, message, path))


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonempty_strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(nonempty_string(item) for item in value)


def validate_authority(value: Any, findings: list[Finding], path: str) -> None:
    if not isinstance(value, dict):
        add(findings, "authority", "authority must be an object", path)
        return
    missing = AUTHORITY_KEYS - set(value)
    if missing:
        add(findings, "authority", "missing authority keys: " + ", ".join(sorted(missing)), path)
    for key in AUTHORITY_KEYS & set(value):
        if not isinstance(value[key], bool):
            add(findings, "authority", f"{key} must be boolean", f"{path}.{key}")


def validate_state(value: Any) -> list[Finding]:
    findings: list[Finding] = []
    if not isinstance(value, dict):
        return [Finding("root", "state root must be an object", "$")]

    if value.get("schema_version") != 1:
        add(findings, "schema-version", "schema_version must equal 1", "$.schema_version")
    if value.get("builder") != "skill-builder":
        add(findings, "builder", "builder must equal skill-builder", "$.builder")
    if not nonempty_string(value.get("build_id")):
        add(findings, "build-id", "build_id must be a non-empty string", "$.build_id")
    if value.get("scenario") not in SCENARIOS:
        add(findings, "scenario", "unknown scenario", "$.scenario")
    if not nonempty_string(value.get("goal")):
        add(findings, "goal", "goal must be a non-empty string", "$.goal")
    if value.get("status") not in ROOT_STATUSES:
        add(findings, "status", "unknown root status", "$.status")
    if not nonempty_strings(value.get("scope")):
        add(findings, "scope", "scope must contain at least one exact target", "$.scope")
    if not nonempty_strings(value.get("acceptance_criteria")):
        add(findings, "acceptance", "acceptance_criteria must be a non-empty string array", "$.acceptance_criteria")
    validate_authority(value.get("authority"), findings, "$.authority")

    phases = value.get("phases")
    if not isinstance(phases, list) or not phases:
        add(findings, "phases", "phases must be a non-empty array", "$.phases")
        return findings

    ids: set[str] = set()
    phase_by_id: dict[str, dict[str, Any]] = {}
    required_incomplete = False
    for index, phase in enumerate(phases):
        path = f"$.phases[{index}]"
        if not isinstance(phase, dict):
            add(findings, "phase", "phase must be an object", path)
            continue
        phase_id = phase.get("id")
        if not nonempty_string(phase_id):
            add(findings, "phase-id", "phase id must be a non-empty string", f"{path}.id")
        elif phase_id in ids:
            add(findings, "phase-id", f"duplicate phase id: {phase_id}", f"{path}.id")
        else:
            ids.add(phase_id)
            phase_by_id[phase_id] = phase
        if phase.get("specialist") not in SPECIALISTS:
            add(findings, "specialist", "unknown specialist", f"{path}.specialist")
        if not nonempty_string(phase.get("objective")):
            add(findings, "objective", "phase objective must be a non-empty string", f"{path}.objective")
        if phase.get("status") not in PHASE_STATUSES:
            add(findings, "phase-status", "unknown phase status", f"{path}.status")
        dependencies = phase.get("dependencies")
        if not isinstance(dependencies, list) or not all(nonempty_string(item) for item in dependencies):
            add(findings, "dependencies", "dependencies must be a string array", f"{path}.dependencies")
        for key in ("entry_conditions", "required_outputs", "exit_checks"):
            if not nonempty_strings(phase.get(key)):
                add(findings, "phase-contract", f"{key} must be a non-empty string array", f"{path}.{key}")
        validate_authority(phase.get("authority"), findings, f"{path}.authority")
        evidence = phase.get("evidence")
        if not isinstance(evidence, list):
            add(findings, "evidence", "evidence must be an array", f"{path}.evidence")
        if phase.get("required", True) and phase.get("status") not in {"completed", "skipped"}:
            required_incomplete = True

    for index, phase in enumerate(phases):
        if not isinstance(phase, dict):
            continue
        for dependency in phase.get("dependencies", []):
            if dependency not in ids:
                add(findings, "dependency", f"unknown dependency: {dependency}", f"$.phases[{index}].dependencies")
            elif dependency == phase.get("id"):
                add(findings, "dependency", "phase cannot depend on itself", f"$.phases[{index}].dependencies")

    if value.get("status") == "completed" and required_incomplete:
        add(findings, "false-completion", "completed root has an incomplete required phase", "$.status")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    path = args.state.expanduser().resolve()
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        findings = [Finding("json", f"cannot read valid JSON: {exc}", str(path))]
    else:
        findings = validate_state(value)

    if args.format == "json":
        print(json.dumps({"valid": not findings, "count": len(findings), "findings": [asdict(item) for item in findings]}, ensure_ascii=False, indent=2))
    else:
        print(f"Findings: {len(findings)}")
        for finding in findings:
            print(f"[ERROR] {finding.code}: {finding.message} ({finding.path})")
        if not findings:
            print("Build state is structurally valid.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
