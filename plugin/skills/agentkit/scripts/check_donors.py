#!/usr/bin/env python3
"""Compare agentkit lock entries with vendored and optional canonical donors."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


VERSION = re.compile(r'^\s*version:\s*["\']([^"\']+)["\']\s*$', re.MULTILINE)


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(
        item for item in root.rglob("*")
        if item.is_file()
        and "__pycache__" not in item.parts
        and item.suffix not in {".pyc", ".pyo"}
        and item.name != ".DS_Store"
    ):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def version(path: Path) -> str | None:
    if not path.is_file():
        return None
    match = VERSION.search(path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--vendor-root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    vendor_root = args.vendor_root.resolve()
    source_root = args.source_root.resolve() if args.source_root else None
    results = []
    for entry in manifest.get("donors", []):
        name = entry.get("name")
        vendor = vendor_root / str(name)
        status = "current"
        reasons = []
        if version(vendor / "DONOR.md") != entry.get("version"):
            status = "changed"
            reasons.append("vendored version differs")
        if not (vendor / "DONOR.md").is_file():
            status = "missing"
            reasons.append("vendored entrypoint missing")
        elif tree_hash(vendor) != entry.get("vendor_tree_sha256"):
            status = "changed"
            reasons.append("vendored tree hash differs")
        if (vendor / "SKILL.md").exists():
            status = "changed"
            reasons.append("nested discoverable SKILL.md exists")
        if source_root:
            source = source_root / str(name)
            if not (source / "SKILL.md").is_file():
                status = "missing"
                reasons.append("canonical donor missing")
            else:
                if version(source / "SKILL.md") != entry.get("version"):
                    status = "changed"
                    reasons.append("canonical version differs")
                if tree_hash(source) != entry.get("source_tree_sha256"):
                    status = "changed"
                    reasons.append("canonical tree hash differs")
        results.append({"name": name, "status": status, "reasons": reasons})

    payload = {"pack": manifest.get("pack"), "pack_version": manifest.get("pack_version"), "donors": results}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if results and all(item["status"] == "current" for item in results) else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        raise SystemExit(1)
