#!/usr/bin/env python3
"""Generate Claude Code, Codex, and Cursor marketplace manifests."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from validate_marketplace import frontmatter


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"object required: {path}")
    return value


def short_description(description: str) -> str:
    result = description.split(". Use ", 1)[0].strip()
    if len(result) <= 240:
        return result
    shortened = result[:236].rsplit(" ", 1)[0].rstrip(" ,;:-")
    return shortened + "..."


def render(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    parser.add_argument("--check", action="store_true", help="Fail if any committed manifest differs")
    args = parser.parse_args()
    root = args.root.resolve()
    release = read_json(root / "catalog" / "release.json")
    entries_config = read_json(root / "catalog" / "entries.json")
    marketplace = release["marketplace"]
    marketplace_version = marketplace["version"]
    distribution = release["distribution"]
    configured = entries_config.get("entries", [])
    if not isinstance(configured, list):
        raise ValueError("catalog/entries.json entries must be an array")

    actual = {
        path.parent.name: path.parent.parent.name
        for path in (root / "skills").glob("*/*/SKILL.md")
    }
    configured_map = {
        item.get("name"): item.get("category")
        for item in configured
        if isinstance(item, dict)
    }
    if actual != configured_map:
        raise ValueError(f"catalog/category mismatch; actual={actual}, configured={configured_map}")

    records = []
    for item in sorted(configured, key=lambda value: value["name"]):
        name = item["name"]
        category = item["category"]
        skill_file = root / "skills" / category / name / "SKILL.md"
        declared_name, description, version, error = frontmatter(skill_file.read_text(encoding="utf-8"))
        if error or declared_name != name or not description or not version:
            raise ValueError(f"invalid skill metadata: {skill_file}: {error or declared_name}")
        records.append(
            {
                "name": name,
                "category": category,
                "description": short_description(description),
                "version": version,
                "tags": sorted(set(["agent-skills", category, *item.get("tags", [])])),
                "keywords": sorted(
                    set(item.get("keywords", ["agent-skills", category, *item.get("tags", [])]))
                ),
            }
        )

    author = {"name": release["publisher"]["brand"], "email": release["reviewer"]["email"]}
    claude = {
        "name": marketplace["name"],
        "owner": {"name": marketplace["owner"]},
        "metadata": {
            "description": "InnovationMachine Agent Skills marketplace",
            "version": marketplace_version,
        },
        "plugins": [
            {
                "name": item["name"],
                "source": f"./plugins/{item['name']}",
                "strict": False,
                "description": item["description"],
                "version": item["version"],
                "author": author,
                "category": item["category"],
                "tags": item["tags"],
            }
            for item in records
        ],
    }
    codex = {
        "name": marketplace["name"],
        "interface": {"displayName": "IM Skills"},
        "plugins": [
            {
                "name": item["name"],
                "source": {"source": "local", "path": f"./plugins/{item['name']}"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": distribution["codex_category"],
            }
            for item in records
        ],
    }
    cursor = {
        "name": marketplace["name"],
        "owner": {"name": marketplace["owner"], "email": release["reviewer"]["email"]},
        "metadata": {
            "description": "InnovationMachine Agent Skills marketplace",
            "version": marketplace_version,
        },
        "plugins": [
            {
                "name": item["name"],
                "source": f"plugins/{item['name']}",
                "description": item["description"],
                "version": item["version"],
                "author": author,
                "homepage": distribution["repository_url"],
                "repository": distribution["repository_url"],
                "license": distribution["license"],
                "keywords": item["keywords"],
                "category": item["category"],
                "tags": item["tags"],
            }
            for item in records
        ],
    }
    targets = {
        root / ".claude-plugin" / "marketplace.json": render(claude),
        root / ".agents" / "plugins" / "marketplace.json": render(codex),
        root / ".cursor-plugin" / "marketplace.json": render(cursor),
    }

    stale = []
    for target, rendered in targets.items():
        if args.check:
            current = target.read_text(encoding="utf-8") if target.exists() else ""
            if current != rendered:
                stale.append(target.relative_to(root).as_posix())
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rendered, encoding="utf-8")
    if stale:
        for path in stale:
            print(f"FAIL {path} is stale", file=sys.stderr)
        return 1
    action = "current" if args.check else "generated"
    print(f"PASS {len(targets)} marketplace manifests {action} ({len(records)} entries each)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        sys.exit(1)
