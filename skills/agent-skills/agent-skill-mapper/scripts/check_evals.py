#!/usr/bin/env python3
"""Validate agent-skill-mapper eval fixtures."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROUTES = {"inventory", "recommend", "audit", "apply", "private-promotion"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("eval_dir", nargs="?", type=Path, default=Path("evals"))
    args = parser.parse_args()
    failures: list[str] = []
    for filename in ("routing.json", "behavior.json"):
        path = args.eval_dir / filename
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{path}: {exc}")
            continue
        cases = data.get("cases") if isinstance(data, dict) else None
        if not isinstance(cases, list) or not cases:
            failures.append(f"{path}: non-empty cases required")
            continue
        ids = [case.get("id") for case in cases if isinstance(case, dict)]
        if len(ids) != len(cases) or len(ids) != len(set(ids)):
            failures.append(f"{path}: unique case ids required")
        if filename == "routing.json":
            covered = {case.get("expected_route") for case in cases if isinstance(case, dict)}
            if ROUTES - covered:
                failures.append(f"{path}: missing routes {sorted(ROUTES - covered)}")
            triggers = {case.get("expected_trigger") for case in cases if isinstance(case, dict)}
            if not {True, False}.issubset(triggers):
                failures.append(f"{path}: positive and negative triggers required")
        else:
            for case in cases:
                if not isinstance(case, dict) or not case.get("expected_properties") or not isinstance(case.get("forbidden_properties"), list):
                    failures.append(f"{path}: behavior properties required")
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        return 1
    print("PASS agent-skill-mapper eval fixtures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
