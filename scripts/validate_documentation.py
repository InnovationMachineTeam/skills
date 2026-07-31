#!/usr/bin/env python3
"""Validate local links in canonical repository documentation."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
EXTERNAL_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:")


def documentation_files(root: Path) -> list[Path]:
    files = list(root.glob("*.md"))
    files.extend((root / "docs").rglob("*.md"))
    files.extend((root / "skills").glob("*.md"))
    files.extend((root / "skills").glob("*/README.md"))
    files.extend((root / "catalog").glob("*.md"))
    files.extend((root / "scripts").glob("*.md"))
    files.extend((root / ".agents").glob("*.md"))
    files.append(root / "plugins" / "README.md")
    return sorted({path for path in files if path.is_file()})


def link_target(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        value = value[1 : value.index(">")]
    elif " " in value:
        value = value.split(" ", 1)[0]
    return unquote(value.split("#", 1)[0])


def validate(root: Path) -> list[str]:
    root = root.resolve()
    failures: list[str] = []
    for document in documentation_files(root):
        text = document.read_text(encoding="utf-8")
        for match in LINK.finditer(text):
            raw = match.group(1).strip()
            if not raw or raw.startswith("#") or raw.startswith(EXTERNAL_SCHEMES):
                continue
            target = link_target(raw)
            if not target:
                continue
            resolved = (document.parent / target).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                failures.append(
                    f"{document.relative_to(root)}: local link escapes repository: {raw}"
                )
                continue
            if not resolved.exists():
                failures.append(
                    f"{document.relative_to(root)}: missing local link target: {raw}"
                )
    return failures


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    failures = validate(root)
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print(f"PASS documentation links: {len(documentation_files(root))} canonical files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
