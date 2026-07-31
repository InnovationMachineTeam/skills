#!/usr/bin/env python3
"""Verify frozen agentkit upgrade, rollback, and external holdout contracts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def safe(value: object) -> bool:
    return isinstance(value, str) and bool(value) and not PurePosixPath(value).is_absolute() and ".." not in PurePosixPath(value).parts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack-root", type=Path, required=True)
    parser.add_argument("--repository-root", type=Path, required=True)
    args = parser.parse_args()
    pack = args.pack_root.resolve()
    repository = args.repository_root.resolve()
    contracts = json.loads((pack / "contracts.json").read_text(encoding="utf-8"))
    failures = []
    for key in ("upgrade", "rollback"):
        entry = contracts.get(key, {})
        locator = entry.get("locator")
        if not safe(locator) or not (pack / str(locator)).is_file():
            failures.append(f"{key}: missing or unsafe locator")
        elif digest(pack / str(locator)) != entry.get("sha256"):
            failures.append(f"{key}: hash drift")
    holdout = contracts.get("holdout", {})
    locator = holdout.get("locator")
    if not safe(locator) or not (repository / str(locator)).is_file():
        failures.append("holdout: missing or unsafe locator")
    elif digest(repository / str(locator)) != holdout.get("sha256"):
        failures.append("holdout: hash drift")
    if holdout.get("external_to_bundle") is not True or (pack / str(locator)).exists():
        failures.append("holdout must remain outside the distributed pack")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    print("PASS frozen agentkit upgrade, rollback, and holdout contracts")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        raise SystemExit(1)
