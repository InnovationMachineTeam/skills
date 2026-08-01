#!/usr/bin/env python3
"""Validate resumable agent-master Agent Harness state schema version 2."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT_STATUSES = {
    "planned", "in_progress", "awaiting_human_decision", "blocked",
    "completed", "aborted",
}
PHASE_STATUSES = {
    "pending", "in_progress", "completed", "rejected", "inconclusive",
    "awaiting_human_decision", "blocked", "skipped",
}
EXECUTION_MODES = {"advisory", "assisted", "supervised", "autonomous", "review-only"}
VISIBILITY_MODES = {"public", "private"}
AUTHORITY_FIELDS = {
    "write", "external_research", "install", "publish", "runtime_activate",
    "production", "destructive", "spend",
}
REQUIRED_PHASES = {
    "analyze", "research-harness", "select-harness", "design-harness",
    "design-orchestrator", "design-role-agents", "design-role-skills",
    "implement-components", "integrate-evaluate", "improve", "document-handoff",
}
COMPONENT_STATUSES = {
    "Proposed", "Researched", "Designed", "Implemented", "Testing",
    "Evaluated", "Integrated", "Validated", "Stable", "Needs Improvement",
    "Deprecated", "Archived",
}
DECISION_STATUSES = {"open", "approved", "rejected", "expired", "cancelled"}


def text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_list(value: object) -> bool:
    return isinstance(value, list) and all(text(item) for item in value)


def validate_authority(value: object, label: str, findings: list[str]) -> None:
    if not isinstance(value, dict):
        findings.append(f"{label} must be an object")
        return
    for field in AUTHORITY_FIELDS:
        if not isinstance(value.get(field), bool):
            findings.append(f"{label}.{field} must be boolean")


def validate_visibility(value: object, findings: list[str]) -> None:
    if not isinstance(value, dict):
        findings.append("visibility must be an object")
        return
    if value.get("mode") not in VISIBILITY_MODES:
        findings.append("visibility.mode must be public or private")
    if value.get("selected_by") != "user":
        findings.append("visibility.selected_by must be user")
    if not text(value.get("selected_at")):
        findings.append("visibility.selected_at is required")


def validate(data: object) -> list[str]:
    findings: list[str] = []
    if not isinstance(data, dict):
        return ["root must be an object"]
    if data.get("schema_version") != 2 or data.get("master") != "agent-master":
        findings.append("schema_version 2 and master agent-master are required")
    for field in ("run_id", "goal", "updated_at"):
        if not text(data.get(field)):
            findings.append(f"{field} is required")
    if data.get("status") not in ROOT_STATUSES:
        findings.append("invalid root status")
    if data.get("execution_mode") not in EXECUTION_MODES:
        findings.append("invalid execution_mode")
    validate_visibility(data.get("visibility"), findings)
    validate_authority(data.get("authority"), "authority", findings)

    for field in ("scope", "acceptance_criteria"):
        if not string_list(data.get(field)) or not data.get(field):
            findings.append(f"{field} must be a non-empty string array")
    for field in (
        "components", "artifacts", "decisions", "findings", "assumptions",
        "human_decisions", "risks",
    ):
        if not isinstance(data.get(field), list):
            findings.append(f"{field} must be an array")

    phases = data.get("phases")
    if not isinstance(phases, list) or not phases:
        findings.append("phases must be a non-empty array")
        return findings
    if not all(isinstance(phase, dict) for phase in phases):
        findings.append("every phase must be an object")
        return findings
    ids = [phase.get("id") for phase in phases]
    if not all(text(item) for item in ids):
        findings.append("every phase requires a string id")
        return findings
    if len(ids) != len(set(ids)):
        findings.append("phase ids must be unique")
    missing_phases = sorted(REQUIRED_PHASES - set(ids))
    if missing_phases:
        findings.append(f"missing required phases: {', '.join(missing_phases)}")

    known = set(ids)
    graph: dict[str, list[str]] = {}
    for index, phase in enumerate(phases):
        label = f"phases[{index}]"
        for field in ("owner", "objective"):
            if not text(phase.get(field)):
                findings.append(f"{label}.{field} is required")
        if phase.get("status") not in PHASE_STATUSES:
            findings.append(f"{label}.status is invalid")
        for field in (
            "dependencies", "entry_conditions", "required_outputs",
            "exit_checks", "evidence",
        ):
            if not string_list(phase.get(field)):
                findings.append(f"{label}.{field} must be a string array")
        if not isinstance(phase.get("retry_count"), int) or phase.get("retry_count", -1) < 0:
            findings.append(f"{label}.retry_count must be a non-negative integer")
        validate_authority(phase.get("authority"), f"{label}.authority", findings)
        dependencies = phase.get("dependencies", [])
        if any(item not in known for item in dependencies):
            findings.append(f"{label}.dependencies contains an unknown phase")
        if phase["id"] in dependencies:
            findings.append(f"{label} cannot depend on itself")
        graph[str(phase["id"])] = dependencies if isinstance(dependencies, list) else []
        if phase.get("status") == "skipped" and not phase.get("evidence"):
            findings.append(f"{label} skipped phase requires evidence")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            findings.append("phase dependency graph contains a cycle")
            return
        if node in visited:
            return
        visiting.add(node)
        for dependency in graph.get(node, []):
            visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for phase_id in graph:
        visit(phase_id)

    components = data.get("components", [])
    if isinstance(components, list):
        component_ids: set[str] = set()
        for index, component in enumerate(components):
            label = f"components[{index}]"
            if not isinstance(component, dict):
                findings.append(f"{label} must be an object")
                continue
            for field in ("id", "kind", "name", "version", "owner", "visibility", "locator"):
                if not text(component.get(field)):
                    findings.append(f"{label}.{field} is required")
            component_id = component.get("id")
            if text(component_id):
                if component_id in component_ids:
                    findings.append(f"duplicate component id: {component_id}")
                component_ids.add(str(component_id))
            if component.get("status") not in COMPONENT_STATUSES:
                findings.append(f"{label}.status is invalid")
            if not string_list(component.get("evidence")):
                findings.append(f"{label}.evidence must be a string array")
            if component.get("visibility") == "package_private":
                if component.get("allowed_consumers") != ["agent-master"]:
                    findings.append(f"{label} package-private consumer must be agent-master")
            elif component.get("visibility") not in {"public", "private"}:
                findings.append(f"{label}.visibility is invalid")
            if component.get("status") == "Stable" and not component.get("evidence"):
                findings.append(f"{label} Stable component requires evidence")

    human_decisions = data.get("human_decisions", [])
    open_blocking = False
    if isinstance(human_decisions, list):
        for index, decision in enumerate(human_decisions):
            label = f"human_decisions[{index}]"
            if not isinstance(decision, dict):
                findings.append(f"{label} must be an object")
                continue
            for field in ("id", "operation", "reason"):
                if not text(decision.get(field)):
                    findings.append(f"{label}.{field} is required")
            if decision.get("status") not in DECISION_STATUSES:
                findings.append(f"{label}.status is invalid")
            if decision.get("blocking") is not None and not isinstance(decision.get("blocking"), bool):
                findings.append(f"{label}.blocking must be boolean")
            if decision.get("status") == "open" and decision.get("blocking", True):
                open_blocking = True

    if open_blocking and data.get("status") != "awaiting_human_decision":
        findings.append("open blocking human decision requires awaiting_human_decision root status")
    if data.get("status") == "completed":
        if any(phase.get("status") not in {"completed", "skipped"} for phase in phases):
            findings.append("completed root requires every phase completed or skipped")
        if open_blocking:
            findings.append("completed root cannot have open blocking human decisions")
        for finding in data.get("findings", []):
            if isinstance(finding, dict) and finding.get("severity") == "critical" and finding.get("status") not in {"resolved", "accepted"}:
                findings.append("completed root cannot have unresolved critical findings")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path)
    parser.add_argument("--json", action="store_true", help="emit machine-readable diagnostics")
    args = parser.parse_args()
    try:
        data = json.loads(args.state.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        if args.json:
            print(json.dumps({"valid": False, "findings": [str(exc)]}))
        else:
            print(f"ERROR {exc}", file=sys.stderr)
        return 2
    findings = validate(data)
    if args.json:
        print(json.dumps({"valid": not findings, "findings": findings}, ensure_ascii=False))
    else:
        for finding in findings:
            print(f"FAIL {finding}")
        if not findings:
            print("PASS agent-master state is valid")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
