#!/usr/bin/env python3
"""Build one self-contained Claude Code, Codex, and Cursor plugin bundle."""

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


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def compact_text(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    shortened = value[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:-")
    return shortened + "…"


def is_package_private_skill(skill_file: Path, skills_root: Path) -> bool:
    parts = skill_file.relative_to(skills_root).parts
    return (
        len(parts) >= 4
        and parts[-3] == "private-skills"
        and (skill_file.parents[2] / "SKILL.md").is_file()
    )


def build_bundle(
    *,
    root: Path,
    output: Path,
    plugin_name: str,
    display_name: str,
    version: str,
    description: str,
    author_name: str,
    author_email: str,
    author_url: str,
    repository_url: str,
    license_name: str,
    codex_category: str,
    keywords: list[str],
    skill_names: list[str] | None = None,
    dependencies: dict | None = None,
    marketplace_name: str | None = None,
) -> None:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        raise ValueError(f"missing canonical skills directory: {skills_root}")
    if output.exists():
        raise ValueError(f"output already exists; use a new staging directory: {output}")
    if output == root or output == skills_root or skills_root in output.parents:
        raise ValueError("output must not replace or be nested inside the canonical skills tree")
    if not PLUGIN_NAME.fullmatch(plugin_name):
        raise ValueError("plugin name must be lowercase kebab-case")
    if not SEMVER.fullmatch(version):
        raise ValueError("version must be SemVer")

    symlinks = [path for path in skills_root.rglob("*") if path.is_symlink()]
    if symlinks:
        raise ValueError(f"source contains symlinks; first: {symlinks[0]}")

    available: dict[str, Path] = {}
    for skill_file in sorted(skills_root.rglob("SKILL.md")):
        parts = skill_file.relative_to(skills_root).parts
        if len(parts) not in (2, 3):
            if is_package_private_skill(skill_file, skills_root):
                continue
            raise ValueError("only canonical skills or parent-owned private-skills are supported")
        name = skill_file.parent.name
        if name in available:
            raise ValueError(f"duplicate canonical skill name: {name}")
        available[name] = skill_file.parent
    selected = sorted(skill_names or available)
    missing = sorted(set(selected) - set(available))
    if missing:
        raise ValueError(f"unknown skills: {missing}")
    if not selected:
        raise ValueError("no skills selected")

    output.mkdir(parents=True)
    excluded_patterns = [".DS_Store", "__pycache__", "*.pyc", ".git"]
    for name in selected:
        shutil.copytree(
            available[name],
            output / "skills" / name,
            ignore=shutil.ignore_patterns(*excluded_patterns),
        )

    required_dependencies = dependencies.get("required", []) if dependencies else []
    manifest_description = description
    if required_dependencies:
        manifest_description = (
            compact_text(description, 170)
            + " Companion skill plugins are required for full functionality; see README.md."
        )
    common = {
        "name": plugin_name,
        "version": version,
        "description": manifest_description,
        "homepage": repository_url,
        "repository": repository_url,
        "license": license_name,
        "keywords": sorted(set(keywords)),
        "skills": "./skills/",
    }
    claude = {
        "name": plugin_name,
        "displayName": display_name,
        "version": version,
        "description": manifest_description,
        "skills": ["./skills"],
        "author": {"name": author_name, "email": author_email},
    }
    if required_dependencies:
        claude["dependencies"] = [item["name"] for item in required_dependencies]
    codex = {
        **common,
        "author": {"name": author_name, "email": author_email, "url": author_url},
        "interface": {
            "displayName": display_name,
            "shortDescription": compact_text(manifest_description, 120),
            "longDescription": manifest_description,
            "developerName": author_name,
            "category": codex_category,
            "capabilities": ["Guidance"],
            "websiteURL": repository_url,
            "defaultPrompt": f"Use {display_name} for this task.",
        },
    }
    cursor = {
        **common,
        "author": {"name": author_name, "email": author_email},
    }
    write_json(output / ".claude-plugin" / "plugin.json", claude)
    write_json(output / ".codex-plugin" / "plugin.json", codex)
    write_json(output / ".cursor-plugin" / "plugin.json", cursor)

    dependency_section = ""
    if dependencies:
        dependency_payload = {
            "schema_version": 1,
            "skill": plugin_name,
            "native_auto_install": {
                "claude-code": True,
                "codex": False,
                "cursor": False,
            },
            "required": dependencies.get("required", []),
            "recommended": dependencies.get("recommended", []),
            "install_order": dependencies.get("install_order", []),
        }
        write_json(output / "skill-dependencies.json", dependency_payload)
        required_lines = "\n".join(
            f"- `{item['name']}>={item['minimum_version']}` — {item['reason']}"
            for item in dependency_payload["required"]
        ) or "- None."
        recommended_lines = "\n".join(
            f"- `{item['name']}>={item['minimum_version']}` — {item['reason']}"
            for item in dependency_payload["recommended"]
        ) or "- None."
        install_lines = "\n".join(
            f"codex plugin add {name}@{marketplace_name}"
            for name in dependency_payload["install_order"]
        )
        dependency_section = (
            "## Companion skill dependencies\n\n"
            "> **DEPENDENCY WARNING:** Claude Code auto-installs the required "
            "companions from this marketplace. Codex and Cursor require the "
            "dependency-first install plan below before using affected routes.\n\n"
            "Required:\n\n"
            f"{required_lines}\n\n"
            "Recommended:\n\n"
            f"{recommended_lines}\n\n"
            "Codex install order:\n\n"
            "```bash\n"
            f"{install_lines}\n"
            "```\n\n"
            "The machine-readable declaration is in `skill-dependencies.json`.\n\n"
        )

    bundled = "\n".join(f"- `{name}`" for name in selected)
    readme = (
        f"# {display_name}\n\n"
        f"{description}\n\n"
        "This generated package is installable by Claude Code, Codex, and Cursor. "
        "Its canonical source lives under `skills/` in the repository root; do not edit this bundle directly.\n\n"
        "## Bundled skills\n\n"
        f"{bundled}\n\n"
        f"{dependency_section}"
        "No credentials or host-specific absolute paths are included. Review bundled scripts before execution.\n"
    )
    (output / "README.md").write_text(readme, encoding="utf-8")

    files = []
    for path in sorted(item for item in output.rglob("*") if item.is_file()):
        files.append(
            {
                "path": path.relative_to(output).as_posix(),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
        )
    build_manifest = {
        "format": 2,
        "plugin": plugin_name,
        "version": version,
        "source_layout": "skills/",
        "bundle_layout": "skills/<name>/",
        "platforms": ["claude-code", "codex", "cursor"],
        "skills": selected,
        "excluded_patterns": excluded_patterns,
        "files": files,
    }
    write_json(output / "build-manifest.json", build_manifest)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Marketplace root containing canonical skills/")
    parser.add_argument("output", type=Path, help="New output directory; must not exist")
    parser.add_argument("--plugin-name", required=True)
    parser.add_argument("--display-name")
    parser.add_argument("--version", required=True)
    parser.add_argument("--description", default="Portable Agent Skills bundle")
    parser.add_argument("--author-name", required=True)
    parser.add_argument("--author-email", required=True)
    parser.add_argument("--author-url", required=True)
    parser.add_argument("--repository-url", required=True)
    parser.add_argument("--license", dest="license_name", required=True)
    parser.add_argument("--codex-category", required=True)
    parser.add_argument("--keyword", action="append", default=[])
    parser.add_argument("--skill", action="append", dest="skill_names")
    args = parser.parse_args()

    build_bundle(
        root=args.root.resolve(),
        output=args.output.resolve(),
        plugin_name=args.plugin_name,
        display_name=args.display_name or args.plugin_name.replace("-", " ").title(),
        version=args.version,
        description=args.description,
        author_name=args.author_name,
        author_email=args.author_email,
        author_url=args.author_url,
        repository_url=args.repository_url,
        license_name=args.license_name,
        codex_category=args.codex_category,
        keywords=args.keyword,
        skill_names=args.skill_names,
    )
    print(f"Built {args.plugin_name}@{args.version} for Claude Code, Codex, and Cursor at {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        sys.exit(1)
