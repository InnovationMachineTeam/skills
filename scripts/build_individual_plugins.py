#!/usr/bin/env python3
"""Build one generated cross-host plugin package per canonical skill."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from build_plugin_bundle import build_bundle
from manage_skill_dependencies import load_graph, ordered_plan
from validate_marketplace import frontmatter


def plugin_description(description: str) -> str:
    result = description.split(". Use ", 1)[0].strip()
    if len(result) <= 240:
        return result
    shortened = result[:236].rsplit(" ", 1)[0].rstrip(" ,;:-")
    return shortened + "..."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    if output.exists():
        raise ValueError(f"output already exists; use a new staging directory: {output}")
    output.mkdir(parents=True)

    release = json.loads((root / "catalog" / "release.json").read_text(encoding="utf-8"))
    entries = json.loads((root / "catalog" / "entries.json").read_text(encoding="utf-8"))["entries"]
    distribution = release["distribution"]
    publisher = release["publisher"]
    reviewer = release["reviewer"]
    _, dependency_graph, _, _ = load_graph(root)

    for item in sorted(entries, key=lambda value: value["name"]):
        name = item["name"]
        category = item["category"]
        skill_file = root / "skills" / category / name / "SKILL.md"
        declared_name, description, version, error = frontmatter(skill_file.read_text(encoding="utf-8"))
        if error or declared_name != name or not description or not version:
            raise ValueError(f"invalid skill metadata: {skill_file}: {error or declared_name}")
        display_name = name.replace("-", " ").title()
        dependency_declaration = dependency_graph.get(name)
        dependency_payload = None
        if dependency_declaration:
            dependency_payload = {
                **dependency_declaration,
                "install_order": ordered_plan(dependency_graph, name),
            }
        build_bundle(
            root=root,
            output=output / name,
            plugin_name=name,
            display_name=display_name,
            version=version,
            description=plugin_description(description),
            author_name=publisher["brand"],
            author_email=reviewer["email"],
            author_url=publisher["url"],
            repository_url=distribution["repository_url"],
            license_name=distribution["license"],
            codex_category=distribution["codex_category"],
            keywords=item.get("keywords", ["agent-skills", category, *item.get("tags", [])]),
            skill_names=[name],
            dependencies=dependency_payload,
            marketplace_name=release["marketplace"]["name"],
        )
    print(f"Built {len(entries)} individual cross-host plugin packages at {output}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        sys.exit(1)
