#!/usr/bin/env python3
"""Run deterministic cross-host repository and marketplace checks."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

sys.dont_write_bytecode = True

from validate_marketplace import validate_marketplace
from manage_agent_assets import validate as validate_agent_assets
from validate_documentation import validate as validate_documentation


LOCAL_PATH = re.compile(r"(?:/Users/|/home/|[A-Za-z]:\\\\)")


def load_object(path: Path, failures: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"invalid JSON {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        failures.append(f"JSON object required: {path}")
        return {}
    return value


def safe_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    pure = PurePosixPath(value.removeprefix("./"))
    return not pure.is_absolute() and ".." not in pure.parts


def compare_trees(source: Path, bundled: Path, failures: list[str], label: str) -> None:
    source_files = {
        path.relative_to(source).as_posix(): path
        for path in source.rglob("*")
        if path.is_file() and path.name not in {".DS_Store"} and path.suffix != ".pyc"
    }
    bundle_files = {
        path.relative_to(bundled).as_posix(): path
        for path in bundled.rglob("*")
        if path.is_file() and path.name not in {".DS_Store"} and path.suffix != ".pyc"
    }
    if source_files.keys() != bundle_files.keys():
        failures.append(f"{label}: bundled file inventory differs from canonical source")
        return
    for relative, source_path in source_files.items():
        if source_path.read_bytes() != bundle_files[relative].read_bytes():
            failures.append(f"{label}: bundled content drift at {relative}")


def validate_instruction_pairs(root: Path) -> list[str]:
    """Require every CLAUDE.md/AGENTS.md pair to exist and stay identical."""
    failures: list[str] = []
    directories = {
        path.parent
        for name in ("CLAUDE.md", "AGENTS.md")
        for path in root.rglob(name)
        if ".git" not in path.relative_to(root).parts
    }
    for directory in sorted(directories):
        claude = directory / "CLAUDE.md"
        agents = directory / "AGENTS.md"
        label = directory.relative_to(root).as_posix() or "."
        if not claude.is_file() or not agents.is_file():
            missing = "CLAUDE.md" if not claude.is_file() else "AGENTS.md"
            failures.append(f"{label}: instruction pair is missing {missing}")
            continue
        if claude.read_bytes() != agents.read_bytes():
            failures.append(f"{label}: CLAUDE.md and AGENTS.md must be byte-identical")
    return failures


def validate_marketplace_names(path: Path, expected: set[str], failures: list[str]) -> dict:
    data = load_object(path, failures)
    plugins = data.get("plugins")
    if not isinstance(plugins, list):
        failures.append(f"{path}: plugins[] is required")
        return data
    names = [item.get("name") for item in plugins if isinstance(item, dict)]
    if len(names) != len(set(names)):
        failures.append(f"{path}: plugin names must be unique")
    if set(names) != expected:
        failures.append(f"{path}: entries do not match canonical skills")
    return data


def validate_plugin_bundle(
    root: Path,
    plugin_root: Path,
    expected_names: list[str],
    versions: dict[str, str],
    sources: dict[str, Path],
    failures: list[str],
    expected_plugin_name: str | None = None,
) -> None:
    label = plugin_root.relative_to(root).as_posix()
    for platform in ("claude", "codex", "cursor"):
        manifest = plugin_root / f".{platform}-plugin" / "plugin.json"
        data = load_object(manifest, failures)
        expected_name = expected_plugin_name or plugin_root.name
        if data.get("name") != expected_name:
            failures.append(f"{label}: {platform} manifest name must be {expected_name!r}")
        if data.get("version") != versions.get(expected_name, data.get("version")):
            failures.append(f"{label}: {platform} manifest version differs from canonical skill")
        paths = data.get("skills", "./skills/")
        values = paths if isinstance(paths, list) else [paths]
        for value in values:
            if not safe_relative_path(value):
                failures.append(f"{label}: unsafe {platform} skills path {value!r}")
        if platform == "codex":
            if not isinstance(data.get("author"), dict) or not isinstance(data.get("interface"), dict):
                failures.append(f"{label}: Codex manifest requires author and interface metadata")
            if data.get("skills", "").rstrip("/") != "./skills":
                failures.append(f"{label}: Codex skills path must resolve to ./skills/")
        if platform == "cursor":
            if not data.get("description") or not isinstance(data.get("author"), dict):
                failures.append(f"{label}: Cursor manifest requires description and author metadata")

    actual_names = sorted(path.parent.name for path in (plugin_root / "skills").glob("*/SKILL.md"))
    if actual_names != sorted(expected_names):
        failures.append(f"{label}: expected bundled skills {sorted(expected_names)}, found {actual_names}")
    for name in expected_names:
        compare_trees(
            sources[name],
            plugin_root / "skills" / name,
            failures,
            f"{label}/{name}",
        )


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    failures: list[str] = []
    failures.extend(validate_instruction_pairs(root))
    failures.extend(validate_documentation(root))
    failures.extend(validate_agent_assets(root))
    findings, inventory = validate_marketplace(root)
    failures.extend(f"{item.code}: {item.path}: {item.message}" for item in findings if item.level == "FAIL")
    skills = inventory["skills"]
    expected = {item["name"] for item in skills}
    versions = {item["name"]: item["version"] for item in skills}
    sources = {
        item["name"]: root / Path(item["path"]).parent
        for item in skills
    }
    dependencies = load_object(root / "catalog" / "dependencies.json", failures).get("skills", {})
    if not isinstance(dependencies, dict):
        failures.append("catalog/dependencies.json: skills object is required")
        dependencies = {}

    claude_path = root / ".claude-plugin" / "marketplace.json"
    codex_path = root / ".agents" / "plugins" / "marketplace.json"
    cursor_path = root / ".cursor-plugin" / "marketplace.json"
    claude = validate_marketplace_names(claude_path, expected, failures)
    codex = validate_marketplace_names(codex_path, expected, failures)
    cursor = validate_marketplace_names(cursor_path, expected, failures)

    for item in claude.get("plugins", []):
        if not isinstance(item, dict) or item.get("source") != f"./plugins/{item.get('name')}":
            failures.append(f"{claude_path}: every entry must point to its self-contained plugin bundle")
    for item in codex.get("plugins", []):
        if not isinstance(item, dict):
            continue
        source = item.get("source")
        policy = item.get("policy")
        if source != {"source": "local", "path": f"./plugins/{item.get('name')}"}:
            failures.append(f"{codex_path}: invalid local source for {item.get('name')}")
        if policy != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
            failures.append(f"{codex_path}: explicit install/auth policy required for {item.get('name')}")
        if not item.get("category"):
            failures.append(f"{codex_path}: category required for {item.get('name')}")
    for item in cursor.get("plugins", []):
        if not isinstance(item, dict):
            continue
        if item.get("source") != f"plugins/{item.get('name')}":
            failures.append(f"{cursor_path}: invalid source for {item.get('name')}")
        if not item.get("description"):
            failures.append(f"{cursor_path}: description required for {item.get('name')}")

    plugins_root = root / "plugins"
    actual_plugin_names = {path.name for path in plugins_root.iterdir() if path.is_dir()} if plugins_root.is_dir() else set()
    if actual_plugin_names != expected:
        failures.append("plugins/ must contain exactly one generated package per canonical skill")
    for name in sorted(expected & actual_plugin_names):
        validate_plugin_bundle(root, plugins_root / name, [name], versions, sources, failures)
        dependency_path = plugins_root / name / "skill-dependencies.json"
        declaration = dependencies.get(name)
        if declaration:
            payload = load_object(dependency_path, failures)
            if payload.get("skill") != name:
                failures.append(f"plugins/{name}: dependency metadata has wrong skill identity")
            for kind in ("required", "recommended"):
                if payload.get(kind) != declaration.get(kind, []):
                    failures.append(f"plugins/{name}: {kind} dependency metadata drift")
            readme = (plugins_root / name / "README.md").read_text(encoding="utf-8")
            if "DEPENDENCY WARNING" not in readme:
                failures.append(f"plugins/{name}: README must warn about companion dependencies")
            required_names = [item["name"] for item in declaration.get("required", [])]
            claude_manifest = load_object(plugins_root / name / ".claude-plugin" / "plugin.json", failures)
            if claude_manifest.get("dependencies", []) != required_names:
                failures.append(f"plugins/{name}: Claude native dependencies drift")
            for host in ("codex", "cursor"):
                manifest = load_object(plugins_root / name / f".{host}-plugin" / "plugin.json", failures)
                if "dependencies" in manifest:
                    failures.append(f"plugins/{name}: unsupported {host} dependencies field")
        elif dependency_path.exists():
            failures.append(f"plugins/{name}: unexpected dependency metadata")

    aggregate = root / "plugin"
    release = load_object(root / "catalog" / "release.json", failures)
    aggregate_name = release.get("aggregate_plugin", {}).get("name") if isinstance(release.get("aggregate_plugin"), dict) else None
    aggregate_version = release.get("aggregate_plugin", {}).get("version") if isinstance(release.get("aggregate_plugin"), dict) else None
    if aggregate_name and aggregate_version:
        aggregate_versions = {aggregate_name: aggregate_version}
        validate_plugin_bundle(
            root,
            aggregate,
            sorted(expected),
            aggregate_versions,
            sources,
            failures,
            expected_plugin_name=aggregate_name,
        )

    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] in {".git", "build"}:
            continue
        if path.is_symlink():
            failures.append(f"symlink is not allowed: {relative}")
        if path.name == ".DS_Store" or path.name == "__pycache__" or path.suffix == ".pyc":
            failures.append(f"non-runtime artifact: {relative}")
        if path.is_file() and "evals" not in relative.parts and path.suffix in {".json", ".yaml", ".yml"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            if LOCAL_PATH.search(text):
                failures.append(f"absolute local path in machine-readable file: {relative}")

    check = subprocess.run(
        [sys.executable, str(root / "scripts" / "generate_marketplace.py"), str(root), "--check"],
        text=True,
        capture_output=True,
        check=False,
    )
    if check.returncode:
        failures.append(check.stderr.strip() or check.stdout.strip() or "marketplace generation check failed")

    check = subprocess.run(
        [sys.executable, str(root / "scripts" / "generate_skill_readmes.py"), str(root), "--check"],
        text=True,
        capture_output=True,
        check=False,
    )
    if check.returncode:
        failures.append(check.stderr.strip() or check.stdout.strip() or "skill README generation check failed")

    dependency_checks = (
        [sys.executable, str(root / "scripts" / "manage_skill_dependencies.py"), "--root", str(root), "validate"],
        [sys.executable, str(root / "scripts" / "manage_skill_dependencies.py"), "--root", str(root), "render", "--check"],
    )
    for command in dependency_checks:
        check = subprocess.run(command, text=True, capture_output=True, check=False)
        if check.returncode:
            failures.append(check.stderr.strip() or check.stdout.strip() or "skill dependency validation failed")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print(f"PASS repository: {len(skills)} skills, three marketplaces, {len(actual_plugin_names)} individual plugins")
    return 0


if __name__ == "__main__":
    sys.exit(main())
