#!/usr/bin/env python3
"""Validate an individual-agent candidate against core portable invariants."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path, PurePosixPath


def fail(message: str) -> None:
    print(f"FAIL {message}", file=sys.stderr)


def safe_docs_path(value: object, allow_root: bool = True) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return False
    if not path.parts or path.parts[0] != "docs":
        return False
    return allow_root or len(path.parts) > 1


def main() -> int:
    if len(sys.argv) != 2:
        fail("usage: validate_agent_candidate.py AGENT.json")
        return 2
    path = Path(sys.argv[1])
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(str(exc))
        return 1
    required = {"schema_version", "id", "name", "version", "accountable_owner", "mission", "risk_tier", "model_policy", "tools", "permissions", "documentation", "runtime", "lifecycle"}
    missing = sorted(required - value.keys())
    errors = [f"missing {item}" for item in missing]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(value.get("name", ""))):
        errors.append("invalid name")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(value.get("version", ""))):
        errors.append("invalid version")
    docs = value.get("documentation", {})
    for key in ("read_roots", "write_roots", "artifacts", "indexes_to_update", "freshness_rules", "validation"):
        if key not in docs:
            errors.append(f"documentation missing {key}")
    for key in ("read_roots", "write_roots"):
        for root in docs.get(key, []):
            if not safe_docs_path(root):
                errors.append(f"documentation {key} escapes docs: {root}")
    for index in docs.get("indexes_to_update", []):
        if not safe_docs_path(index, allow_root=False):
            errors.append(f"documentation index escapes docs: {index}")
    artifact_required = {"type", "path_pattern", "owner", "reviewers", "consumers", "source_of_truth", "decision_authority", "freshness", "supersession"}
    for position, artifact in enumerate(docs.get("artifacts", [])):
        if not isinstance(artifact, dict):
            errors.append(f"documentation artifact {position} must be an object")
            continue
        for key in sorted(artifact_required - artifact.keys()):
            errors.append(f"documentation artifact {position} missing {key}")
        if not safe_docs_path(artifact.get("path_pattern"), allow_root=False):
            errors.append(f"documentation artifact {position} path escapes docs")
        if not artifact.get("owner"):
            errors.append(f"documentation artifact {position} owner is required")
        if not isinstance(artifact.get("consumers"), list) or not artifact.get("consumers"):
            errors.append(f"documentation artifact {position} needs a consumer")
        if not isinstance(artifact.get("reviewers"), list):
            errors.append(f"documentation artifact {position} reviewers must be a list")
        if not artifact.get("freshness"):
            errors.append(f"documentation artifact {position} freshness is required")
    if errors:
        for error in errors:
            fail(error)
        return 1
    print(f"PASS agent candidate: {value['name']}@{value['version']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
