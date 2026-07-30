#!/usr/bin/env python3
"""Generate the managed-skill modification prompt from registry and template."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path


REVISION_PATTERN = re.compile(r"^Revision:\s*(.+)$", re.MULTILINE)
HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
RETRIEVAL_STATUSES = {"available", "unavailable", "partial", "moved"}


def valid_time(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def valid_snapshot(snapshot: object) -> bool:
    if not isinstance(snapshot, dict) or snapshot.get("schema_version") != 1 or not valid_time(snapshot.get("created_at")):
        return False
    if not HASH_PATTERN.fullmatch(snapshot.get("registry_hash", "")) or not isinstance(snapshot.get("sources"), list):
        return False
    seen_ids: set[str] = set()
    for item in snapshot["sources"]:
        if not isinstance(item, dict) or not isinstance(item.get("source_id"), str) or not item["source_id"]:
            return False
        if item["source_id"] in seen_ids:
            return False
        seen_ids.add(item["source_id"])
        if item.get("status") not in RETRIEVAL_STATUSES or not valid_time(item.get("checked_at")):
            return False
        if not isinstance(item.get("canonical_locator"), str) or not item["canonical_locator"]:
            return False
        if not isinstance(item.get("claims"), list) or not isinstance(item.get("errors"), list) or not isinstance(item.get("coverage_notes"), str):
            return False
        fingerprint = item.get("semantic_fingerprint")
        if item["status"] in {"available", "moved"} and not HASH_PATTERN.fullmatch(fingerprint or ""):
            return False
        if fingerprint is not None and not HASH_PATTERN.fullmatch(fingerprint):
            return False
    return True


def file_hash(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def corpus_hash(practices_path: Path, claims_path: Path) -> str:
    digest = hashlib.sha256()
    paths = sorted(practices_path.parent.glob("*.md"), key=lambda item: item.name) + [claims_path]
    for path in sorted(paths, key=lambda item: item.name):
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return "sha256:" + digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills", type=Path, required=True)
    parser.add_argument("--practices", type=Path, required=True)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--claims", type=Path, required=True)
    parser.add_argument("--reconciliation", type=Path, required=True)
    parser.add_argument("--validation", type=Path, required=True)
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    skills_path = args.skills.expanduser().resolve()
    practices_path = args.practices.expanduser().resolve()
    registry_path = args.registry.expanduser().resolve()
    snapshot_path = args.snapshot.expanduser().resolve()
    claims_path = args.claims.expanduser().resolve()
    reconciliation_path = args.reconciliation.expanduser().resolve()
    validation_path = args.validation.expanduser().resolve()
    template_path = args.template.expanduser().resolve()
    output_path = args.output.expanduser().resolve()
    input_paths = {skills_path, practices_path, registry_path, snapshot_path, claims_path, reconciliation_path, validation_path, template_path}
    if output_path in input_paths:
        print("Output must not overwrite an input.", file=sys.stderr)
        return 1
    if output_path.exists() and not args.force:
        print(f"Output exists; pass --force to replace it: {output_path}", file=sys.stderr)
        return 1
    try:
        registry = json.loads(skills_path.read_text(encoding="utf-8"))
        skills = registry["skills"]
        practices_text = practices_path.read_text(encoding="utf-8")
        source_registry = json.loads(registry_path.read_text(encoding="utf-8"))
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        claims = json.loads(claims_path.read_text(encoding="utf-8"))
        reconciliation = json.loads(reconciliation_path.read_text(encoding="utf-8"))
        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        template = template_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError) as exc:
        print(f"Cannot read inputs: {exc}", file=sys.stderr)
        return 1
    if not isinstance(skills, list) or not skills:
        print("Managed skills must be a non-empty array.", file=sys.stderr)
        return 1
    names: set[str] = set()
    lines: list[str] = []
    for index, skill in enumerate(skills):
        if not isinstance(skill, dict):
            print(f"Managed skill {index} must be an object.", file=sys.stderr)
            return 1
        required = ("name", "role", "source_hint", "risk", "default_action")
        if not all(isinstance(skill.get(key), str) and skill[key].strip() for key in required):
            print(f"Managed skill {index} is missing required string fields.", file=sys.stderr)
            return 1
        if skill["name"] in names:
            print(f"Duplicate managed skill: {skill['name']}", file=sys.stderr)
            return 1
        names.add(skill["name"])
        note = f" {skill['notes']}" if isinstance(skill.get("notes"), str) and skill["notes"].strip() else ""
        lines.append(
            f"  - `{skill['name']}` — {skill['role']}; source hint `{skill['source_hint']}`; "
            f"risk `{skill['risk']}`; default `{skill['default_action']}`.{note}"
        )
    match = REVISION_PATTERN.search("\n".join(practices_text.splitlines()[:20]))
    if not match:
        print("Practice index does not declare Revision.", file=sys.stderr)
        return 1
    revision = match.group(1).strip()
    expected_corpus_hash = corpus_hash(practices_path, claims_path)
    expected_registry_hash = file_hash(registry_path)
    expected_snapshot_hash = file_hash(snapshot_path)
    snapshot_id = snapshot.get("snapshot_id")
    reconciliation_id = reconciliation.get("reconciliation_id")
    registry_source_ids = {item.get("id") for item in source_registry.get("sources", []) if isinstance(item, dict)}
    snapshot_source_ids = {item.get("source_id") for item in snapshot.get("sources", []) if isinstance(item, dict)}
    if registry.get("practices_revision") != revision:
        print("Managed-skill registry revision does not match practice index.", file=sys.stderr)
        return 1
    if claims.get("practices_revision") != revision:
        print("Claims manifest revision does not match practice index.", file=sys.stderr)
        return 1
    if validation.get("valid") is not True or validation.get("practices_revision") != revision:
        print("A passing validation artifact for this revision is required.", file=sys.stderr)
        return 1
    if validation.get("corpus_hash") != expected_corpus_hash or validation.get("registry_hash") != expected_registry_hash:
        print("Validation artifact is stale for the current corpus or source registry.", file=sys.stderr)
        return 1
    if not valid_snapshot(snapshot) or not isinstance(snapshot_id, str) or not snapshot_id:
        print("Snapshot does not satisfy the strict snapshot schema.", file=sys.stderr)
        return 1
    if snapshot.get("registry_hash") != expected_registry_hash:
        print("Snapshot registry hash does not match the source registry.", file=sys.stderr)
        return 1
    if not registry_source_ids or registry_source_ids != snapshot_source_ids:
        print("Snapshot source coverage does not match the source registry.", file=sys.stderr)
        return 1
    if reconciliation.get("snapshot_id") != snapshot_id or reconciliation.get("practices_revision") != revision:
        print("Reconciliation artifact is not bound to the snapshot and practice revision.", file=sys.stderr)
        return 1
    if reconciliation.get("snapshot_hash") != expected_snapshot_hash or reconciliation.get("registry_hash") != expected_registry_hash:
        print("Reconciliation artifact is stale for the snapshot or source registry.", file=sys.stderr)
        return 1
    if not isinstance(reconciliation_id, str) or not reconciliation_id:
        print("Reconciliation artifact must declare reconciliation_id.", file=sys.stderr)
        return 1
    conflicts = reconciliation.get("unresolved_conflicts")
    unverified = reconciliation.get("unverified_sources")
    if not isinstance(conflicts, list) or not isinstance(unverified, list) or not all(isinstance(item, str) for item in unverified):
        print("Reconciliation must declare unresolved_conflicts and unverified_sources arrays.", file=sys.stderr)
        return 1
    unavailable_ids = sorted(
        item.get("source_id") for item in snapshot.get("sources", [])
        if isinstance(item, dict) and item.get("status") in {"unavailable", "partial"}
    )
    if sorted(unverified) != unavailable_ids:
        print("Reconciliation unverified_sources does not match unavailable or partial snapshot sources.", file=sys.stderr)
        return 1
    unresolved_status = f"conflicts={len(conflicts)}, unverified_sources={len(unverified)}"
    rendered = template.replace("{{PRACTICES_INDEX}}", str(args.practices))
    rendered = rendered.replace("{{PRACTICES_REVISION}}", revision)
    rendered = rendered.replace("{{REGISTRY_HASH}}", expected_registry_hash)
    rendered = rendered.replace("{{SNAPSHOT_ID}}", snapshot_id)
    rendered = rendered.replace("{{SNAPSHOT_HASH}}", expected_snapshot_hash)
    rendered = rendered.replace("{{RECONCILIATION_ID}}", reconciliation_id)
    rendered = rendered.replace("{{CORPUS_HASH}}", expected_corpus_hash)
    rendered = rendered.replace("{{UNRESOLVED_STATUS}}", unresolved_status)
    rendered = rendered.replace("{{MANAGED_SKILLS}}", "\n".join(lines))
    if "{{" in rendered or "}}" in rendered:
        print("Unresolved template placeholder remains.", file=sys.stderr)
        return 1
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=output_path.name + ".", dir=output_path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(rendered.rstrip() + "\n")
        os.replace(temp_name, output_path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    print(f"Generated prompt for {len(skills)} managed skills: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
