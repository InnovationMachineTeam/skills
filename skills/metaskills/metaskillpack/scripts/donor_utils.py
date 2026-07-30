#!/usr/bin/env python3
"""Shared read-only donor discovery and hashing helpers."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


IGNORED_NAMES = {".DS_Store", "__pycache__"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def load_lock(skillpack: Path) -> dict:
    path = skillpack / "donors.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("donors"), list):
        raise ValueError(f"invalid donor lock: {path}")
    return value


def frontmatter_identity(skill_file: Path) -> tuple[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated YAML frontmatter")
    frontmatter = text[4:end]
    name_match = re.search(r"(?m)^name:\s*[\"']?([^\"'\n]+?)[\"']?\s*$", frontmatter)
    metadata_match = re.search(r"(?m)^metadata:\s*$", frontmatter)
    version_match = re.search(r"(?m)^\s{2}version:\s*[\"']?([^\"'\n]+?)[\"']?\s*$", frontmatter)
    if not name_match:
        raise ValueError("frontmatter name is required")
    if not metadata_match or not version_match:
        raise ValueError("frontmatter metadata.version is required")
    return name_match.group(1).strip(), version_match.group(1).strip()


def included_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in IGNORED_NAMES or part == ".git" for part in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"symlink is not allowed: {path}")
        if path.is_file() and path.suffix not in IGNORED_SUFFIXES:
            files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in included_files(root):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        content = path.read_bytes()
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def candidate_paths(skillpack: Path, donor: dict, roots: list[Path]) -> list[Path]:
    name = donor["name"]
    values: list[Path] = []
    source = donor.get("source")
    if isinstance(source, str) and source:
        values.append(skillpack / source)
    for root in roots:
        values.extend(
            [
                root / name,
                root / "metaskills" / name,
                root / "skills" / name,
                root / "skills" / "metaskills" / name,
                root / "plugins" / name / "skills" / name,
            ]
        )
        version_root = root / name
        if version_root.is_dir():
            for version_dir in sorted(version_root.iterdir()):
                if version_dir.is_dir() and re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version_dir.name):
                    values.append(version_dir / "skills" / name)
    seen: set[Path] = set()
    result: list[Path] = []
    for value in values:
        resolved = value.resolve()
        if resolved not in seen:
            seen.add(resolved)
            result.append(resolved)
    return result


def resolve_donor(skillpack: Path, donor: dict, roots: list[Path]) -> dict:
    expected_name = donor["name"]
    candidates = candidate_paths(skillpack, donor, roots)
    valid = []
    errors = []
    for path in candidates:
        skill_file = path / "SKILL.md"
        if not skill_file.is_file():
            continue
        try:
            name, version = frontmatter_identity(skill_file)
            if name != expected_name:
                raise ValueError(f"declares name {name!r}")
            digest = tree_digest(path)
            valid.append({"path": path, "version": version, "tree_sha256": digest})
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append({"path": str(path), "error": str(exc)})

    signatures = {(item["version"], item["tree_sha256"]) for item in valid}
    if len(signatures) > 1:
        return {
            "status": "invalid",
            "name": expected_name,
            "error": "ambiguous donor candidates with different versions or content",
            "candidates": [str(item["path"]) for item in valid],
            "searched": [str(path) for path in candidates],
        }
    if not valid:
        status = "invalid" if errors else "missing"
        return {
            "status": status,
            "name": expected_name,
            "error": errors or "no valid SKILL.md found",
            "searched": [str(path) for path in candidates],
        }

    selected = valid[0]
    locked_version = donor.get("version", "")
    locked_digest = donor.get("tree_sha256", "")
    status = "current" if selected["version"] == locked_version and selected["tree_sha256"] == locked_digest else "changed"
    return {
        "status": status,
        "name": expected_name,
        "path": str(selected["path"]),
        "locked_version": locked_version,
        "actual_version": selected["version"],
        "locked_tree_sha256": locked_digest,
        "actual_tree_sha256": selected["tree_sha256"],
        "searched": [str(path) for path in candidates],
    }
