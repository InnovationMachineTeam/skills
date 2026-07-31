#!/usr/bin/env python3
"""Validate curated Markdown knowledge and build a deterministic JSON graph."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REQUIRED = {"id", "type", "status", "owner", "version", "updated_at", "review_at", "sources", "related", "tags", "sensitivity", "agent_access"}
STATUSES = {"candidate", "approved", "stale", "revoked", "superseded", "archived"}
TYPES = {"fact", "interpretation", "decision", "conflict", "incident", "learning", "runbook", "evidence", "concept", "source", "map"}
SENSITIVITY = {"public", "internal", "confidential", "restricted"}
ACCESS = {"none", "read", "propose", "curate"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")


def scalar(value: str) -> object:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip('"\'') for item in inner.split(",")]
    return value.strip('"\'')


def frontmatter(path: Path) -> tuple[dict[str, object], str]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n") or "\n---\n" not in content[4:]:
        raise ValueError("missing YAML frontmatter")
    raw, body = content[4:].split("\n---\n", 1)
    data: dict[str, object] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) or ":" not in line:
            raise ValueError(f"unsupported frontmatter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = scalar(value)
    return data, body


def build(root: Path, generated_at: str) -> tuple[dict, list[str]]:
    failures: list[str] = []
    nodes: list[dict] = []
    edges: list[dict] = []
    ids: set[str] = set()
    documents: list[tuple[Path, dict[str, object], str]] = []
    for path in sorted(root.rglob("*.md")):
        if path.name == "README.md":
            continue
        try:
            metadata, body = frontmatter(path)
        except (OSError, ValueError) as exc:
            failures.append(f"{path}: {exc}")
            continue
        missing = sorted(REQUIRED - set(metadata))
        if missing:
            failures.append(f"{path}: missing metadata {missing}")
            continue
        doc_id = metadata.get("id")
        if not isinstance(doc_id, str) or not doc_id.startswith("doc://") or doc_id in ids:
            failures.append(f"{path}: id must be unique and start with doc://")
            continue
        ids.add(doc_id)
        if metadata.get("status") not in STATUSES:
            failures.append(f"{path}: invalid status")
        if metadata.get("type") not in TYPES:
            failures.append(f"{path}: invalid type")
        if metadata.get("sensitivity") not in SENSITIVITY or metadata.get("agent_access") not in ACCESS:
            failures.append(f"{path}: invalid sensitivity or agent_access")
        if not isinstance(metadata.get("version"), str) or not SEMVER.fullmatch(str(metadata["version"])):
            failures.append(f"{path}: invalid SemVer")
        for key in ("sources", "related", "tags"):
            if not isinstance(metadata.get(key), list):
                failures.append(f"{path}: {key} must be an inline array")
        if metadata.get("status") == "approved" and not metadata.get("sources"):
            failures.append(f"{path}: approved knowledge requires provenance sources")
        documents.append((path, metadata, body))
    for path, metadata, body in documents:
        doc_id = str(metadata["id"])
        digest = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        locator = path.relative_to(root.parent.parent if root.name == "knowledge" and root.parent.name == "docs" else root.parent).as_posix()
        nodes.append({
            "id": doc_id,
            "type": metadata["type"],
            "status": metadata["status"],
            "version": metadata["version"],
            "owner": metadata["owner"],
            "updated_at": metadata["updated_at"],
            "sensitivity": metadata["sensitivity"],
            "agent_access": metadata["agent_access"],
            "tags": metadata["tags"],
            "locator": locator,
            "content_sha256": digest,
            "summary": next((line.lstrip("# ").strip() for line in body.splitlines() if line.strip()), ""),
        })
        for target in metadata["related"]:
            if target not in ids:
                failures.append(f"{path}: unresolved related id {target}")
            edges.append({"type": "RELATED_TO", "from": doc_id, "to": target, "source_locator": locator, "source_sha256": digest})
        for target in metadata["sources"]:
            edges.append({"type": "DERIVED_FROM", "from": doc_id, "to": target, "source_locator": locator, "source_sha256": digest})
        if isinstance(metadata.get("supersedes"), str) and metadata["supersedes"]:
            edges.append({"type": "SUPERSEDES", "from": doc_id, "to": metadata["supersedes"], "source_locator": locator, "source_sha256": digest})
    graph = {"schema_version": 1, "generated_at": generated_at, "source_root": root.as_posix(), "nodes": sorted(nodes, key=lambda item: item["id"]), "edges": sorted(edges, key=lambda item: (item["from"], item["type"], item["to"]))}
    return graph, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--generated-at", required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    graph, failures = build(args.root, args.generated_at)
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        return 1
    rendered = json.dumps(graph, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        if args.check:
            current = args.output.read_text(encoding="utf-8") if args.output.exists() else ""
            if current != rendered:
                print(f"FAIL projection drift: {args.output}")
                return 1
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
    print(f"PASS knowledge graph: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges")
    return 0


if __name__ == "__main__":
    sys.exit(main())
