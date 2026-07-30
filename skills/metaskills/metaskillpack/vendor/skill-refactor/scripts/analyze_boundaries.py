#!/usr/bin/env python3
"""Create a deterministic read-only structural report for exact skill directories."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path


SKIP_DIRS = {".git", "__pycache__", "node_modules", ".cache", "dist", "build"}
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def metadata(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        return {}
    result: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip("\"'")
    return result


def kind(relative: Path) -> str:
    parts = set(relative.parts[:-1])
    if relative.as_posix() == "SKILL.md":
        return "skill-definition"
    if "prompts" in parts:
        return "prompt"
    if "references" in parts:
        return "reference"
    if "scripts" in parts:
        return "script"
    if "evals" in parts:
        return "eval"
    if "agents" in parts:
        return "agent-metadata"
    return "other"


def inspect(root: Path) -> dict[str, object]:
    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        return {"path": str(root), "error": "SKILL.md not found"}
    text = skill_file.read_text(encoding="utf-8", errors="replace")
    meta = metadata(text)
    files: list[dict[str, object]] = []
    broken_links: list[dict[str, str]] = []
    for current, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = sorted(name for name in dirnames if name not in SKIP_DIRS and not name.startswith("."))
        current_path = Path(current)
        for filename in sorted(filenames):
            if filename.endswith((".pyc", ".pyo")) or filename == ".DS_Store":
                continue
            path = current_path / filename
            relative = path.relative_to(root)
            if path.is_symlink() or not path.is_file():
                files.append({"path": relative.as_posix(), "kind": "symlink", "size_bytes": None, "sha256": None})
                continue
            files.append({"path": relative.as_posix(), "kind": kind(relative), "size_bytes": path.stat().st_size, "sha256": sha256(path)})
            if path.suffix.lower() in {".md", ".mdx"}:
                body = path.read_text(encoding="utf-8", errors="replace")
                for raw in LINK_RE.findall(body):
                    target = raw.strip().strip("<>").split("#", 1)[0]
                    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                        continue
                    resolved = (path.parent / target).resolve()
                    if not resolved.exists():
                        broken_links.append({"file": relative.as_posix(), "target": raw})
    files.sort(key=lambda item: str(item["path"]))
    by_kind: dict[str, int] = {}
    for item in files:
        by_kind[str(item["kind"])] = by_kind.get(str(item["kind"]), 0) + 1
    seed = json.dumps([{"path": item["path"], "sha256": item["sha256"]} for item in files], sort_keys=True).encode("utf-8")
    return {
        "path": str(root),
        "error": None,
        "name": meta.get("name"),
        "description": meta.get("description"),
        "manifest_sha256": hashlib.sha256(seed).hexdigest(),
        "skill_lines": len(text.splitlines()),
        "headings": [{"level": len(mark), "title": title} for mark, title in HEADING_RE.findall(text)],
        "files": files,
        "files_by_kind": dict(sorted(by_kind.items())),
        "broken_links": broken_links,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    reports = [inspect(path.expanduser().resolve()) for path in args.skills]
    payload = {"schema_version": "1.0", "skills": reports, "summary": {"skills": len(reports), "errors": sum(item["error"] is not None for item in reports), "broken_links": sum(len(item.get("broken_links", [])) for item in reports)}}
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        output = args.output.expanduser().resolve()
        if not output.parent.is_dir():
            print(f"Error: output directory does not exist: {output.parent}", file=sys.stderr)
            return 2
        output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Boundary report written to {output}")
    else:
        print(rendered)
    return 1 if payload["summary"]["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
