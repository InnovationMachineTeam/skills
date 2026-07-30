#!/usr/bin/env python3
"""Create a deterministic read-only inventory of explicitly scoped skill roots."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKIP_DIRS = {".git", ".svn", "node_modules", "__pycache__", ".cache", "dist", "build"}
SKIP_FILES = {".DS_Store"}


def parse_frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "missing opening frontmatter delimiter"
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        return {}, "missing closing frontmatter delimiter"
    values: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return {}, f"unsupported frontmatter syntax on line {number}"
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value[:1] == value[-1:] and value[:1] in {'"', "'"}:
            value = value[1:-1]
        values[key] = value
    return values, None


def manifest_hash(skill_dir: Path) -> str:
    digest = hashlib.sha256()
    for current, dirnames, filenames in os.walk(skill_dir):
        dirnames[:] = sorted(name for name in dirnames if name not in SKIP_DIRS)
        current_path = Path(current)
        for filename in sorted(filenames):
            if filename in SKIP_FILES or filename.endswith((".pyc", ".pyo")):
                continue
            path = current_path / filename
            if path.is_symlink() or not path.is_file():
                continue
            relative = path.relative_to(skill_dir).as_posix().encode("utf-8")
            digest.update(relative)
            digest.update(b"\0")
            try:
                digest.update(path.read_bytes())
            except OSError as exc:
                digest.update(f"<unreadable:{exc}>".encode("utf-8"))
            digest.update(b"\0")
    return digest.hexdigest()


def display_name(skill_dir: Path) -> str | None:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r'^\s*display_name:\s*(["\'])(.*?)\1\s*$', text, re.MULTILINE)
    return match.group(2) if match else None


def discover(root: Path, max_depth: int) -> list[Path]:
    found: list[Path] = []
    if (root / "SKILL.md").is_file():
        found.append(root)
    for current, dirnames, filenames in os.walk(root):
        current_path = Path(current)
        depth = len(current_path.relative_to(root).parts)
        dirnames[:] = sorted(
            name
            for name in dirnames
            if name not in SKIP_DIRS and not name.startswith(".") and depth < max_depth
        )
        if current_path != root and "SKILL.md" in filenames:
            found.append(current_path)
            dirnames[:] = []
    return sorted(set(path.resolve() for path in found), key=str)


def inspect_skill(skill_dir: Path, root: Path, root_index: int) -> dict[str, object]:
    skill_file = skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8", errors="replace")
    metadata, error = parse_frontmatter(text)
    errors: list[str] = []
    if error:
        errors.append(error)
    if set(metadata) != {"name", "description"}:
        errors.append("frontmatter must contain exactly name and description")
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if not NAME_RE.fullmatch(name) or len(name) > 63:
        errors.append("invalid skill name")
    if name and skill_dir.name != name:
        errors.append("folder name does not match declared name")
    if not 20 <= len(description) <= 1024:
        errors.append("description length is outside 20-1024 characters")
    return {
        "identity_key": f"{name or '<invalid>'}@{skill_dir}",
        "name": name or None,
        "folder_name": skill_dir.name,
        "path": str(skill_dir),
        "root": str(root),
        "root_index": root_index,
        "description": description or None,
        "display_name": display_name(skill_dir),
        "manifest_sha256": manifest_hash(skill_dir),
        "structurally_valid": not errors,
        "errors": errors,
        "predicted_lifecycle": "UNKNOWN",
    }


def inventory(roots: list[Path], max_depth: int) -> dict[str, object]:
    root_records: list[dict[str, object]] = []
    entries: list[dict[str, object]] = []
    for index, requested in enumerate(roots):
        resolved = requested.expanduser().resolve()
        error: str | None = None
        if resolved == Path("/") or resolved == Path.home().resolve():
            error = "broad root is refused; provide a narrower skill directory"
        elif not resolved.is_dir():
            error = "root is not a directory"
        root_records.append(
            {
                "requested": str(requested),
                "resolved": str(resolved),
                "precedence_index": index,
                "error": error,
            }
        )
        if error:
            continue
        for skill_dir in discover(resolved, max_depth):
            entries.append(inspect_skill(skill_dir, resolved, index))

    entries.sort(key=lambda item: (int(item["root_index"]), str(item["path"])))
    by_name: dict[str, list[dict[str, object]]] = {}
    for entry in entries:
        name = entry.get("name")
        if isinstance(name, str):
            by_name.setdefault(name, []).append(entry)

    duplicate_names: list[dict[str, object]] = []
    for name, group in sorted(by_name.items()):
        valid_group = [item for item in group if item["structurally_valid"]]
        for position, entry in enumerate(valid_group):
            entry["predicted_lifecycle"] = (
                "PREDICTED_AVAILABLE" if len(valid_group) == 1 else "PREDICTED_ACTIVE" if position == 0 else "PREDICTED_SHADOWED"
            )
        if len(group) > 1:
            hashes = {str(item["manifest_sha256"]) for item in group}
            duplicate_names.append(
                {
                    "name": name,
                    "paths": [str(item["path"]) for item in group],
                    "content_relation": "identical" if len(hashes) == 1 else "divergent",
                    "note": "Lifecycle labels are predicted from declared root order and require host verification.",
                }
            )
    for entry in entries:
        if not entry["structurally_valid"]:
            entry["predicted_lifecycle"] = "INVALID"

    snapshot_seed = json.dumps(
        {
            "roots": root_records,
            "entries": [
                {
                    "identity_key": item["identity_key"],
                    "manifest_sha256": item["manifest_sha256"],
                    "predicted_lifecycle": item["predicted_lifecycle"],
                }
                for item in entries
            ],
        },
        sort_keys=True,
        ensure_ascii=False,
    ).encode("utf-8")
    return {
        "schema_version": "1.0",
        "snapshot_sha256": hashlib.sha256(snapshot_seed).hexdigest(),
        "max_depth": max_depth,
        "roots": root_records,
        "skills": entries,
        "duplicate_names": duplicate_names,
        "summary": {
            "roots": len(root_records),
            "root_errors": sum(record["error"] is not None for record in root_records),
            "skills": len(entries),
            "structurally_invalid": sum(not item["structurally_valid"] for item in entries),
            "duplicate_names": len(duplicate_names),
        },
        "scope_note": "Predicted lifecycle is not proof of actual host installation, enablement, or precedence.",
    }


def render_text(payload: dict[str, object]) -> str:
    summary = payload["summary"]
    assert isinstance(summary, dict)
    lines = [
        f"Snapshot: {payload['snapshot_sha256']}",
        f"Roots: {summary['roots']} ({summary['root_errors']} errors)",
        f"Skills: {summary['skills']} ({summary['structurally_invalid']} invalid)",
        f"Duplicate names: {summary['duplicate_names']}",
    ]
    skills = payload["skills"]
    assert isinstance(skills, list)
    for item in skills:
        assert isinstance(item, dict)
        lines.append(
            f"- {item.get('name') or '<invalid>'}: {item['predicted_lifecycle']} — {item['path']}"
        )
        for error in item["errors"]:
            lines.append(f"  error: {error}")
    duplicates = payload["duplicate_names"]
    assert isinstance(duplicates, list)
    for duplicate in duplicates:
        assert isinstance(duplicate, dict)
        lines.append(
            f"Conflict: {duplicate['name']} ({duplicate['content_relation']})"
        )
    lines.append(str(payload["scope_note"]))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="+", type=Path)
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fail-on-invalid", action="store_true")
    args = parser.parse_args()
    if not 0 <= args.max_depth <= 8:
        print("Error: --max-depth must be between 0 and 8", file=sys.stderr)
        return 2
    payload = inventory(args.roots, args.max_depth)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_text(payload)
    if args.output:
        output = args.output.expanduser().resolve()
        if not output.parent.is_dir():
            print(f"Error: output directory does not exist: {output.parent}", file=sys.stderr)
            return 2
        output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Inventory written to {output}", file=sys.stderr)
    else:
        print(rendered)
    summary = payload["summary"]
    assert isinstance(summary, dict)
    return 1 if args.fail_on_invalid and (summary["root_errors"] or summary["structurally_invalid"]) else 0


if __name__ == "__main__":
    sys.exit(main())

