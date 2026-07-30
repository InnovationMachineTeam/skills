#!/usr/bin/env python3
"""Compare read-only source donors with the metaskillpack donor lock."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from donor_utils import load_lock, resolve_donor


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skillpack", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--donor-root", action="append", type=Path, default=[])
    parser.add_argument("--json", action="store_true", help="Emit a JSON report")
    args = parser.parse_args()

    skillpack = args.skillpack.resolve()
    roots = [path.resolve() for path in args.donor_root]
    try:
        lock = load_lock(skillpack)
        results = [resolve_donor(skillpack, donor, roots) for donor in lock["donors"]]
    except (OSError, UnicodeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 3

    counts = {status: sum(item["status"] == status for item in results) for status in ("current", "changed", "missing", "invalid")}
    report = {
        "pack": lock.get("pack"),
        "pack_version": lock.get("pack_version"),
        "summary": counts,
        "donors": results,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for item in results:
            locked = item.get("locked_version", "-") or "-"
            actual = item.get("actual_version", "-") or "-"
            print(f"{item['status'].upper():7} {item['name']}: locked={locked} actual={actual}")
        print("SUMMARY " + " ".join(f"{key}={value}" for key, value in counts.items()))

    if counts["missing"] or counts["invalid"]:
        return 3
    if counts["changed"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
