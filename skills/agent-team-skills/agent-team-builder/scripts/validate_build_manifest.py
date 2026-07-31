#!/usr/bin/env python3
"""Validate a staged agent-team build manifest."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath

SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
ACTIONS = {"create", "update-generated", "register", "map", "validate"}
VISIBILITY = {"public", "private", "internal"}


def text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def safe_relative(path: object) -> bool:
    if not text(path):
        return False
    pure = PurePosixPath(str(path))
    return not pure.is_absolute() and ".." not in pure.parts


def validate(data: object) -> list[str]:
    failures: list[str] = []
    if not isinstance(data, dict):
        return ["root must be an object"]
    if data.get("schema_version") != 1 or not text(data.get("build_id")):
        failures.append("schema_version 1 and build_id are required")
    spec = data.get("spec")
    if not isinstance(spec, dict):
        failures.append("spec must be an object")
    else:
        if not text(spec.get("id")) or not isinstance(spec.get("version"), str) or not SEMVER.fullmatch(spec["version"]):
            failures.append("spec id and SemVer version are required")
        if spec.get("status") != "approved" or not re.fullmatch(r"sha256:[0-9a-f]{64}", str(spec.get("hash", ""))):
            failures.append("spec must be approved and have a sha256 digest")
    if not safe_relative(data.get("destination")):
        failures.append("destination must be a safe relative path")
    if data.get("activation") is not False:
        failures.append("build manifests must set activation to false")
    revisions = data.get("expected_revisions")
    if not isinstance(revisions, dict) or not all(text(revisions.get(k)) for k in ("registry", "map")):
        failures.append("expected registry and map revisions are required")
    operations = data.get("operations")
    if not isinstance(operations, list) or not operations:
        failures.append("operations must be non-empty")
        operations = []
    seen: set[str] = set()
    for index, op in enumerate(operations):
        label = f"operations[{index}]"
        if not isinstance(op, dict) or op.get("action") not in ACTIONS:
            failures.append(f"{label} has invalid action")
            continue
        path = op.get("path")
        if not safe_relative(path) or path in seen:
            failures.append(f"{label}.path must be safe and unique")
            continue
        seen.add(str(path))
        if op.get("visibility") not in VISIBILITY:
            failures.append(f"{label}.visibility is invalid")
        if op.get("visibility") == "private":
            owner = op.get("owner_agent_ref")
            if not text(owner) or op.get("allowed_consumers") != [owner]:
                failures.append(f"{label} has invalid private owner/consumers")
            agent_id = str(owner).rsplit("/", 1)[-1] if text(owner) else ""
            if agent_id not in PurePosixPath(str(path)).parts:
                failures.append(f"{label} private path is outside owner directory")
            if str(path).startswith(("skills/", "plugins/", "catalog/")):
                failures.append(f"{label} attempts to package a private asset")
        if op.get("collision_policy") not in {"absent", "generated-compatible", "stale-generated", "stop"}:
            failures.append(f"{label}.collision_policy is invalid")
    if not isinstance(data.get("validations"), list) or not data["validations"]:
        failures.append("validations must be non-empty")
    rollback = data.get("rollback")
    if not isinstance(rollback, dict) or not text(rollback.get("backup_path")) or not text(rollback.get("procedure")):
        failures.append("rollback backup_path and procedure are required")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    failures = validate(data)
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        return 1
    print("PASS agent-team build manifest is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
