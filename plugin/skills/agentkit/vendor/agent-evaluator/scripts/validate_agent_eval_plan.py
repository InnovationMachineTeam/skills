#!/usr/bin/env python3
"""Validate a portable individual-agent evaluation plan."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ALLOWED = {"definition", "routing", "outcome", "tools-authority", "delegation", "budgets", "state-memory", "documentation", "recovery", "lifecycle"}


def main() -> int:
    if len(sys.argv) != 2:
        print("FAIL usage: validate_agent_eval_plan.py PLAN.json", file=sys.stderr)
        return 2
    try:
        value = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    required = {"schema_version", "evaluation_id", "target", "environment", "authority", "layers", "acceptance", "holdout_policy", "artifacts"}
    errors = [f"missing {key}" for key in sorted(required - value.keys())]
    layers = value.get("layers", [])
    if not layers or any(layer not in ALLOWED for layer in layers):
        errors.append("layers must be a non-empty supported list")
    criteria = value.get("acceptance", {}).get("criteria", {})
    for layer in layers:
        if layer not in criteria:
            errors.append(f"acceptance missing {layer}")
    if value.get("holdout_policy", {}).get("protected") is not True:
        errors.append("holdout_policy.protected must be true")
    if errors:
        for error in errors:
            print(f"FAIL {error}", file=sys.stderr)
        return 1
    print(f"PASS agent evaluation plan: {value['evaluation_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
