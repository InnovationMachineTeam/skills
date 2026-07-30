#!/usr/bin/env python3
"""Build a deterministic read-only inventory of explicitly scoped harvest sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path


SKIP_DIRS = {".git", ".svn", ".hg", "node_modules", "__pycache__", ".cache", "dist", "build", "vendor"}
SKIP_FILES = {".DS_Store"}
TEXT_EXTENSIONS = {
    ".md", ".mdx", ".txt", ".rst", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".xml",
    ".csv", ".tsv", ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".sh", ".bash",
    ".zsh", ".fish", ".rb", ".go", ".rs", ".java", ".kt", ".sql", ".html", ".css",
}
DOCUMENT_EXTENSIONS = {".pdf", ".docx", ".odt", ".pptx", ".rtf"}
DELEGATED_EXTENSIONS = {".doc", ".xls", ".xlsx", ".ppt"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def looks_binary(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            chunk = handle.read(8192)
    except OSError:
        return False
    return b"\0" in chunk


def classify(path: Path, relative: Path) -> str:
    parts = {part.lower() for part in relative.parts[:-1]}
    name = path.name.lower()
    if name == "skill.md":
        return "skill-definition"
    if path.suffix.lower() in DOCUMENT_EXTENSIONS:
        return "extractable-document"
    if path.suffix.lower() in DELEGATED_EXTENSIONS:
        return "delegated-document"
    if "evals" in parts or name.startswith(("eval", "test")):
        return "eval-fixture"
    if "prompts" in parts or "prompt" in name:
        return "prompt-template"
    if "references" in parts or "docs" in parts or path.suffix.lower() in {".md", ".mdx", ".rst", ".txt"}:
        return "reference-document"
    if "scripts" in parts or path.suffix.lower() in {".py", ".sh", ".bash", ".zsh", ".js", ".ts", ".rb", ".go", ".rs"}:
        return "script-tool"
    if name in {"openai.yaml", "plugin.json", "package.json", "pyproject.toml"}:
        return "metadata-config"
    return "other"


def inspect_file(path: Path, source: Path, source_index: int, relative: Path, max_bytes: int) -> dict[str, object]:
    try:
        size = path.stat().st_size
    except OSError as exc:
        return {
            "source_index": source_index,
            "source": str(source),
            "path": str(path),
            "relative_path": relative.as_posix(),
            "kind": "unreadable",
            "size_bytes": None,
            "sha256": None,
            "text_candidate": False,
            "document_candidate": False,
            "extractor_hint": None,
            "excluded_reason": f"cannot stat: {exc}",
        }
    excluded = None
    digest = None
    if size > max_bytes:
        excluded = f"file exceeds max bytes ({max_bytes})"
    elif not path.is_file():
        excluded = "not a regular file"
    else:
        try:
            digest = sha256(path)
        except OSError as exc:
            excluded = f"cannot hash: {exc}"
    binary = looks_binary(path) if excluded is None else False
    extension = path.suffix.lower()
    document_candidate = extension in DOCUMENT_EXTENSIONS
    delegated_document = extension in DELEGATED_EXTENSIONS
    extractor_hint = (
        "native-text" if extension in TEXT_EXTENSIONS or path.name == "SKILL.md"
        else extension.lstrip(".") if document_candidate
        else "purpose-built-artifact-tool" if delegated_document
        else None
    )
    if binary and not document_candidate and not delegated_document and excluded is None:
        excluded = "unsupported binary content"
    return {
        "source_index": source_index,
        "source": str(source),
        "path": str(path),
        "relative_path": relative.as_posix(),
        "kind": classify(path, relative),
        "size_bytes": size,
        "sha256": digest,
        "text_candidate": not binary and (extension in TEXT_EXTENSIONS or path.name == "SKILL.md"),
        "document_candidate": document_candidate or delegated_document,
        "extractor_hint": extractor_hint,
        "excluded_reason": excluded,
    }


def walk_source(source: Path, source_index: int, max_depth: int, max_bytes: int) -> list[dict[str, object]]:
    if source.is_file():
        return [inspect_file(source, source, source_index, Path(source.name), max_bytes)]
    records: list[dict[str, object]] = []
    for current, dirnames, filenames in os.walk(source, followlinks=False):
        current_path = Path(current)
        depth = len(current_path.relative_to(source).parts)
        dirnames[:] = sorted(
            name for name in dirnames
            if name not in SKIP_DIRS and not name.startswith(".") and depth < max_depth
        )
        for filename in sorted(filenames):
            if filename in SKIP_FILES or filename.endswith((".pyc", ".pyo")):
                continue
            path = current_path / filename
            relative = path.relative_to(source)
            if path.is_symlink():
                records.append({
                    "source_index": source_index,
                    "source": str(source),
                    "path": str(path),
                    "relative_path": relative.as_posix(),
                    "kind": "symlink",
                    "size_bytes": None,
                    "sha256": None,
                    "text_candidate": False,
                    "document_candidate": False,
                    "extractor_hint": None,
                    "excluded_reason": "symlink not followed",
                })
            else:
                records.append(inspect_file(path, source, source_index, relative, max_bytes))
    return records


def inventory(requested_sources: list[Path], max_depth: int, max_bytes: int) -> dict[str, object]:
    source_records: list[dict[str, object]] = []
    files: list[dict[str, object]] = []
    seen: set[Path] = set()
    home = Path.home().resolve()
    for index, requested in enumerate(requested_sources):
        expanded = requested.expanduser()
        error = None
        if expanded.is_symlink():
            resolved = expanded.resolve()
            error = "source symlink is refused; pass the resolved target explicitly"
        else:
            resolved = expanded.resolve()
            if resolved in {Path("/"), home}:
                error = "broad source is refused; provide a narrower path"
            elif not resolved.exists():
                error = "source does not exist"
            elif not (resolved.is_file() or resolved.is_dir()):
                error = "source is not a regular file or directory"
            elif resolved in seen:
                error = "duplicate resolved source"
        source_records.append({
            "requested": str(requested),
            "resolved": str(resolved),
            "source_index": index,
            "source_kind": "file" if resolved.is_file() else "git-repository" if resolved.is_dir() and (resolved / ".git").exists() else "directory",
            "error": error,
        })
        if error:
            continue
        seen.add(resolved)
        files.extend(walk_source(resolved, index, max_depth, max_bytes))

    files.sort(key=lambda item: (int(item["source_index"]), str(item["relative_path"])))
    by_hash: dict[str, list[str]] = {}
    for item in files:
        digest = item.get("sha256")
        if isinstance(digest, str):
            by_hash.setdefault(digest, []).append(str(item["path"]))
    duplicate_groups = [
        {"sha256": digest, "paths": paths}
        for digest, paths in sorted(by_hash.items()) if len(paths) > 1
    ]
    seed = json.dumps(
        {
            "sources": source_records,
            "files": [{"path": item["path"], "sha256": item["sha256"], "excluded_reason": item["excluded_reason"]} for item in files],
        },
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    return {
        "schema_version": "1.0",
        "inventory_sha256": hashlib.sha256(seed).hexdigest(),
        "max_depth": max_depth,
        "max_file_bytes": max_bytes,
        "sources": source_records,
        "files": files,
        "duplicate_content": duplicate_groups,
        "summary": {
            "sources": len(source_records),
            "source_errors": sum(item["error"] is not None for item in source_records),
            "files": len(files),
            "excluded_files": sum(item["excluded_reason"] is not None for item in files),
            "duplicate_groups": len(duplicate_groups),
        },
        "scope_note": "This inventory hashes files without executing source content and does not establish authority, license, safety, or reuse readiness.",
    }


def render_text(payload: dict[str, object]) -> str:
    summary = payload["summary"]
    assert isinstance(summary, dict)
    lines = [
        f"Inventory: {payload['inventory_sha256']}",
        f"Sources: {summary['sources']} ({summary['source_errors']} errors)",
        f"Files: {summary['files']} ({summary['excluded_files']} excluded)",
        f"Duplicate content groups: {summary['duplicate_groups']}",
    ]
    for item in payload["files"]:
        assert isinstance(item, dict)
        suffix = f" — excluded: {item['excluded_reason']}" if item["excluded_reason"] else ""
        lines.append(f"- {item['kind']}: {item['path']}{suffix}")
    lines.append(str(payload["scope_note"]))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", type=Path)
    parser.add_argument("--max-depth", type=int, default=4)
    parser.add_argument("--max-file-bytes", type=int, default=5 * 1024 * 1024)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()
    if not 0 <= args.max_depth <= 12:
        print("Error: --max-depth must be between 0 and 12", file=sys.stderr)
        return 2
    if not 1024 <= args.max_file_bytes <= 1024 * 1024 * 1024:
        print("Error: --max-file-bytes must be between 1024 and 1073741824", file=sys.stderr)
        return 2
    payload = inventory(args.sources, args.max_depth, args.max_file_bytes)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_text(payload)
    if args.output:
        output = args.output.expanduser().resolve()
        if not output.parent.is_dir():
            print(f"Error: output directory does not exist: {output.parent}", file=sys.stderr)
            return 2
        output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Inventory written to {output}", file=sys.stderr)
    else:
        print(rendered)
    summary = payload["summary"]
    assert isinstance(summary, dict)
    return 1 if args.fail_on_error and summary["source_errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
