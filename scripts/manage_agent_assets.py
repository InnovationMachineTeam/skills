#!/usr/bin/env python3
"""Register, render, and validate canonical agent assets without dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

sys.dont_write_bytecode = True

from validate_marketplace import frontmatter


ASSET_ID = re.compile(r"^asset://(repository|project|user|organization)/(agent|skill|command|workflow|team)/[a-z0-9][a-z0-9./-]*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA = re.compile(r"^sha256:[a-f0-9]{64}$")
SKIP_DIRS = {".git", ".svn", "__pycache__", "node_modules", "build", "dist"}
SKIP_FILES = {".DS_Store"}
KINDS = {"agent", "skill", "command", "workflow", "team"}
HOSTS = {"codex", "claude-code", "cursor", "agent-skills"}
REGISTRY_PATH = Path("docs/AGENT-ASSET-REGISTRY.json")
MAP_PATH = Path("docs/AGENT-SKILLS-MAP.json")
REGISTRY_VIEW = Path("docs/AGENT-ASSET-REGISTRY.md")
MAP_VIEW = Path("docs/AGENT-SKILLS-MAP.md")


def canonical_skill_files(root: Path) -> list[Path]:
    skills_root = root / "skills"
    return sorted(
        path for path in skills_root.rglob("SKILL.md")
        if len(path.relative_to(skills_root).parts) in (2, 3)
    )


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(rendered)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def safe_locator(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    pure = PurePosixPath(value)
    return not pure.is_absolute() and ".." not in pure.parts


def content_hash(path: Path) -> str:
    digest = hashlib.sha256()
    paths: list[Path]
    if path.is_file():
        paths = [path]
        root = path.parent
    elif path.is_dir():
        paths = []
        root = path
        for current, dirnames, filenames in os.walk(path, followlinks=False):
            dirnames[:] = sorted(name for name in dirnames if name not in SKIP_DIRS)
            for filename in sorted(filenames):
                candidate = Path(current) / filename
                if filename in SKIP_FILES or filename.endswith((".pyc", ".pyo")) or candidate.is_symlink():
                    continue
                paths.append(candidate)
    else:
        raise ValueError(f"asset locator does not exist: {path}")
    for candidate in sorted(paths):
        relative = candidate.relative_to(root).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(candidate.read_bytes())
        digest.update(b"\0")
    return "sha256:" + digest.hexdigest()


def unversioned(reference: object) -> str | None:
    if not isinstance(reference, str):
        return None
    return reference.split("@", 1)[0]


def version_of(reference: object) -> str | None:
    if not isinstance(reference, str) or "@" not in reference:
        return None
    return reference.rsplit("@", 1)[1].removeprefix("^")


def private_locator(locator: str, kind: str) -> bool:
    parts = PurePosixPath(locator).parts
    if len(parts) < 5 or parts[0:2] != (".agents", "definitions"):
        return False
    expected = "skills" if kind == "skill" else "commands" if kind == "command" else None
    return expected is not None and parts[3] == expected


def identity(path: Path, kind: str) -> tuple[str, str | None]:
    if kind == "skill":
        skill_file = path / "SKILL.md" if path.is_dir() else path
        name, _description, version, error = frontmatter(skill_file.read_text(encoding="utf-8"))
        if error or not name or not version:
            raise ValueError(f"invalid skill identity at {skill_file}: {error or 'missing name/version'}")
        return name, version
    if kind == "command":
        return path.stem, None
    if not path.is_file():
        raise ValueError(f"{kind} locator must be a JSON file: {path}")
    data = load_object(path)
    name = data.get("name")
    version = data.get("version")
    if not isinstance(name, str) or not isinstance(version, str):
        raise ValueError(f"{kind} definition requires name and version: {path}")
    return name, version


def base_asset(
    *, root: Path, asset_id: str, kind: str, locator: str, visibility: str,
    accountable_owner: str, owner_agent_ref: str | None, allowed_consumers: list[str],
    revision: int = 1, parent_version_ref: str | None = None,
) -> dict[str, Any]:
    resolved = root / locator
    name, version = identity(resolved, kind)
    command = kind == "command"
    namespace = asset_id.removeprefix("asset://").split("/", 1)[0]
    public_scope = namespace if namespace in {"project", "repository", "user", "organization"} else "project"
    return {
        "id": asset_id,
        "kind": kind,
        "name": name,
        "version": None if command else version,
        "revision": revision,
        "version_strategy": "inherit_agent" if command else "independent",
        "parent_version_ref": parent_version_ref if command else None,
        "content_sha256": content_hash(resolved),
        "locator": locator,
        "visibility": visibility,
        "scope": "agent" if visibility == "private" else public_scope,
        "discoverability": "agent_scoped" if visibility == "private" else "project" if public_scope == "project" else "global",
        "owner_agent_ref": owner_agent_ref,
        "allowed_consumers": sorted(set(allowed_consumers)),
        "accountable_owner": accountable_owner,
        "source_type": "project",
        "provenance": {"repository": "InnovationMachineTeam/skills"},
        "trust_status": "verified",
        "lifecycle_status": "registered",
        "host_compatibility": (
            ["agent-skills", "claude-code", "codex", "cursor"]
            if kind == "skill" and visibility == "public"
            else ["claude-code", "codex", "cursor"] if kind == "agent" else []
        ),
        "eval_evidence": [],
        "replacement": None,
    }


def render_registry(data: dict[str, Any]) -> str:
    lines = [
        "# Agent Asset Registry",
        "",
        "Generated from `AGENT-ASSET-REGISTRY.json`; do not edit manually.",
        "",
        f"Revision: **{data.get('revision', '?')}**",
        f"Updated: **{data.get('updated_at', '?')}**",
        "",
        "| Kind | Name | Version | Visibility | Scope | Owner agent | Accountable owner | Status | Locator |",
        "|---|---|---:|---|---|---|---|---|---|",
    ]
    assets = data.get("assets", [])
    for item in sorted((value for value in assets if isinstance(value, dict)), key=lambda value: (str(value.get("kind")), str(value.get("name")))):
        version = item.get("version") or f"agent revision {item.get('revision', '?')}"
        lines.append(
            f"| {item.get('kind','')} | {item.get('name','')} | {version} | {item.get('visibility','')} | "
            f"{item.get('scope','')} | {item.get('owner_agent_ref') or '—'} | {item.get('accountable_owner','')} | "
            f"{item.get('lifecycle_status','')} | `{item.get('locator','')}` |"
        )
    lines.extend(["", f"Total assets: **{len(assets) if isinstance(assets, list) else 0}**.", ""])
    return "\n".join(lines)


def render_map(data: dict[str, Any]) -> str:
    lines = [
        "# Agent Skills Map",
        "",
        "Generated from `AGENT-SKILLS-MAP.json`; do not edit manually.",
        "",
        f"Revision: **{data.get('revision', '?')}**",
        f"Updated: **{data.get('updated_at', '?')}**",
        "",
        "| Agent | Capability | Mode | Activation | Status | Owner |",
        "|---|---|---|---|---|---|",
    ]
    bindings = data.get("bindings", [])
    for item in sorted((value for value in bindings if isinstance(value, dict)), key=lambda value: str(value.get("id"))):
        lines.append(
            f"| {item.get('agent_ref','')} | {item.get('capability_ref','')} | {item.get('mode','')} | "
            f"{item.get('activation','')} | {item.get('status','')} | {item.get('accountable_owner','')} |"
        )
    lines.extend(["", f"Total bindings: **{len(bindings) if isinstance(bindings, list) else 0}**.", ""])
    return "\n".join(lines)


def validate(
    root: Path, *, check_views: bool = True, require_catalog: bool = True,
    registry_data: dict[str, Any] | None = None, mapping_data: dict[str, Any] | None = None,
) -> list[str]:
    failures: list[str] = []
    try:
        registry = registry_data if registry_data is not None else load_object(root / REGISTRY_PATH)
        mapping = mapping_data if mapping_data is not None else load_object(root / MAP_PATH)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]
    if registry.get("schema_version") != 1 or not isinstance(registry.get("revision"), int):
        failures.append("registry schema_version=1 and integer revision are required")
    assets = registry.get("assets")
    if not isinstance(assets, list):
        return failures + ["registry assets must be an array"]
    by_id: dict[str, dict[str, Any]] = {}
    by_locator: dict[str, dict[str, Any]] = {}
    for index, asset in enumerate(assets):
        label = f"assets[{index}]"
        if not isinstance(asset, dict):
            failures.append(f"{label} must be an object")
            continue
        asset_id = asset.get("id")
        kind = asset.get("kind")
        locator = asset.get("locator")
        if not isinstance(asset_id, str) or not ASSET_ID.fullmatch(asset_id):
            failures.append(f"{label} has invalid id")
            continue
        if asset_id in by_id:
            failures.append(f"duplicate asset id: {asset_id}")
        by_id[asset_id] = asset
        if kind not in KINDS:
            failures.append(f"{asset_id}: invalid kind")
        if not isinstance(asset.get("name"), str) or not NAME.fullmatch(asset["name"]):
            failures.append(f"{asset_id}: invalid name")
        if not safe_locator(locator):
            failures.append(f"{asset_id}: unsafe locator")
            continue
        if locator in by_locator:
            failures.append(f"duplicate asset locator: {locator}")
        by_locator[locator] = asset
        resolved = root / locator
        if not resolved.exists():
            failures.append(f"{asset_id}: missing locator {locator}")
            continue
        expected_hash = asset.get("content_sha256")
        if not isinstance(expected_hash, str) or not SHA.fullmatch(expected_hash):
            failures.append(f"{asset_id}: invalid content_sha256")
        elif content_hash(resolved) != expected_hash:
            failures.append(f"{asset_id}: content hash drift")
        if not isinstance(asset.get("accountable_owner"), str) or not asset["accountable_owner"]:
            failures.append(f"{asset_id}: accountable_owner is required")
        visibility = asset.get("visibility")
        if visibility == "private":
            owner = asset.get("owner_agent_ref")
            consumers = asset.get("allowed_consumers")
            if asset.get("scope") != "agent" or asset.get("discoverability") != "agent_scoped":
                failures.append(f"{asset_id}: private scope/discoverability mismatch")
            if not isinstance(owner, str) or not ASSET_ID.fullmatch(owner):
                failures.append(f"{asset_id}: private owner_agent_ref is required")
            if not isinstance(consumers, list) or owner not in consumers:
                failures.append(f"{asset_id}: allowed_consumers must include owner")
            elif any(consumer != owner for consumer in consumers):
                failures.append(f"{asset_id}: a private capability may only allow its owner agent")
            if isinstance(locator, str) and not private_locator(locator, str(kind)):
                failures.append(f"{asset_id}: private skill/command is outside canonical agent root")
        elif visibility == "public":
            if kind in {"skill", "command"} and isinstance(locator, str) and locator.startswith(".agents/definitions/"):
                failures.append(f"{asset_id}: public asset is inside a private root")
        else:
            failures.append(f"{asset_id}: visibility must be public or private")
        if kind == "command":
            if asset.get("version") is not None or asset.get("version_strategy") != "inherit_agent":
                failures.append(f"{asset_id}: command must inherit agent version")
            if not isinstance(asset.get("revision"), int) or int(asset["revision"]) < 1:
                failures.append(f"{asset_id}: command revision must be positive")
            if not isinstance(asset.get("parent_version_ref"), str):
                failures.append(f"{asset_id}: parent_version_ref is required")
        else:
            if not isinstance(asset.get("version"), str) or not SEMVER.fullmatch(asset["version"]):
                failures.append(f"{asset_id}: independent SemVer is required")
            if asset.get("version_strategy") != "independent":
                failures.append(f"{asset_id}: version_strategy must be independent")
        hosts = asset.get("host_compatibility")
        if not isinstance(hosts, list) or not set(hosts).issubset(HOSTS):
            failures.append(f"{asset_id}: invalid host_compatibility")
    for asset_id, asset in by_id.items():
        if asset.get("visibility") == "private":
            owner = asset.get("owner_agent_ref")
            if owner not in by_id or by_id.get(str(owner), {}).get("kind") != "agent":
                failures.append(f"{asset_id}: owner agent is not registered")
            elif asset.get("kind") == "command":
                expected_parent = f"{owner}@{by_id[str(owner)].get('version')}"
                if asset.get("parent_version_ref") != expected_parent:
                    failures.append(f"{asset_id}: parent_version_ref must be {expected_parent}")
    if require_catalog:
        category_root = root / "skills"
        if category_root.is_dir():
            for skill_file in canonical_skill_files(root):
                locator = skill_file.parent.relative_to(root).as_posix()
                if locator not in by_locator:
                    failures.append(f"unregistered canonical skill: {locator}")
                elif by_locator[locator].get("visibility") != "public":
                    failures.append(f"canonical marketplace skill is not public: {locator}")
    if mapping.get("schema_version") != 1 or not isinstance(mapping.get("revision"), int):
        failures.append("map schema_version=1 and integer revision are required")
    bindings = mapping.get("bindings")
    if not isinstance(bindings, list):
        failures.append("map bindings must be an array")
        bindings = []
    binding_ids: set[str] = set()
    binding_pairs: set[tuple[str, str]] = set()
    bound_by_agent: dict[str, set[str]] = {}
    for index, binding in enumerate(bindings):
        label = f"bindings[{index}]"
        if not isinstance(binding, dict):
            failures.append(f"{label} must be an object")
            continue
        binding_id = binding.get("id")
        if not isinstance(binding_id, str) or not binding_id.startswith("binding://"):
            failures.append(f"{label}: invalid id")
        elif binding_id in binding_ids:
            failures.append(f"duplicate binding id: {binding_id}")
        else:
            binding_ids.add(binding_id)
        agent_id = unversioned(binding.get("agent_ref"))
        capability_id = unversioned(binding.get("capability_ref"))
        if agent_id not in by_id or by_id.get(str(agent_id), {}).get("kind") != "agent":
            failures.append(f"{binding_id}: agent_ref does not resolve")
        capability = by_id.get(str(capability_id))
        if capability is None or capability.get("kind") not in {"skill", "command"}:
            failures.append(f"{binding_id}: capability_ref does not resolve")
        elif capability.get("visibility") == "private" and agent_id not in capability.get("allowed_consumers", []):
            failures.append(f"{binding_id}: unauthorized private capability binding")
        if agent_id in by_id and version_of(binding.get("agent_ref")) != by_id[str(agent_id)].get("version"):
            failures.append(f"{binding_id}: agent_ref version does not match registry")
        if capability is not None:
            expected_version = (
                version_of(capability.get("parent_version_ref"))
                if capability.get("kind") == "command"
                else capability.get("version")
            )
            if version_of(binding.get("capability_ref")) != expected_version:
                failures.append(f"{binding_id}: capability_ref version does not match registry")
        if isinstance(agent_id, str) and isinstance(capability_id, str):
            pair = (agent_id, capability_id)
            if pair in binding_pairs:
                failures.append(f"{binding_id}: duplicate agent/capability binding")
            binding_pairs.add(pair)
            bound_by_agent.setdefault(agent_id, set()).add(str(binding.get("capability_ref")))
    for asset_id, asset in by_id.items():
        if asset.get("visibility") == "private" and not any(
            pair == (asset.get("owner_agent_ref"), asset_id) for pair in binding_pairs
        ):
            failures.append(f"{asset_id}: orphan private capability has no owner binding")
        if asset.get("kind") != "agent":
            continue
        definition_path = root / str(asset.get("locator"))
        try:
            definition = load_object(definition_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append(str(exc))
            continue
        for field in ("id", "name", "version", "accountable_owner"):
            if definition.get(field) != asset.get(field):
                failures.append(f"{asset_id}: definition {field} differs from registry")
        declared: set[str] = set()
        for field in ("public_skill_refs", "private_skill_refs", "private_command_refs"):
            values = definition.get(field)
            if not isinstance(values, list):
                failures.append(f"{asset_id}: definition {field} must be an array")
                continue
            declared.update(value for value in values if isinstance(value, str))
        bound = bound_by_agent.get(asset_id, set())
        if declared != bound:
            failures.append(f"{asset_id}: definition capabilities differ from binding map")
        budgets = definition.get("runtime", {}).get("budgets", {}) if isinstance(definition.get("runtime"), dict) else {}
        maximum = budgets.get("max_capabilities", 12) if isinstance(budgets, dict) else 12
        if not isinstance(maximum, int) or maximum < 0:
            failures.append(f"{asset_id}: max_capabilities must be a non-negative integer")
        elif len(bound) > maximum:
            failures.append(f"{asset_id}: capability budget exceeded ({len(bound)} > {maximum})")
    if check_views:
        expected_views = {
            root / REGISTRY_VIEW: render_registry(registry),
            root / MAP_VIEW: render_map(mapping),
        }
        for path, expected in expected_views.items():
            actual = path.read_text(encoding="utf-8") if path.exists() else ""
            if actual != expected:
                failures.append(f"generated view drift: {path.relative_to(root)}")
    return failures


def sync_public(root: Path, owner: str, write: bool) -> int:
    registry_path = root / REGISTRY_PATH
    registry = load_object(registry_path)
    assets = registry.get("assets")
    if not isinstance(assets, list):
        raise ValueError("registry assets must be an array")
    by_id = {item.get("id"): item for item in assets if isinstance(item, dict)}
    changed = 0
    for skill_file in canonical_skill_files(root):
        locator = skill_file.parent.relative_to(root).as_posix()
        name, _description, _version, error = frontmatter(skill_file.read_text(encoding="utf-8"))
        if error or not name:
            raise ValueError(f"invalid canonical skill: {skill_file}: {error}")
        asset_id = f"asset://repository/skill/{name}"
        previous = by_id.get(asset_id)
        candidate = base_asset(
            root=root, asset_id=asset_id, kind="skill", locator=locator,
            visibility="public", accountable_owner=owner, owner_agent_ref=None,
            allowed_consumers=[], revision=int(previous.get("revision", 0)) + 1 if isinstance(previous, dict) else 1,
        )
        if isinstance(previous, dict):
            candidate["revision"] = previous.get("revision", 1)
            if previous == candidate:
                continue
            if previous.get("content_sha256") != candidate.get("content_sha256") or previous.get("version") != candidate.get("version"):
                candidate["revision"] = int(previous.get("revision", 0)) + 1
        by_id[asset_id] = candidate
        changed += 1
    updated = dict(registry)
    updated["assets"] = sorted(by_id.values(), key=lambda value: str(value.get("id")))
    if changed:
        updated["revision"] = int(registry.get("revision", 0)) + 1
        updated["updated_at"] = now()
    print(json.dumps({"changed": changed, "revision": updated.get("revision"), "write": write}, indent=2))
    if write and changed:
        atomic_json(registry_path, updated)
    return 0


def register_asset(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    registry_path = root / REGISTRY_PATH
    registry = load_object(registry_path)
    assets = registry.get("assets")
    if not isinstance(assets, list):
        raise ValueError("registry assets must be an array")
    previous = next((item for item in assets if isinstance(item, dict) and item.get("id") == args.id), None)
    owner = args.owner_agent_ref
    consumers = args.allowed_consumer or ([] if owner is None else [owner])
    candidate = base_asset(
        root=root, asset_id=args.id, kind=args.kind, locator=args.locator,
        visibility=args.visibility, accountable_owner=args.accountable_owner,
        owner_agent_ref=owner, allowed_consumers=consumers,
        revision=int(previous.get("revision", 0)) + 1 if isinstance(previous, dict) else 1,
        parent_version_ref=args.parent_version_ref,
    )
    updated_assets = [item for item in assets if not isinstance(item, dict) or item.get("id") != args.id]
    updated_assets.append(candidate)
    updated = dict(registry)
    updated["assets"] = sorted(updated_assets, key=lambda value: str(value.get("id")) if isinstance(value, dict) else "")
    updated["revision"] = int(registry.get("revision", 0)) + 1
    updated["updated_at"] = now()
    print(json.dumps(candidate, ensure_ascii=False, indent=2))
    if args.write:
        raise ValueError(
            "direct registry-only writes are disabled; place this preview in an "
            "expected-revision apply-transaction operation"
        )
    return 0


def render(root: Path, write: bool) -> int:
    registry = load_object(root / REGISTRY_PATH)
    mapping = load_object(root / MAP_PATH)
    values = {root / REGISTRY_VIEW: render_registry(registry), root / MAP_VIEW: render_map(mapping)}
    for path, rendered in values.items():
        if write:
            path.write_text(rendered, encoding="utf-8")
        else:
            print(f"--- {path.relative_to(root)}\n{rendered}")
    return 0


def transaction(root: Path, transaction_path: Path, write: bool) -> int:
    operation = load_object(transaction_path)
    if operation.get("schema_version") != 1 or not isinstance(operation.get("id"), str):
        raise ValueError("transaction requires schema_version=1 and id")
    registry_path = root / REGISTRY_PATH
    map_path = root / MAP_PATH
    registry = load_object(registry_path)
    mapping = load_object(map_path)
    expected = operation.get("expected_revisions")
    if not isinstance(expected, dict):
        raise ValueError("transaction expected_revisions object is required")
    if expected.get("registry") != registry.get("revision") or expected.get("map") != mapping.get("revision"):
        raise ValueError(
            f"revision conflict: expected registry/map {expected.get('registry')}/{expected.get('map')}, "
            f"found {registry.get('revision')}/{mapping.get('revision')}"
        )

    def apply_changes(document: dict[str, Any], key: str, identity_key: str) -> dict[str, Any]:
        section = operation.get(key, {})
        if not isinstance(section, dict):
            raise ValueError(f"transaction {key} must be an object")
        upsert = section.get("upsert", [])
        remove = section.get("remove", [])
        if not isinstance(upsert, list) or not isinstance(remove, list) or not all(isinstance(item, str) for item in remove):
            raise ValueError(f"transaction {key} requires upsert[] and remove[]")
        values_key = "assets" if key == "assets" else "bindings"
        current = document.get(values_key)
        if not isinstance(current, list):
            raise ValueError(f"{values_key} must be an array")
        indexed = {
            item.get(identity_key): item
            for item in current
            if isinstance(item, dict) and isinstance(item.get(identity_key), str)
        }
        for item_id in remove:
            indexed.pop(item_id, None)
        for item in upsert:
            if not isinstance(item, dict) or not isinstance(item.get(identity_key), str):
                raise ValueError(f"transaction {key}.upsert entries require {identity_key}")
            indexed[item[identity_key]] = item
        updated = dict(document)
        updated[values_key] = sorted(indexed.values(), key=lambda item: str(item.get(identity_key)))
        updated["revision"] = int(document.get("revision", 0)) + 1
        updated["updated_at"] = now()
        return updated

    candidate_registry = apply_changes(registry, "assets", "id")
    candidate_map = apply_changes(mapping, "bindings", "id")
    failures = validate(
        root, check_views=False, require_catalog=True,
        registry_data=candidate_registry, mapping_data=candidate_map,
    )
    if failures:
        raise ValueError("transaction rejected:\n- " + "\n- ".join(failures))
    result = {
        "transaction": operation["id"],
        "registry_revision": candidate_registry["revision"],
        "map_revision": candidate_map["revision"],
        "write": write,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not write:
        return 0
    snapshots = {
        registry_path: registry_path.read_bytes(),
        map_path: map_path.read_bytes(),
        root / REGISTRY_VIEW: (root / REGISTRY_VIEW).read_bytes() if (root / REGISTRY_VIEW).exists() else None,
        root / MAP_VIEW: (root / MAP_VIEW).read_bytes() if (root / MAP_VIEW).exists() else None,
    }
    try:
        atomic_json(registry_path, candidate_registry)
        atomic_json(map_path, candidate_map)
        (root / REGISTRY_VIEW).write_text(render_registry(candidate_registry), encoding="utf-8")
        (root / MAP_VIEW).write_text(render_map(candidate_map), encoding="utf-8")
    except BaseException:
        for path, payload in snapshots.items():
            if payload is None:
                try:
                    path.unlink()
                except FileNotFoundError:
                    pass
            else:
                path.write_bytes(payload)
        raise
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    validate_parser.add_argument("--no-view-check", action="store_true")
    validate_parser.add_argument("--no-catalog-check", action="store_true")
    sync_parser = sub.add_parser("sync-public")
    sync_parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    sync_parser.add_argument("--accountable-owner", required=True)
    sync_parser.add_argument("--write", action="store_true")
    render_parser = sub.add_parser("render")
    render_parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    render_parser.add_argument("--write", action="store_true")
    register_parser = sub.add_parser("register")
    register_parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    register_parser.add_argument("--id", required=True)
    register_parser.add_argument("--kind", choices=sorted(KINDS), required=True)
    register_parser.add_argument("--locator", required=True)
    register_parser.add_argument("--visibility", choices=("public", "private"), required=True)
    register_parser.add_argument("--accountable-owner", required=True)
    register_parser.add_argument("--owner-agent-ref")
    register_parser.add_argument("--allowed-consumer", action="append")
    register_parser.add_argument("--parent-version-ref")
    register_parser.add_argument("--write", action="store_true")
    transaction_parser = sub.add_parser("apply-transaction")
    transaction_parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    transaction_parser.add_argument("--transaction", type=Path, required=True)
    transaction_parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "validate":
            failures = validate(args.root.resolve(), check_views=not args.no_view_check, require_catalog=not args.no_catalog_check)
            if failures:
                for failure in failures:
                    print(f"FAIL {failure}")
                return 1
            print("PASS agent asset registry, bindings, locators, hashes, visibility and generated views")
            return 0
        if args.command == "sync-public":
            return sync_public(args.root.resolve(), args.accountable_owner, args.write)
        if args.command == "render":
            return render(args.root.resolve(), args.write)
        if args.command == "apply-transaction":
            return transaction(args.root.resolve(), args.transaction.resolve(), args.write)
        return register_asset(args)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
