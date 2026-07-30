#!/usr/bin/env python3
"""Validate a skill-refactor plan and destructive-operation gates."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


DECISIONS = {"KEEP_SEPARATE", "COMPOSE", "MERGE", "SPLIT", "EXTRACT_REFERENCE", "EXTRACT_SUBSKILL", "CREATE_FACADE"}
ACTIONS = {"KEEP", "COPY", "MOVE", "CREATE", "UPDATE", "DELETE"}
STATUSES = {"proposed", "approved", "applied", "verified"}


@dataclass
class Finding:
    code: str
    message: str
    location: str


def text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(value: object) -> list[Finding]:
    findings: list[Finding] = []
    if not isinstance(value, dict):
        return [Finding("root", "Plan root must be an object.", "/")]
    for key in ("schema_version", "plan_id", "rationale", "rollback"):
        if not text(value.get(key)):
            findings.append(Finding("required", f"{key} must be a non-empty string.", f"/{key}"))
    if value.get("schema_version") != "1.0":
        findings.append(Finding("schema", "schema_version must be 1.0.", "/schema_version"))
    if value.get("decision") not in DECISIONS:
        findings.append(Finding("decision", "Invalid decision.", "/decision"))
    if value.get("approval_status") not in STATUSES:
        findings.append(Finding("approval", "Invalid approval_status.", "/approval_status"))
    for key in ("inputs", "outputs", "preserved_invariants", "trigger_ownership", "resource_ownership", "consumer_migrations", "file_operations", "validation"):
        raw = value.get(key)
        if not isinstance(raw, list):
            findings.append(Finding("array", f"{key} must be an array.", f"/{key}"))
    for key in ("inputs", "preserved_invariants", "validation"):
        if isinstance(value.get(key), list) and not value[key]:
            findings.append(Finding("nonempty", f"{key} must not be empty.", f"/{key}"))
    operations = value.get("file_operations")
    if isinstance(operations, list):
        for index, operation in enumerate(operations):
            where = f"/file_operations/{index}"
            if not isinstance(operation, dict) or operation.get("action") not in ACTIONS:
                findings.append(Finding("operation", "Operation must be an object with a valid action.", where))
                continue
            if not text(operation.get("target")):
                findings.append(Finding("target", "Every operation requires an exact target.", where))
            if operation.get("action") in {"COPY", "MOVE", "UPDATE", "DELETE"} and not text(operation.get("source")):
                findings.append(Finding("source", "This operation requires an exact source.", where))
            if operation.get("action") == "DELETE" and value.get("approval_status") not in {"approved", "applied", "verified"}:
                findings.append(Finding("delete-approval", "DELETE requires approved status.", where))
            if operation.get("action") == "DELETE" and not text(operation.get("recovery")):
                findings.append(Finding("delete-recovery", "DELETE requires operation-level recovery evidence.", where))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    try:
        value = json.loads(args.plan.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"Error: cannot read valid JSON: {exc}", file=sys.stderr)
        return 2
    findings = validate(value)
    if args.format == "json":
        print(json.dumps({"count": len(findings), "findings": [asdict(item) for item in findings]}, ensure_ascii=False, indent=2))
    else:
        print(f"Findings: {len(findings)}")
        for item in findings:
            print(f"[ERROR] {item.code}: {item.message} ({item.location})")
        if not findings:
            print("Refactor plan is structurally valid and passes destructive-operation gates.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
