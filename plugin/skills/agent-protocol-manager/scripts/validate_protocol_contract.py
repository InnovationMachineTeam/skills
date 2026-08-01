#!/usr/bin/env python3
"""Validate an agent protocol and host adapter contract candidate."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


STATUSES = {"candidate", "verified", "approved", "active", "suspended", "deprecated", "retired"}
OUTCOMES = {"native", "generated", "unsupported"}
BOUNDARIES = {"mcp", "a2a", "host", "provider"}


def text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_list(value: object) -> bool:
    return isinstance(value, list) and all(text(item) for item in value)


def validate(data: object) -> list[str]:
    findings: list[str] = []
    if not isinstance(data, dict):
        return ["root must be an object"]
    if data.get("schema_version") != 1:
        findings.append("schema_version must be 1")
    for field in ("contract_id", "version", "owner", "checked_at", "canonical_contract_ref", "upgrade_ref", "rollback_ref"):
        if not text(data.get(field)):
            findings.append(f"{field} is required")
    if data.get("status") not in STATUSES:
        findings.append("invalid status")
    if not string_list(data.get("conformance_refs")) or not data.get("conformance_refs"):
        findings.append("conformance_refs must be a non-empty string array")

    adapters = data.get("adapters")
    if not isinstance(adapters, list) or not adapters:
        findings.append("adapters must be a non-empty array")
        return findings
    ids: set[str] = set()
    for index, adapter in enumerate(adapters):
        label = f"adapters[{index}]"
        if not isinstance(adapter, dict):
            findings.append(f"{label} must be an object")
            continue
        for field in ("id", "protocol", "version", "direction", "authentication", "error_model", "retry_policy", "idempotency", "credential_ref"):
            if not text(adapter.get(field)):
                findings.append(f"{label}.{field} is required")
        if adapter.get("boundary") not in BOUNDARIES:
            findings.append(f"{label}.boundary is invalid")
        if adapter.get("outcome") not in OUTCOMES:
            findings.append(f"{label}.outcome is invalid")
        for field in ("capabilities", "unsupported_features", "schemas", "data_classes", "conformance_cases"):
            if not string_list(adapter.get(field)):
                findings.append(f"{label}.{field} must be a string array")
        for field in ("streaming", "cancellation", "provenance_required"):
            if not isinstance(adapter.get(field), bool):
                findings.append(f"{label}.{field} must be boolean")
        for field in ("timeout_ms", "max_payload_bytes", "retry_budget"):
            value = adapter.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                findings.append(f"{label}.{field} must be a non-negative integer")
        if adapter.get("outcome") == "unsupported" and not adapter.get("unsupported_features"):
            findings.append(f"{label} unsupported outcome requires unsupported_features")
        adapter_id = adapter.get("id")
        if text(adapter_id):
            if adapter_id in ids:
                findings.append("adapter ids must be unique")
            ids.add(adapter_id)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.contract.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    findings = validate(data)
    for finding in findings:
        print(f"FAIL {finding}")
    if findings:
        return 1
    print("PASS protocol contract is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
