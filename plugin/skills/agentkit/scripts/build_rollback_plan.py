#!/usr/bin/env python3
"""Build a read-only agentkit rollback plan with a direct-donor fallback."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--reason", required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() or not output.parent.is_dir() or output.parent.is_symlink():
        raise ValueError("output must be a new file in an existing real directory")
    manifest_path = args.manifest.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    donors = manifest.get("donors", [])
    if not donors:
        raise ValueError("manifest donors are required")
    routes = []
    for donor in donors:
        for mode in donor.get("modes", []):
            routes.append({"command": mode, "fallback": f"direct invocation of {donor['name']}@{donor['version']}", "hash": donor["source_tree_sha256"]})
    payload = {
        "schema_version": 1,
        "pack": manifest.get("pack"),
        "from_version": manifest.get("pack_version"),
        "fallback_mode": "direct-donor-dispatch",
        "reason": args.reason,
        "manifest_sha256": "sha256:" + hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "mutates_host": False,
        "requires_lifecycle_authority_to_apply": True,
        "routes": sorted(routes, key=lambda item: item["command"]),
        "verification": ["donor lock current", "direct donor resolves", "authority unchanged", "failing case rerun"],
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pack": payload["pack"], "from_version": payload["from_version"], "routes": len(routes), "mutates_host": False}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        raise SystemExit(1)
