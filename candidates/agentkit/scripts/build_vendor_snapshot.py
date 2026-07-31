#!/usr/bin/env python3
"""Build a read-only agentkit donor snapshot without modifying source donors."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path


DONORS = (
    "agent-architect", "agent-best-practices", "agent-builder", "agent-context",
    "agent-doctor", "agent-evaluator", "agent-manager", "agent-optimizer",
    "agent-refactor", "agent-scout",
)
MODES = {
    "agent-architect": ["architect"],
    "agent-best-practices": ["practices"],
    "agent-builder": ["run"],
    "agent-context": ["context"],
    "agent-doctor": ["doctor"],
    "agent-evaluator": ["evaluate"],
    "agent-manager": ["manage"],
    "agent-optimizer": ["optimize"],
    "agent-refactor": ["refactor"],
    "agent-scout": ["scout"],
}
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


def safe_target(path: Path) -> Path:
    resolved = path.resolve()
    if resolved == Path(resolved.anchor) or resolved == Path.home().resolve():
        raise ValueError(f"refusing broad target: {resolved}")
    if resolved.exists():
        raise ValueError(f"target already exists: {resolved}")
    if not resolved.parent.is_dir() or resolved.parent.is_symlink():
        raise ValueError(f"target parent must be an existing real directory: {resolved.parent}")
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--source-revision", required=True)
    args = parser.parse_args()

    source_root = args.source_root.resolve()
    output = safe_target(args.output)
    manifest = safe_target(args.manifest)
    if output.parent != manifest.parent:
        raise ValueError("vendor output and manifest must share the pack root")
    if output == source_root or output in source_root.parents or source_root in output.parents:
        raise ValueError("vendor output must be separate from canonical donors")

    entries = []
    output.mkdir()
    try:
        for name in DONORS:
            source = source_root / name
            skill_file = source / "SKILL.md"
            if not skill_file.is_file():
                raise ValueError(f"missing donor: {name}")
            symlinks = [path for path in source.rglob("*") if path.is_symlink()]
            if symlinks:
                raise ValueError(f"donor contains symlink: {symlinks[0]}")
            text = skill_file.read_text(encoding="utf-8")
            match = VERSION.search(text)
            if not match:
                raise ValueError(f"missing donor metadata.version: {name}")
            destination = output / name
            shutil.copytree(
                source,
                destination,
                ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc", "*.pyo", ".git"),
            )
            (destination / "SKILL.md").rename(destination / "DONOR.md")
            entries.append({
                "name": name,
                "version": match.group(1),
                "source_revision": args.source_revision,
                "source_tree_sha256": tree_hash(source),
                "vendor_tree_sha256": tree_hash(destination),
                "vendored_path": f"vendor/{name}",
                "entrypoint": f"vendor/{name}/DONOR.md",
                "modes": MODES[name],
                "interface_version": 1,
                "transforms": ["SKILL.md renamed to DONOR.md to prevent nested discovery"],
            })
        payload = {
            "schema_version": 1,
            "pack": "agentkit",
            "pack_version": "0.1.0",
            "source_repository": "InnovationMachineTeam/skills",
            "source_revision": args.source_revision,
            "donors": entries,
        }
        manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception:
        shutil.rmtree(output, ignore_errors=True)
        if manifest.exists():
            manifest.unlink()
        raise
    print(json.dumps({"donors": len(entries), "manifest": str(manifest), "vendor": str(output)}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        raise SystemExit(1)
