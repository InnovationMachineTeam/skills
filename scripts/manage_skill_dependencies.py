#!/usr/bin/env python3
"""Validate, render, plan, check, and install companion skill plugins."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from validate_marketplace import frontmatter


SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
GENERATED_MARKER = "<!-- generated from catalog/dependencies.json; do not edit -->"


def read_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def inventory(root: Path) -> tuple[dict[str, dict], dict[str, str], dict[str, Path]]:
    entries = read_object(root / "catalog" / "entries.json").get("entries")
    if not isinstance(entries, list):
        raise ValueError("catalog/entries.json entries must be an array")
    configured = {item["name"]: item for item in entries if isinstance(item, dict)}
    versions: dict[str, str] = {}
    paths: dict[str, Path] = {}
    for name, item in configured.items():
        path = root / "skills" / item["category"] / name
        declared, _, version, error = frontmatter((path / "SKILL.md").read_text(encoding="utf-8"))
        if error or declared != name or not version:
            raise ValueError(f"invalid canonical skill metadata: {path / 'SKILL.md'}")
        versions[name] = version
        paths[name] = path
    return configured, versions, paths


def semver_core(value: str) -> tuple[int, int, int]:
    if not SEMVER.fullmatch(value):
        raise ValueError(f"invalid SemVer: {value!r}")
    return tuple(int(part) for part in value.split("-", 1)[0].split("+", 1)[0].split("."))


def load_graph(root: Path) -> tuple[dict, dict[str, dict], dict[str, str], dict[str, Path]]:
    document = read_object(root / "catalog" / "dependencies.json")
    graph = document.get("skills")
    if document.get("schema_version") != 1 or not isinstance(graph, dict):
        raise ValueError("catalog/dependencies.json requires schema_version 1 and skills object")
    configured, versions, paths = inventory(root)
    return document, graph, versions, paths


def dependency_items(graph: dict[str, dict], skill: str, kind: str) -> list[dict]:
    declaration = graph.get(skill, {})
    value = declaration.get(kind, []) if isinstance(declaration, dict) else []
    if not isinstance(value, list):
        raise ValueError(f"{skill}.{kind} must be an array")
    return value


def validate_graph(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        document, graph, versions, _ = load_graph(root)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]
    policy = document.get("policy")
    native = policy.get("native_plugin_dependencies") if isinstance(policy, dict) else None
    if native != {"claude-code": True, "codex": False, "cursor": False}:
        errors.append("policy.native_plugin_dependencies must declare Claude support and Codex/Cursor fallback")
    known = set(versions)
    for owner, declaration in graph.items():
        if owner not in known:
            errors.append(f"unknown dependent skill: {owner}")
            continue
        if not isinstance(declaration, dict):
            errors.append(f"dependency declaration must be an object: {owner}")
            continue
        seen: set[str] = set()
        for kind in ("required", "recommended"):
            try:
                items = dependency_items(graph, owner, kind)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            for index, item in enumerate(items):
                label = f"{owner}.{kind}[{index}]"
                if not isinstance(item, dict):
                    errors.append(f"{label} must be an object")
                    continue
                name = item.get("name")
                minimum = item.get("minimum_version")
                reason = item.get("reason")
                if name not in known:
                    errors.append(f"{label} references unknown skill: {name!r}")
                if name == owner:
                    errors.append(f"{label} cannot depend on itself")
                if name in seen:
                    errors.append(f"{owner} declares duplicate dependency: {name}")
                if isinstance(name, str):
                    seen.add(name)
                if not isinstance(minimum, str) or not SEMVER.fullmatch(minimum):
                    errors.append(f"{label} has invalid minimum_version: {minimum!r}")
                elif isinstance(name, str) and name in versions and semver_core(versions[name]) < semver_core(minimum):
                    errors.append(f"{label} requires {name}>={minimum}, canonical version is {versions[name]}")
                if not isinstance(reason, str) or not reason.strip():
                    errors.append(f"{label} requires a reason")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(name: str, trail: list[str]) -> None:
        if name in visiting:
            errors.append("required dependency cycle: " + " -> ".join([*trail, name]))
            return
        if name in visited:
            return
        visiting.add(name)
        for item in dependency_items(graph, name, "required"):
            target = item.get("name") if isinstance(item, dict) else None
            if isinstance(target, str) and target in known:
                visit(target, [*trail, name])
        visiting.remove(name)
        visited.add(name)

    for name in sorted(graph):
        visit(name, [])
    return errors


def ordered_plan(graph: dict[str, dict], skill: str, include_recommended: bool = False) -> list[str]:
    order: list[str] = []
    visited: set[str] = set()

    def visit(name: str) -> None:
        if name in visited:
            return
        visited.add(name)
        kinds = ("required", "recommended") if include_recommended else ("required",)
        for kind in kinds:
            for item in dependency_items(graph, name, kind):
                visit(item["name"])
        order.append(name)

    visit(skill)
    return order


def install_command(host: str, name: str, marketplace: str) -> list[str]:
    if host == "codex":
        return ["codex", "plugin", "add", f"{name}@{marketplace}"]
    if host == "claude":
        return ["claude", "plugin", "install", f"{name}@{marketplace}"]
    raise ValueError(f"unsupported host: {host}")


def render_reference(skill: str, declaration: dict, marketplace: str) -> str:
    required = declaration.get("required", [])
    recommended = declaration.get("recommended", [])

    def table(items: list[dict]) -> str:
        if not items:
            return "None."
        rows = ["| Skill | Minimum | Why |", "|---|---:|---|"]
        rows.extend(f"| `{item['name']}` | `{item['minimum_version']}` | {item['reason']} |" for item in items)
        return "\n".join(rows)

    commands = "\n".join(
        f"codex plugin add {item['name']}@{marketplace}"
        for item in [*required, {"name": skill}]
    )
    return (
        "# Companion skill dependencies\n\n"
        f"{GENERATED_MARKER}\n\n"
        "Claude Code supports native same-marketplace plugin dependencies. Codex "
        "and Cursor do not share that manifest contract, so they use generated "
        "warnings and an explicit install plan. Companions remain separate plugins "
        "so their identities do not collide.\n\n"
        "## Required for full route coverage\n\n"
        f"{table(required)}\n\n"
        "## Recommended\n\n"
        f"{table(recommended)}\n\n"
        "## Runtime rule\n\n"
        "Before dispatching a route, compare its owning companion with the skills "
        "available in the current session. If a required companion is missing or "
        "older than the minimum, emit a visible `DEPENDENCY WARNING`, name the "
        "blocked route, and do not imitate that specialist. Other routes may "
        "continue when their companions are available. Missing recommended skills "
        "are informational unless the chosen workflow needs them. If installed "
        "state cannot be inspected, say that dependency status is unverified.\n\n"
        "## Codex installation\n\n"
        "From the marketplace repository, preview or execute the complete plan:\n\n"
        "```bash\n"
        f"python3 scripts/manage_skill_dependencies.py plan {skill} --host codex\n"
        f"python3 scripts/manage_skill_dependencies.py install {skill} --host codex --execute\n"
        "```\n\n"
        "Manual equivalent:\n\n"
        "```bash\n"
        f"{commands}\n"
        "```\n\n"
        "For Claude Code, install only the requested plugin; its generated "
        "`dependencies` array auto-installs required companions from the same "
        "marketplace.\n"
    )


def render_references(root: Path, check: bool) -> list[str]:
    _, graph, _, paths = load_graph(root)
    marketplace = read_object(root / "catalog" / "release.json")["marketplace"]["name"]
    stale: list[str] = []
    for skill, declaration in sorted(graph.items()):
        target = paths[skill] / "references" / "skill-dependencies.md"
        expected = render_reference(skill, declaration, marketplace)
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current != expected:
            stale.append(target.relative_to(root).as_posix())
            if not check:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(expected, encoding="utf-8")
    return stale


def installed_codex() -> dict[str, str]:
    result = subprocess.run(["codex", "plugin", "list", "--json"], text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "codex plugin list failed")
    payload = json.loads(result.stdout)
    return {
        item["name"]: item["version"]
        for item in payload.get("installed", [])
        if isinstance(item, dict) and item.get("installed") and item.get("enabled")
    }


def required_findings(declaration: dict, installed: dict[str, str]) -> tuple[list[str], list[str]]:
    missing: list[str] = []
    outdated: list[str] = []
    for item in declaration.get("required", []):
        actual = installed.get(item["name"])
        if actual is None:
            missing.append(item["name"])
        elif semver_core(actual) < semver_core(item["minimum_version"]):
            outdated.append(f"{item['name']}={actual}<{item['minimum_version']}")
    return missing, outdated


def warning_text(missing: list[str], outdated: list[str]) -> str:
    lines = ["DEPENDENCY WARNING"]
    if missing:
        lines.append("Missing required companion plugins: " + ", ".join(missing))
    if outdated:
        lines.append("Outdated required companion plugins: " + ", ".join(outdated))
    return "\n".join(lines)


def main() -> int:
    default_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_root)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    render_parser = sub.add_parser("render")
    render_parser.add_argument("--check", action="store_true")
    for command in ("plan", "install"):
        item = sub.add_parser(command)
        item.add_argument("skill")
        item.add_argument("--host", choices=("codex", "claude"), default="codex")
        item.add_argument("--marketplace")
        item.add_argument("--include-recommended", action="store_true")
        if command == "plan":
            item.add_argument("--json", action="store_true", dest="json_output")
        else:
            item.add_argument("--execute", action="store_true")
    check_parser = sub.add_parser("check")
    check_parser.add_argument("skill")
    check_parser.add_argument("--host", choices=("codex",), default="codex")
    args = parser.parse_args()
    root = args.root.resolve()

    errors = validate_graph(root)
    if errors:
        for error in errors:
            print(f"FAIL {error}", file=sys.stderr)
        return 1
    document, graph, versions, _ = load_graph(root)
    if args.command == "validate":
        print(f"PASS dependency graph: {len(graph)} dependent skills, {len(versions)} catalog skills")
        return 0
    if args.command == "render":
        stale = render_references(root, args.check)
        if stale and args.check:
            for path in stale:
                print(f"FAIL stale generated dependency reference: {path}", file=sys.stderr)
            return 1
        print(f"PASS dependency references {'current' if args.check else 'generated'}: {len(graph)}")
        return 0
    if args.skill not in versions:
        raise ValueError(f"unknown skill: {args.skill}")
    declaration = graph.get(args.skill, {"required": [], "recommended": []})

    if args.command == "check":
        installed = installed_codex()
        missing, outdated = required_findings(declaration, installed)
        if missing or outdated:
            print(warning_text(missing, outdated))
            return 2
        print(f"PASS required companions available for {args.skill}")
        return 0

    release = read_object(root / "catalog" / "release.json")
    marketplace = args.marketplace or release["marketplace"]["name"]
    order = ordered_plan(graph, args.skill, args.include_recommended)
    install_names = [args.skill] if args.host == "claude" else order
    commands = [install_command(args.host, name, marketplace) for name in install_names]
    if args.command == "plan" and args.json_output:
        print(json.dumps({"skill": args.skill, "host": args.host, "order": order, "commands": commands}, indent=2))
        return 0
    print("Dependency-aware install order: " + " -> ".join(order))
    if args.host == "claude":
        print("Claude Code will resolve and auto-install required companions from the same marketplace.")
    for command in commands:
        print(" ".join(command))
    if args.command == "plan" or not args.execute:
        if args.command == "install":
            print("DRY RUN: pass --execute to install these plugins")
        return 0
    for command in commands:
        result = subprocess.run(command, check=False)
        if result.returncode:
            print(f"FAIL installation stopped at: {' '.join(command)}", file=sys.stderr)
            return result.returncode
    print(f"PASS installed {len(order)} plugins for {args.skill}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, KeyError, TypeError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        sys.exit(1)
