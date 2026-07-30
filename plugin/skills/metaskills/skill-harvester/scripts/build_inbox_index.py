#!/usr/bin/env python3
"""Build a deterministic index of an explicit skill-harvester inbox."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path


SENSITIVE_NAMES = {".env", "id_rsa", "id_ed25519", "credentials", "credentials.json", "secrets.json"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inbox", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    inbox = args.inbox.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if inbox.is_symlink() or not inbox.is_dir() or inbox in {Path("/"), Path.home().resolve()}:
        print("Error: inbox must be an explicit non-symlink directory", file=sys.stderr)
        return 2
    files: list[dict[str, object]] = []
    for current, dirnames, filenames in os.walk(inbox, followlinks=False):
        dirnames[:] = sorted(name for name in dirnames if name not in {".git", "__pycache__"})
        current_path = Path(current)
        for filename in sorted(filenames):
            path = current_path / filename
            if path.resolve() == output or path.is_symlink() or not path.is_file():
                continue
            relative = path.relative_to(inbox)
            files.append({
                "path": relative.as_posix(),
                "section": relative.parts[0] if len(relative.parts) > 1 else "root",
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
                "sensitive_name": filename.lower() in SENSITIVE_NAMES or path.suffix.lower() in {".pem", ".key", ".p12", ".pfx"},
            })
    files.sort(key=lambda item: str(item["path"]))
    by_section: dict[str, int] = {}
    for item in files:
        by_section[str(item["section"])] = by_section.get(str(item["section"]), 0) + 1
    payload = {
        "schema_version": "1.0",
        "inbox": str(inbox),
        "files": files,
        "summary": {
            "files": len(files),
            "bytes": sum(int(item["size_bytes"]) for item in files),
            "sensitive_name_findings": sum(bool(item["sensitive_name"]) for item in files),
            "by_section": dict(sorted(by_section.items())),
        },
        "scope_note": "Indexing does not establish source completeness, rights, safety, or semantic quality.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Inbox index written to {output}")
    return 1 if payload["summary"]["sensitive_name_findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
