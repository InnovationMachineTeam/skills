#!/usr/bin/env python3
"""Validate a pinned runtime model-routing policy candidate."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


STATUSES = {"candidate", "verified", "approved", "active", "suspended", "deprecated", "retired"}
MODES = {"fixed", "tiered", "dynamic"}


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
    for field in ("policy_id", "version", "owner", "checked_at", "policy_ref", "rollback_ref"):
        if not text(data.get(field)):
            findings.append(f"{field} is required")
    if data.get("status") not in STATUSES:
        findings.append("invalid status")
    if data.get("mode") not in MODES:
        findings.append("invalid routing mode")
    if not isinstance(data.get("feature_schema"), dict) or not data.get("feature_schema"):
        findings.append("feature_schema must be a non-empty object")
    if not string_list(data.get("evaluation_refs")) or not data.get("evaluation_refs"):
        findings.append("evaluation_refs must be a non-empty string array")
    if not string_list(data.get("drift_signals")) or not data.get("drift_signals"):
        findings.append("drift_signals must be a non-empty string array")

    models = data.get("approved_models")
    if not isinstance(models, list) or not models:
        findings.append("approved_models must be a non-empty array")
        return findings
    model_ids: set[str] = set()
    for index, model in enumerate(models):
        label = f"approved_models[{index}]"
        if not isinstance(model, dict):
            findings.append(f"{label} must be an object")
            continue
        for field in ("ref", "provider", "model_id", "version", "evidence_ref", "checked_at"):
            if not text(model.get(field)):
                findings.append(f"{label}.{field} is required")
        for field in ("hosts", "data_classes", "tools", "modalities"):
            if not string_list(model.get(field)):
                findings.append(f"{label}.{field} must be a string array")
        ref = model.get("ref")
        if text(ref):
            if ref in model_ids:
                findings.append("approved model refs must be unique")
            model_ids.add(ref)

    routes = data.get("routes")
    if not isinstance(routes, list) or not routes:
        findings.append("routes must be a non-empty array")
        return findings
    route_ids: set[str] = set()
    for index, route in enumerate(routes):
        label = f"routes[{index}]"
        if not isinstance(route, dict):
            findings.append(f"{label} must be an object")
            continue
        for field in ("id", "task_class", "risk_tier", "model_ref", "quality_floor", "hard_stop"):
            if not text(route.get(field)):
                findings.append(f"{label}.{field} is required")
        for field in ("confidence_threshold", "max_latency_ms", "max_cost_usd"):
            value = route.get(field)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
                findings.append(f"{label}.{field} must be a non-negative number")
        if isinstance(route.get("confidence_threshold"), (int, float)) and route["confidence_threshold"] > 1:
            findings.append(f"{label}.confidence_threshold must be at most 1")
        if route.get("model_ref") not in model_ids:
            findings.append(f"{label}.model_ref is not approved")
        if not string_list(route.get("fallback_refs")):
            findings.append(f"{label}.fallback_refs must be a string array")
        elif any(ref not in model_ids for ref in route["fallback_refs"]):
            findings.append(f"{label}.fallback_refs contains an unapproved model")
        route_id = route.get("id")
        if text(route_id):
            if route_id in route_ids:
                findings.append("route ids must be unique")
            route_ids.add(route_id)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.policy.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    findings = validate(data)
    for finding in findings:
        print(f"FAIL {finding}")
    if findings:
        return 1
    print("PASS model-routing policy is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
