#!/usr/bin/env python3
"""Build a self-contained aggregate Claude Code plugin into a new directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path


SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
PLUGIN_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Marketplace root containing canonical skills/")
    parser.add_argument("output", type=Path, help="New output directory; must not exist")
    parser.add_argument("--plugin-name", required=True)
    parser.add_argument("--display-name")
    parser.add_argument("--version", required=True)
    parser.add_argument("--description", default="Portable Agent Skills bundle")
    parser.add_argument("--author-name")
    parser.add_argument("--author-email")
    args = parser.parse_args()

    root = args.root.resolve()
    output = args.output.resolve()
    skills = root / "skills"
    if not skills.is_dir():
        parser.error(f"missing canonical skills directory: {skills}")
    if output.exists():
        parser.error(f"output already exists; use a new staging directory: {output}")
    if output == root or output == skills or skills in output.parents:
        parser.error("output must not replace or be nested inside the canonical skills tree")
    if not PLUGIN_NAME.fullmatch(args.plugin_name):
        parser.error("plugin name must be lowercase kebab-case")
    if not SEMVER.fullmatch(args.version):
        parser.error("version must be SemVer")
    symlinks = [path for path in skills.rglob("*") if path.is_symlink()]
    if symlinks:
        parser.error(f"source contains symlinks; first: {symlinks[0]}")

    skill_files = sorted(skills.rglob("SKILL.md"))
    if not skill_files:
        parser.error("no skills found")
    relative_parts = [path.relative_to(skills).parts for path in skill_files]
    if any(len(parts) not in (2, 3) for parts in relative_parts):
        parser.error("only flat or one-category skill layouts are supported")

    output.mkdir(parents=True)
    excluded_patterns = [".DS_Store", "__pycache__", "*.pyc", ".git"]
    shutil.copytree(skills, output / "skills", ignore=shutil.ignore_patterns(*excluded_patterns))
    manifest_dir = output / ".claude-plugin"
    manifest_dir.mkdir()

    direct_skills = any(len(parts) == 2 for parts in relative_parts)
    categories = sorted({parts[0] for parts in relative_parts if len(parts) == 3})
    skill_paths = (["./skills"] if direct_skills else []) + [f"./skills/{category}" for category in categories]
    manifest = {
        "name": args.plugin_name,
        "displayName": args.display_name or args.plugin_name.replace("-", " ").title(),
        "version": args.version,
        "description": args.description,
        "skills": skill_paths,
    }
    if args.author_name:
        manifest["author"] = {"name": args.author_name}
        if args.author_email:
            manifest["author"]["email"] = args.author_email
    (manifest_dir / "plugin.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    files = []
    for path in sorted(p for p in output.rglob("*") if p.is_file()):
        files.append({"path": path.relative_to(output).as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size})
    build_manifest = {
        "format": 1,
        "plugin": args.plugin_name,
        "version": args.version,
        "source_layout": "skills/",
        "skills": len(skill_files),
        "excluded_patterns": excluded_patterns,
        "files": files,
    }
    (output / "build-manifest.json").write_text(json.dumps(build_manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Built {args.plugin_name}@{args.version} with {len(skill_files)} skills at {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
