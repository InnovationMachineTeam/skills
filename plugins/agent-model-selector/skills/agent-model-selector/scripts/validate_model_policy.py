#!/usr/bin/env python3
"""Validate an agent model-selection policy without external dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
DECISIONS = {"RECOMMEND", "CONDITIONAL", "RESEARCH_REQUIRED", "INCONCLUSIVE", "REJECT"}
RISKS = {"R0", "R1", "R2", "R3"}


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(data: object) -> list[str]:
    failures: list[str] = []
    if not isinstance(data, dict):
        return ["root must be an object"]
    if data.get("schema_version") != 1:
        failures.append("schema_version must be 1")
    if not nonempty(data.get("policy_id")) or not str(data.get("policy_id", "")).startswith("model-policy://"):
        failures.append("policy_id must start with model-policy://")
    if not isinstance(data.get("version"), str) or not SEMVER.fullmatch(data["version"]):
        failures.append("version must be SemVer")
    for key in ("checked_at", "next_review_at", "accountable_owner"):
        if not nonempty(data.get(key)):
            failures.append(f"{key} is required")
    if not isinstance(data.get("target_hosts"), list) or not data["target_hosts"]:
        failures.append("target_hosts must be a non-empty array")
    sources = data.get("sources")
    source_ids: set[str] = set()
    if not isinstance(sources, list) or not sources:
        failures.append("sources must be a non-empty array")
    else:
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                failures.append(f"sources[{index}] must be an object")
                continue
            source_id = source.get("id")
            if not nonempty(source_id) or source_id in source_ids:
                failures.append(f"sources[{index}].id must be non-empty and unique")
            else:
                source_ids.add(str(source_id))
            for key in ("url", "authority", "checked_at"):
                if not nonempty(source.get(key)):
                    failures.append(f"sources[{index}].{key} is required")
            if not isinstance(source.get("claims"), list) or not source["claims"]:
                failures.append(f"sources[{index}].claims must be non-empty")
    roles = data.get("roles")
    role_ids: set[str] = set()
    if not isinstance(roles, list) or not roles:
        failures.append("roles must be a non-empty array")
    else:
        for index, role in enumerate(roles):
            if not isinstance(role, dict):
                failures.append(f"roles[{index}] must be an object")
                continue
            role_id = role.get("id")
            if not nonempty(role_id) or role_id in role_ids:
                failures.append(f"roles[{index}].id must be non-empty and unique")
            else:
                role_ids.add(str(role_id))
            if role.get("risk_tier") not in RISKS:
                failures.append(f"roles[{index}].risk_tier is invalid")
            if role.get("decision") not in DECISIONS:
                failures.append(f"roles[{index}].decision is invalid")
            for key in ("task_classes", "requirements", "fallback", "escalate_when", "stop_when", "evidence_refs", "benchmark_refs"):
                if not isinstance(role.get(key), list):
                    failures.append(f"roles[{index}].{key} must be an array")
            evidence = role.get("evidence_refs", [])
            unknown = [item for item in evidence if item not in source_ids]
            if unknown:
                failures.append(f"roles[{index}] references unknown evidence: {unknown}")
            if role.get("decision") == "RECOMMEND":
                if not nonempty(role.get("preferred")):
                    failures.append(f"roles[{index}].preferred is required for RECOMMEND")
                if not evidence or not role.get("benchmark_refs"):
                    failures.append(f"roles[{index}] RECOMMEND requires evidence and benchmark refs")
    if not isinstance(data.get("re_evaluate_on"), list) or not data["re_evaluate_on"]:
        failures.append("re_evaluate_on must be a non-empty array")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.policy.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    failures = validate(data)
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        return 1
    print("PASS model policy is structurally valid and evidence-linked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
