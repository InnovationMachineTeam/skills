#!/usr/bin/env python3
"""Generate deterministic host projections for registered project agents."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from manage_agent_assets import MAP_PATH, REGISTRY_PATH, content_hash, load_object, unversioned


GENERATED_MARKER = "Generated from the agent asset registry; do not edit manually."


def text_asset(path: Path, kind: str) -> str:
    source = path / "SKILL.md" if kind == "skill" and path.is_dir() else path
    return source.read_text(encoding="utf-8").strip()


def bound_capabilities(
    registry: dict[str, Any], mapping: dict[str, Any], agent_id: str
) -> list[dict[str, Any]]:
    assets = {
        item["id"]: item
        for item in registry.get("assets", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    result: list[dict[str, Any]] = []
    for binding in mapping.get("bindings", []):
        if not isinstance(binding, dict) or unversioned(binding.get("agent_ref")) != agent_id:
            continue
        asset = assets.get(unversioned(binding.get("capability_ref")) or "")
        if asset is not None and binding.get("status") != "revoked":
            result.append(asset)
    return sorted(result, key=lambda item: str(item.get("id")))


def capability_block(root: Path, assets: list[dict[str, Any]], *, include_public: bool) -> str:
    blocks: list[str] = []
    for asset in assets:
        if asset.get("visibility") != "private" and not include_public:
            continue
        source = root / str(asset["locator"])
        blocks.extend(
            [
                f"## Embedded capability: {asset['id']}",
                f"Source hash: {asset['content_sha256']}",
                "",
                text_asset(source, str(asset["kind"])),
                "",
            ]
        )
    return "\n".join(blocks).rstrip()


def quote_toml(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def codex_projection(root: Path, definition: dict[str, Any], assets: list[dict[str, Any]]) -> str:
    policy = definition.get("model_policy", {})
    preferred = policy.get("preferred", {}) if isinstance(policy, dict) else {}
    lines = [
        f"# {GENERATED_MARKER}",
        f"# agent-definition-sha256: {content_hash(root / definition['_locator'])}",
        f"name = {quote_toml(str(definition['name']))}",
        f"description = {quote_toml(str(definition['mission']['goal']))}",
    ]
    model = preferred.get("codex") if isinstance(preferred, dict) else None
    if isinstance(model, str) and model:
        lines.append(f"model = {quote_toml(model)}")
    if definition.get("risk_tier") in {"R0", "R1"}:
        lines.append('sandbox_mode = "read-only"')
    private_commands = [item for item in assets if item.get("kind") == "command" and item.get("visibility") == "private"]
    command_text = capability_block(root, private_commands, include_public=False)
    instructions = str(definition["mission"]["goal"])
    if command_text:
        instructions += "\n\n" + command_text
    lines.append(f"developer_instructions = {quote_toml(instructions)}")
    for asset in assets:
        if asset.get("kind") == "skill" and asset.get("visibility") == "private":
            lines.extend(
                [
                    "",
                    "[[skills.config]]",
                    f"path = {quote_toml('./' + str(asset['locator']))}",
                    "enabled = true",
                ]
            )
    return "\n".join(lines) + "\n"


def claude_projection(root: Path, definition: dict[str, Any], assets: list[dict[str, Any]]) -> str:
    policy = definition.get("model_policy", {})
    preferred = policy.get("preferred", {}) if isinstance(policy, dict) else {}
    model = preferred.get("claude-code", "inherit") if isinstance(preferred, dict) else "inherit"
    embedded = capability_block(root, assets, include_public=True)
    body = [
        "---",
        f"name: {definition['name']}",
        f"description: {json.dumps(definition['mission']['goal'], ensure_ascii=False)}",
        f"model: {model}",
        "disallowedTools: Skill",
        "---",
        "",
        f"<!-- {GENERATED_MARKER} -->",
        f"<!-- agent-definition-sha256: {content_hash(root / definition['_locator'])} -->",
        "",
        str(definition["mission"]["goal"]),
    ]
    if embedded:
        body.extend(["", embedded])
    return "\n".join(body).rstrip() + "\n"


def cursor_projection(root: Path, definition: dict[str, Any], assets: list[dict[str, Any]]) -> str:
    policy = definition.get("model_policy", {})
    preferred = policy.get("preferred", {}) if isinstance(policy, dict) else {}
    model = preferred.get("cursor", "inherit") if isinstance(preferred, dict) else "inherit"
    embedded = capability_block(root, assets, include_public=False)
    body = [
        "---",
        f"name: {definition['name']}",
        f"description: {json.dumps(definition['mission']['goal'], ensure_ascii=False)}",
        f"model: {model}",
        "readonly: true" if definition.get("risk_tier") in {"R0", "R1"} else "readonly: false",
        "---",
        "",
        f"<!-- {GENERATED_MARKER} -->",
        "<!-- Private capabilities are embedded because a stable per-agent allow-list is not assumed. -->",
        f"<!-- agent-definition-sha256: {content_hash(root / definition['_locator'])} -->",
        "",
        str(definition["mission"]["goal"]),
    ]
    if embedded:
        body.extend(["", embedded])
    return "\n".join(body).rstrip() + "\n"


def expected_outputs(root: Path) -> dict[Path, str]:
    registry = load_object(root / REGISTRY_PATH)
    mapping = load_object(root / MAP_PATH)
    outputs: dict[Path, str] = {}
    for asset in registry.get("assets", []):
        if not isinstance(asset, dict) or asset.get("kind") != "agent":
            continue
        definition_path = root / str(asset["locator"])
        definition = load_object(definition_path)
        definition["_locator"] = str(asset["locator"])
        capabilities = bound_capabilities(registry, mapping, str(asset["id"]))
        name = str(definition["name"])
        outputs[root / ".codex" / "agents" / f"{name}.toml"] = codex_projection(root, definition, capabilities)
        outputs[root / ".claude" / "agents" / f"{name}.md"] = claude_projection(root, definition, capabilities)
        outputs[root / ".cursor" / "agents" / f"{name}.md"] = cursor_projection(root, definition, capabilities)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    failures: list[str] = []
    try:
        outputs = expected_outputs(root)
        for path, expected in outputs.items():
            if args.check:
                actual = path.read_text(encoding="utf-8") if path.exists() else ""
                if actual != expected:
                    failures.append(f"generated agent adapter drift: {path.relative_to(root)}")
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(expected, encoding="utf-8")
        if args.check:
            expected_paths = {path.resolve() for path in outputs}
            for host_root in (root / ".codex" / "agents", root / ".claude" / "agents", root / ".cursor" / "agents"):
                if not host_root.is_dir():
                    continue
                for path in host_root.iterdir():
                    if path.is_file() and path.resolve() not in expected_paths and GENERATED_MARKER in path.read_text(encoding="utf-8", errors="replace"):
                        failures.append(f"orphan generated agent adapter: {path.relative_to(root)}")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        failures.append(str(exc))
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    action = "verified" if args.check else "generated"
    print(f"PASS {action} {len(outputs)} host adapter files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
