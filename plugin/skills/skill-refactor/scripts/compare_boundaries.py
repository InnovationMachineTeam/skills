#!/usr/bin/env python3
"""Compare two reports emitted by analyze_boundaries.py."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("skills"), list):
        raise ValueError(f"invalid boundary report: {path}")
    return value


def index(value: dict[str, object]) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for item in value["skills"]:
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            result[str(item["path"])] = item
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    try:
        before = index(load(args.before))
        after = index(load(args.after))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    shared = sorted(set(before) & set(after))
    payload = {
        "added_skills": sorted(set(after) - set(before)),
        "removed_skills": sorted(set(before) - set(after)),
        "changed_skills": [path for path in shared if before[path].get("manifest_sha256") != after[path].get("manifest_sha256")],
        "unchanged_skills": [path for path in shared if before[path].get("manifest_sha256") == after[path].get("manifest_sha256")],
        "before_broken_links": sum(len(item.get("broken_links", [])) for item in before.values()),
        "after_broken_links": sum(len(item.get("broken_links", [])) for item in after.values()),
        "note": "Structural deltas do not prove behavioral, routing, consumer, host, or rollback correctness."
    }
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for key in ("added_skills", "removed_skills", "changed_skills", "unchanged_skills"):
            print(f"{key}: {len(payload[key])}")
        print(f"broken_links: {payload['before_broken_links']} -> {payload['after_broken_links']}")
        print(payload["note"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
