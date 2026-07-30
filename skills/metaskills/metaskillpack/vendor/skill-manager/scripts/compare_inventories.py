#!/usr/bin/env python3
"""Compare two JSON snapshots emitted by inventory_skills.py."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load(path: Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict) or not isinstance(value.get("skills"), list):
        raise ValueError(f"invalid inventory: {path}")
    return value


def indexed(value: dict[str, object]) -> dict[str, dict[str, object]]:
    skills = value["skills"]
    assert isinstance(skills, list)
    result: dict[str, dict[str, object]] = {}
    for item in skills:
        if isinstance(item, dict) and isinstance(item.get("identity_key"), str):
            result[str(item["identity_key"])] = item
    return result


def roots(value: dict[str, object]) -> list[str]:
    raw = value.get("roots")
    if not isinstance(raw, list):
        return []
    return [str(item.get("resolved")) for item in raw if isinstance(item, dict)]


def compare(before: dict[str, object], after: dict[str, object]) -> dict[str, object]:
    old = indexed(before)
    new = indexed(after)
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    shared = sorted(set(old) & set(new))
    changed = [
        key
        for key in shared
        if old[key].get("manifest_sha256") != new[key].get("manifest_sha256")
    ]
    lifecycle_changed = [
        key
        for key in shared
        if old[key].get("predicted_lifecycle") != new[key].get("predicted_lifecycle")
    ]
    before_roots = roots(before)
    after_roots = roots(after)
    return {
        "before_snapshot": before.get("snapshot_sha256"),
        "after_snapshot": after.get("snapshot_sha256"),
        "comparable_roots": before_roots == after_roots,
        "before_roots": before_roots,
        "after_roots": after_roots,
        "added": added,
        "removed": removed,
        "content_changed": changed,
        "predicted_lifecycle_changed": lifecycle_changed,
        "before_duplicate_names": before.get("duplicate_names", []),
        "after_duplicate_names": after.get("duplicate_names", []),
        "verification_note": "Inventory deltas do not prove actual client installation, enablement, routing, or successful rollback.",
    }


def render_text(value: dict[str, object]) -> str:
    lines = [
        f"Comparable roots: {value['comparable_roots']}",
        f"Added: {len(value['added'])}",
        f"Removed: {len(value['removed'])}",
        f"Content changed: {len(value['content_changed'])}",
        f"Predicted lifecycle changed: {len(value['predicted_lifecycle_changed'])}",
    ]
    for key in ("added", "removed", "content_changed", "predicted_lifecycle_changed"):
        values = value[key]
        assert isinstance(values, list)
        for item in values:
            lines.append(f"  {key}: {item}")
    lines.append(str(value["verification_note"]))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    try:
        value = compare(load(args.before), load(args.after))
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(value, ensure_ascii=False, indent=2) if args.format == "json" else render_text(value))
    return 0


if __name__ == "__main__":
    sys.exit(main())
