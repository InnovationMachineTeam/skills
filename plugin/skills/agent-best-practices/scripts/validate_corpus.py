#!/usr/bin/env python3
"""Validate the bundled agent-practices corpus. Read-only; exits nonzero on failure."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    corpus = root / "best-practices"
    failures: list[str] = []
    index = corpus / "README.md"
    if not index.is_file():
        failures.append("missing best-practices/README.md")
    files = sorted(corpus.glob("*.md")) if corpus.is_dir() else []
    if len(files) < 10:
        failures.append("corpus has fewer than 10 thematic/source files")
    names = {path.name for path in files}
    for path in files:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("# "):
            failures.append(f"{path.name}: missing H1")
        for target in re.findall(r"\[[^]]+\]\(([^)#]+\.md)(?:#[^)]+)?\)", text):
            if "://" not in target and Path(target).name not in names:
                failures.append(f"{path.name}: broken local link {target}")
    for required in ("sources-platforms.md", "sources-frameworks.md", "sources-standards-and-docs.md", "sources-patterns-and-cycles.md"):
        if required not in names:
            failures.append(f"missing {required}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    print(f"PASS corpus: {len(files)} Markdown files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
