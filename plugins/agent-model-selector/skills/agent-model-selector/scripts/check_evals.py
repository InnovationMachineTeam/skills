#!/usr/bin/env python3
"""Validate agent-model-selector routing and behavior fixtures."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROUTES = {"recommend", "benchmark-plan", "benchmark-run", "audit", "migration"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("eval_dir", type=Path, nargs="?", default=Path("evals"))
    args = parser.parse_args()
    failures: list[str] = []
    for name in ("routing.json", "behavior.json"):
        path = args.eval_dir / name
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{path}: {exc}")
            continue
        cases = data.get("cases") if isinstance(data, dict) else None
        if not isinstance(cases, list) or not cases:
            failures.append(f"{path}: cases must be non-empty")
            continue
        ids = [item.get("id") for item in cases if isinstance(item, dict)]
        if len(ids) != len(cases) or len(ids) != len(set(ids)):
            failures.append(f"{path}: case ids must be unique")
        for item in cases:
            if not isinstance(item, dict) or not isinstance(item.get("input"), str):
                failures.append(f"{path}: every case requires input")
            if name == "behavior.json" and (
                not isinstance(item.get("expected_properties"), list)
                or not isinstance(item.get("forbidden_properties"), list)
            ):
                failures.append(f"{path}: behavior cases require expected/forbidden properties")
        if name == "routing.json":
            covered = {item.get("expected_route") for item in cases if isinstance(item, dict)}
            if ROUTES - covered:
                failures.append(f"{path}: missing routes {sorted(ROUTES - covered)}")
            if not {True, False}.issubset({item.get("expected_trigger") for item in cases if isinstance(item, dict)}):
                failures.append(f"{path}: positive and negative triggers are required")
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        return 1
    print("PASS agent-model-selector eval fixtures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
