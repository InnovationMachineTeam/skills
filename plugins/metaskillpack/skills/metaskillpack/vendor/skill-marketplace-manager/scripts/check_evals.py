#!/usr/bin/env python3
"""Validate the shape and identifiers of marketplace-manager eval files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evals", type=Path)
    args = parser.parse_args()
    failures: list[str] = []
    seen: set[str] = set()
    count = 0
    for path in sorted(args.evals.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{path}: {exc}")
            continue
        cases = data.get("cases") if isinstance(data, dict) else None
        if not isinstance(cases, list) or not cases:
            failures.append(f"{path}: non-empty cases[] required")
            continue
        for index, case in enumerate(cases):
            count += 1
            if not isinstance(case, dict):
                failures.append(f"{path}[{index}]: object required")
                continue
            identifier = case.get("id")
            if not isinstance(identifier, str) or not identifier:
                failures.append(f"{path}[{index}]: id required")
            elif identifier in seen:
                failures.append(f"{path}[{index}]: duplicate id {identifier}")
            else:
                seen.add(identifier)
            if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
                failures.append(f"{path}[{index}]: prompt required")
            if not isinstance(case.get("expect"), dict) or not case["expect"]:
                failures.append(f"{path}[{index}]: non-empty expect object required")
    if count == 0:
        failures.append("no eval cases found")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print(f"PASS {count} eval cases across {len(list(args.evals.glob('*.json')))} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
