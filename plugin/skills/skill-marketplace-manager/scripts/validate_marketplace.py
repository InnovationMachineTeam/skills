#!/usr/bin/env python3
"""Portable structural validator for Agent Skills marketplace repositories."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote


SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


@dataclass
class Finding:
    level: str
    code: str
    path: str
    message: str


def add(findings: list[Finding], level: str, code: str, path: Path, message: str) -> None:
    findings.append(Finding(level, code, path.as_posix(), message))


def frontmatter(text: str) -> tuple[str | None, str | None, str | None, str | None]:
    if not text.startswith("---\n"):
        return None, None, None, "missing YAML frontmatter"
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, None, None, "unclosed YAML frontmatter"
    block = text[4:end]
    name = None
    description = None
    version = None
    in_metadata = False
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if indent == 0:
            in_metadata = line == "metadata:"
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip().strip("\"'")
            elif line.startswith("description:"):
                description = line.split(":", 1)[1].strip().strip("\"'")
        elif in_metadata and line.startswith("version:"):
            version = line.split(":", 1)[1].strip().strip("\"'")
    return name, description, version, None


def local_links(path: Path, root: Path, findings: list[Finding]) -> None:
    text = path.read_text(encoding="utf-8")
    for match in LINK.finditer(text):
        target = match.group(1).strip().split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        pure = PurePosixPath(target)
        if pure.is_absolute() or ".." in pure.parts:
            add(findings, "FAIL", "unsafe-local-link", path.relative_to(root), f"link escapes package: {target}")
            continue
        resolved = path.parent / unquote(target)
        if not resolved.exists():
            add(findings, "FAIL", "broken-local-link", path.relative_to(root), f"target does not exist: {target}")


def resolve_local(root: Path, value: Any) -> list[Path]:
    values = value if isinstance(value, list) else [value]
    result: list[Path] = []
    for item in values:
        if isinstance(item, str) and item.startswith("./"):
            result.append(root / item[2:])
    return result


def validate_json_manifest(path: Path, root: Path, findings: list[Finding]) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        add(findings, "FAIL", "invalid-json", path.relative_to(root), str(exc))
        return None
    if not isinstance(data, dict):
        add(findings, "FAIL", "invalid-manifest", path.relative_to(root), "manifest root must be an object")
        return None
    return data


def validate_marketplace(root: Path) -> tuple[list[Finding], dict[str, Any]]:
    findings: list[Finding] = []
    inventory: list[dict[str, str]] = []
    skills_root = root / "skills"
    if not skills_root.is_dir():
        add(findings, "FAIL", "missing-skills-root", Path("skills"), "canonical skills/ directory is missing")
        return findings, {"skills": inventory}

    all_skill_files = sorted(skills_root.rglob("SKILL.md"))
    if not all_skill_files:
        add(findings, "FAIL", "empty-catalog", Path("skills"), "no SKILL.md files found")

    names: dict[str, Path] = {}
    for skill_file in all_skill_files:
        rel = skill_file.relative_to(root)
        depth = len(skill_file.relative_to(skills_root).parts)
        if depth not in (2, 3):
            add(findings, "FAIL", "unsupported-depth", rel, "skill.sh-compatible layout allows zero or one category level")
        text = skill_file.read_text(encoding="utf-8")
        name, description, version, error = frontmatter(text)
        if error:
            add(findings, "FAIL", "frontmatter", rel, error)
            continue
        folder = skill_file.parent.name
        if not name or not NAME.fullmatch(name):
            add(findings, "FAIL", "invalid-name", rel, f"invalid or missing name: {name!r}")
        elif name != folder:
            add(findings, "FAIL", "name-directory-mismatch", rel, f"name {name!r} does not match {folder!r}")
        elif name in names:
            add(findings, "FAIL", "duplicate-name", rel, f"also declared by {names[name].as_posix()}")
        else:
            names[name] = rel
        if not description:
            add(findings, "FAIL", "missing-description", rel, "description is required")
        if not version or not SEMVER.fullmatch(version):
            add(findings, "FAIL", "invalid-version", rel, f"metadata.version must be a SemVer string, got {version!r}")
        inventory.append({"name": name or "", "version": version or "", "path": rel.as_posix()})
        for markdown in skill_file.parent.rglob("*.md"):
            local_links(markdown, root, findings)

    for symlink in root.rglob("*"):
        if symlink.is_symlink():
            add(findings, "FAIL", "symlink", symlink.relative_to(root), "portable distributions must not rely on symlinks")
        elif symlink.name == ".DS_Store" or symlink.name == "__pycache__" or symlink.suffix == ".pyc":
            add(findings, "WARN", "non-runtime-artifact", symlink.relative_to(root), "exclude generated or OS metadata from distribution bundles")

    market_path = root / ".claude-plugin" / "marketplace.json"
    if market_path.exists():
        data = validate_json_manifest(market_path, root, findings)
        if data is not None:
            plugins = data.get("plugins")
            if not data.get("name") or not isinstance(plugins, list):
                add(findings, "FAIL", "marketplace-schema", market_path.relative_to(root), "name and plugins[] are required")
            else:
                entry_names: set[str] = set()
                for index, entry in enumerate(plugins):
                    if not isinstance(entry, dict) or not entry.get("name"):
                        add(findings, "FAIL", "marketplace-entry", market_path.relative_to(root), f"plugins[{index}] lacks name")
                        continue
                    entry_name = str(entry["name"])
                    if entry_name in entry_names:
                        add(findings, "FAIL", "duplicate-plugin-entry", market_path.relative_to(root), entry_name)
                    entry_names.add(entry_name)
                    for key in ("source", "skills"):
                        for local in resolve_local(root, entry.get(key)):
                            if not local.exists():
                                add(findings, "FAIL", "missing-component-path", market_path.relative_to(root), f"{key} path does not exist: {local.relative_to(root)}")

    plugin_paths = [root / ".claude-plugin" / "plugin.json", root / "plugin" / ".claude-plugin" / "plugin.json"]
    for plugin_path in (path for path in plugin_paths if path.exists()):
        data = validate_json_manifest(plugin_path, root, findings)
        if data is not None:
            plugin_root = plugin_path.parent.parent
            if not data.get("name"):
                add(findings, "FAIL", "plugin-schema", plugin_path.relative_to(root), "plugin name is required")
            for local in resolve_local(plugin_root, data.get("skills", [])):
                if not local.exists():
                    add(findings, "FAIL", "missing-plugin-skill-path", plugin_path.relative_to(root), str(local))

    if not any(f.level == "FAIL" for f in findings):
        add(findings, "PASS", "portable-structure", Path("."), f"validated {len(inventory)} skills")
    return findings, {"skills": inventory}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    findings, inventory = validate_marketplace(root)
    counts = {level: sum(f.level == level for f in findings) for level in ("PASS", "WARN", "FAIL")}
    payload = {"root": str(root), "counts": counts, "inventory": inventory, "findings": [asdict(f) for f in findings]}
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for finding in findings:
            print(f"{finding.level:4} {finding.code:28} {finding.path}: {finding.message}")
        print(f"Summary: PASS={counts['PASS']} WARN={counts['WARN']} FAIL={counts['FAIL']}")
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
