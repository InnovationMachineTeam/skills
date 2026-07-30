#!/usr/bin/env python3
"""Extract text from explicit files into a separate destination without executing source content."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree


TEXT_EXTENSIONS = {".md", ".mdx", ".txt", ".rst", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".xml", ".csv", ".tsv", ".log", ".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".sql", ".css"}
SUPPORTED = TEXT_EXTENSIONS | {".html", ".htm", ".rtf", ".docx", ".odt", ".pptx", ".pdf"}
SKIP_DIRS = {".git", ".svn", ".hg", "node_modules", "__pycache__", ".cache", "dist", "build", "vendor"}


class TextHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.parts.append(data.strip())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def discover(source: Path, max_depth: int) -> list[Path]:
    if source.is_file():
        return [source]
    result: list[Path] = []
    for current, dirnames, filenames in os.walk(source, followlinks=False):
        current_path = Path(current)
        depth = len(current_path.relative_to(source).parts)
        dirnames[:] = sorted(name for name in dirnames if name not in SKIP_DIRS and not name.startswith(".") and depth < max_depth)
        for filename in sorted(filenames):
            path = current_path / filename
            if not path.is_symlink() and path.suffix.lower() in SUPPORTED:
                result.append(path)
    return result


def zip_xml_text(path: Path, selectors: tuple[str, ...]) -> str:
    parts: list[str] = []
    with zipfile.ZipFile(path) as archive:
        names = sorted(name for name in archive.namelist() if any(name == selector or name.startswith(selector) for selector in selectors))
        for name in names:
            try:
                root = ElementTree.fromstring(archive.read(name))
            except (KeyError, ElementTree.ParseError):
                continue
            values = [element.text for element in root.iter() if element.text and element.text.strip()]
            if values:
                parts.append(f"[{name}]\n" + "\n".join(value.strip() for value in values))
    return "\n\n".join(parts)


def pdf_text(path: Path) -> tuple[str, str]:
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        pages = [f"[page {index}]\n{page.extract_text() or ''}" for index, page in enumerate(reader.pages, start=1)]
        return "\n\n".join(pages), "pypdf"
    except ImportError:
        pass
    tool = shutil.which("pdftotext")
    if tool:
        result = subprocess.run([tool, str(path), "-"], check=False, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            return result.stdout, "pdftotext"
        raise RuntimeError(result.stderr.strip() or f"pdftotext exited {result.returncode}")
    raise RuntimeError("PDF extractor unavailable; use a purpose-built PDF tool, pypdf, or pdftotext")


def extract(path: Path) -> tuple[str, str]:
    extension = path.suffix.lower()
    if extension in TEXT_EXTENSIONS:
        return path.read_text(encoding="utf-8", errors="replace"), "utf8-text"
    if extension in {".html", ".htm"}:
        parser = TextHTMLParser()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        return "\n".join(parser.parts), "html-parser"
    if extension == ".rtf":
        raw = path.read_text(encoding="utf-8", errors="replace")
        value = re.sub(r"\\'[0-9a-fA-F]{2}", " ", raw)
        value = re.sub(r"\\[a-zA-Z]+-?\d* ?", " ", value)
        value = re.sub(r"[{}]", " ", value)
        return re.sub(r"\s+", " ", value).strip(), "basic-rtf"
    if extension == ".docx":
        return zip_xml_text(path, ("word/document.xml", "word/header", "word/footer", "word/footnotes.xml", "word/endnotes.xml")), "docx-xml"
    if extension == ".odt":
        return zip_xml_text(path, ("content.xml",)), "odt-xml"
    if extension == ".pptx":
        return zip_xml_text(path, ("ppt/slides/slide", "ppt/notesSlides/notesSlide")), "pptx-xml"
    if extension == ".pdf":
        return pdf_text(path)
    raise RuntimeError(f"unsupported extension: {extension}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--max-depth", type=int, default=4)
    parser.add_argument("--max-file-bytes", type=int, default=50 * 1024 * 1024)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    if not 0 <= args.max_depth <= 12:
        print("Error: --max-depth must be between 0 and 12", file=sys.stderr)
        return 2
    home = Path.home().resolve()
    roots: list[Path] = []
    for requested in args.sources:
        expanded = requested.expanduser()
        resolved = expanded.resolve()
        if expanded.is_symlink() or resolved in {Path("/"), home} or not resolved.exists():
            print(f"Error: unsafe or missing source: {requested}", file=sys.stderr)
            return 2
        roots.append(resolved)
    output_dir = args.output_dir.expanduser().resolve()
    manifest = args.manifest.expanduser().resolve()
    for root in roots:
        parent = root if root.is_dir() else root.parent
        if inside(output_dir, parent) or inside(manifest, parent):
            print(f"Error: output and manifest must be outside source tree: {parent}", file=sys.stderr)
            return 2
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    for source_index, root in enumerate(roots):
        for path in discover(root, args.max_depth):
            relative = Path(path.name) if root.is_file() else path.relative_to(root)
            record: dict[str, object] = {
                "source_index": source_index,
                "source_root": str(root),
                "path": str(path),
                "relative_path": relative.as_posix(),
                "sha256": sha256(path),
                "size_bytes": path.stat().st_size,
                "status": "pending",
                "extractor": None,
                "output": None,
                "error": None,
            }
            if path.stat().st_size > args.max_file_bytes:
                record["status"] = "excluded"
                record["error"] = f"file exceeds max bytes ({args.max_file_bytes})"
                records.append(record)
                continue
            name = re.sub(r"[^A-Za-z0-9._-]+", "_", relative.as_posix()).strip("_") or "source"
            destination = output_dir / f"s{source_index}-{record['sha256'][:12]}-{name}.txt"
            try:
                if destination.exists() and not args.overwrite:
                    raise RuntimeError(f"destination exists: {destination}")
                value, extractor_name = extract(path)
                destination.write_text(value.rstrip() + "\n", encoding="utf-8")
                record.update({"status": "extracted", "extractor": extractor_name, "output": str(destination)})
            except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
                record.update({"status": "failed", "error": str(exc)})
            records.append(record)
    payload = {
        "schema_version": "1.0",
        "sources": [str(root) for root in roots],
        "output_dir": str(output_dir),
        "records": records,
        "summary": {
            "files": len(records),
            "extracted": sum(item["status"] == "extracted" for item in records),
            "failed": sum(item["status"] == "failed" for item in records),
            "excluded": sum(item["status"] == "excluded" for item in records),
        },
        "scope_note": "Extracted text is an analysis aid and does not preserve all layout, images, formulas, comments, or document semantics.",
    }
    manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False))
    return 1 if payload["summary"]["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
