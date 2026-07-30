#!/usr/bin/env python3
"""Print a compact, deterministic summary of skill-builder state."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    path = args.state.expanduser().resolve()
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"Cannot read state: {exc}", file=sys.stderr)
        return 1
    if not isinstance(value, dict) or not isinstance(value.get("phases"), list):
        print("State must be an object with a phases array.", file=sys.stderr)
        return 1

    phases = [phase for phase in value["phases"] if isinstance(phase, dict)]
    counts = Counter(str(phase.get("status", "unknown")) for phase in phases)
    first_incomplete = next(
        (
            {
                "id": phase.get("id"),
                "specialist": phase.get("specialist"),
                "status": phase.get("status"),
                "objective": phase.get("objective"),
            }
            for phase in phases
            if phase.get("status") not in {"completed", "skipped"}
        ),
        None,
    )
    summary = {
        "build_id": value.get("build_id"),
        "scenario": value.get("scenario"),
        "status": value.get("status"),
        "goal": value.get("goal"),
        "phase_count": len(phases),
        "phase_statuses": dict(sorted(counts.items())),
        "first_incomplete": first_incomplete,
        "updated_at": value.get("updated_at"),
    }

    if args.format == "json":
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"Build: {summary['build_id']}")
        print(f"Scenario: {summary['scenario']}")
        print(f"Status: {summary['status']}")
        print(f"Goal: {summary['goal']}")
        print("Phases: " + ", ".join(f"{key}={count}" for key, count in summary["phase_statuses"].items()))
        if first_incomplete:
            print(
                "Next: "
                f"{first_incomplete['id']} ({first_incomplete['specialist']}, {first_incomplete['status']}) — "
                f"{first_incomplete['objective']}"
            )
        else:
            print("Next: none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
