#!/usr/bin/env python3
"""Generate individual Claude Code marketplace entries from canonical skills."""

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
    result = description.split(" Use ", 1)[0].strip()
    return result if len(result) <= 240 else result[:237].rstrip() + "..."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    parser.add_argument("--check", action="store_true", help="Fail if the committed manifest differs")
    args = parser.parse_args()
    root = args.root.resolve()
    release = read_json(root / "catalog" / "release.json")
    entries_config = read_json(root / "catalog" / "entries.json")
    marketplace = release["marketplace"]
    category = release["category"]
    category_root = root / "skills" / category
    configured = entries_config.get("entries", [])
    if not isinstance(configured, list):
        raise ValueError("catalog/entries.json entries must be an array")

    actual_names = {path.parent.name for path in category_root.glob("*/SKILL.md")}
    configured_names = {item.get("name") for item in configured if isinstance(item, dict)}
    if actual_names != configured_names:
        missing = sorted(actual_names - configured_names)
        extra = sorted(configured_names - actual_names)
        raise ValueError(f"catalog mismatch; missing={missing}, extra={extra}")

    plugins = []
    for item in sorted(configured, key=lambda value: value["name"]):
        name = item["name"]
        skill_file = category_root / name / "SKILL.md"
        declared_name, description, version, error = frontmatter(skill_file.read_text(encoding="utf-8"))
        if error or declared_name != name or not description or not version:
            raise ValueError(f"invalid skill metadata: {skill_file}: {error or declared_name}")
        plugins.append(
            {
                "name": name,
                "source": "./",
                "strict": False,
                "description": short_description(description),
                "version": version,
                "author": {
                    "name": release["publisher"]["brand"],
                    "email": release["reviewer"]["email"],
                },
                "category": category,
                "tags": ["agent-skills", "metaskills", *item.get("tags", [])],
                "skills": f"./skills/{category}/{name}",
            }
        )

    value = {
        "name": marketplace["name"],
        "owner": {"name": marketplace["owner"]},
        "metadata": {
            "description": "InnovationMachine Agent Skills marketplace",
            "version": "1.0.0",
            "pluginRoot": "./",
        },
        "plugins": plugins,
    }
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    target = root / ".claude-plugin" / "marketplace.json"
    if args.check:
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current != rendered:
            print("FAIL .claude-plugin/marketplace.json is stale", file=sys.stderr)
            return 1
        print(f"PASS marketplace manifest is current ({len(plugins)} entries)")
        return 0
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding="utf-8")
    print(f"Generated {target} with {len(plugins)} individual entries")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        sys.exit(1)
