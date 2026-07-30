#!/usr/bin/env python3
"""Compare two source snapshot manifests and classify material signals."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
RETRIEVAL_STATUSES = {"available", "unavailable", "partial", "moved"}


def valid_time(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def load(path: Path) -> dict[str, dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if (
        not isinstance(value, dict)
        or value.get("schema_version") != 1
        or not isinstance(value.get("sources"), list)
        or not HASH_PATTERN.fullmatch(value.get("registry_hash", ""))
        or not valid_time(value.get("created_at"))
    ):
        raise ValueError(f"invalid snapshot root: {path}")
    result: dict[str, dict[str, Any]] = {}
    for item in value["sources"]:
        if not isinstance(item, dict) or not isinstance(item.get("source_id"), str) or not item["source_id"]:
            raise ValueError(f"invalid source record: {path}")
        status = item.get("status")
        if status not in RETRIEVAL_STATUSES:
            raise ValueError(f"invalid retrieval status for {item['source_id']}: {status}")
        if not valid_time(item.get("checked_at")) or not isinstance(item.get("canonical_locator"), str) or not item["canonical_locator"]:
            raise ValueError(f"missing checked_at or canonical_locator for {item['source_id']}")
        if not isinstance(item.get("claims"), list) or not isinstance(item.get("errors"), list) or not isinstance(item.get("coverage_notes"), str):
            raise ValueError(f"missing claims, errors, or coverage_notes for {item['source_id']}")
        fingerprint = item.get("semantic_fingerprint")
        if status in {"available", "moved"} and not HASH_PATTERN.fullmatch(fingerprint or ""):
            raise ValueError(f"available source needs semantic_fingerprint for {item['source_id']}")
        if fingerprint is not None and not HASH_PATTERN.fullmatch(fingerprint):
            raise ValueError(f"invalid semantic_fingerprint for {item['source_id']}")
        if item["source_id"] in result:
            raise ValueError(f"duplicate source_id {item['source_id']}: {path}")
        result[item["source_id"]] = item
    return result


def compare(before: dict[str, dict[str, Any]], after: dict[str, dict[str, Any]]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for source_id in sorted(set(before) | set(after)):
        old = before.get(source_id)
        new = after.get(source_id)
        if new is not None and new.get("status") in {"unavailable", "partial"}:
            records.append({
                "source_id": source_id,
                "change": new.get("status"),
                "registry_change": "added" if old is None else "none",
                "semantic_change": None,
                "semantic_status": "unknown",
            })
            continue
        if old is None:
            records.append({"source_id": source_id, "change": "added", "registry_change": "added", "semantic_change": True, "semantic_status": "changed"})
            continue
        if new is None:
            records.append({"source_id": source_id, "change": "removed", "registry_change": "removed", "semantic_change": True, "semantic_status": "changed"})
            continue
        semantic_changed = old.get("semantic_fingerprint") != new.get("semantic_fingerprint")
        transport_changed = any(
            old.get(key) != new.get(key)
            for key in ("revision", "etag", "last_modified", "content_hash", "resolved_locator")
        )
        if semantic_changed:
            change = "semantic"
        elif transport_changed:
            change = "transport-only"
        else:
            change = "unchanged"
        records.append({"source_id": source_id, "change": change, "registry_change": "none", "semantic_change": semantic_changed, "semantic_status": "changed" if semantic_changed else "unchanged"})
    counts: dict[str, int] = {}
    for record in records:
        counts[record["change"]] = counts.get(record["change"], 0) + 1
    return {"counts": dict(sorted(counts.items())), "sources": records}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = compare(load(args.before.expanduser().resolve()), load(args.after.expanduser().resolve()))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"Snapshot comparison failed: {exc}", file=sys.stderr)
        return 1
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.expanduser().resolve().write_text(rendered + "\n", encoding="utf-8")
    if args.format == "json":
        print(rendered)
    else:
        print("Source changes: " + ", ".join(f"{key}={value}" for key, value in result["counts"].items()))
        for record in result["sources"]:
            print(f"{record['source_id']}: {record['change']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
