#!/usr/bin/env python3
"""Classify hard modal rules and context size in canonical SKILL.md files.

The command is read-only. It prints a human summary or stable JSON and exits 0
when the supplied root exists, even when review candidates are present.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


MODAL = re.compile(r"\b(must(?:\s+not)?|never|always|do\s+not|require[ds]?|reject(?:ed|s)?|stop|cannot)\b", re.IGNORECASE)

AUTHORITY = re.compile(
    r"\b(authority|permission|approval|credential|secret|private key|publish|deploy|production|delete|destructive|recipient|data boundary|confidential|spend|install|activate|retire)\b",
    re.IGNORECASE,
)
VERIFICATION = re.compile(
    r"\b(verify|validation|evidence|complete|completion|rollback|recover|retry|holdout|baseline|regression|partial|failure|false completion)\b",
    re.IGNORECASE,
)
INTERFACE = re.compile(
    r"\b(schema|state|hash|idempotent|exit code|enum|contract|version|identifier|field|json|frontmatter)\b",
    re.IGNORECASE,
)


def classify_line(line: str) -> str | None:
    if not MODAL.search(line):
        return None
    if AUTHORITY.search(line):
        return "authority_safety"
    if VERIFICATION.search(line):
        return "verification_recovery"
    if INTERFACE.search(line):
        return "deterministic_interface"
    return "judgment_candidate"


def audit(root: Path) -> dict:
    files = sorted(root.rglob("SKILL.md"))
    records = []
    totals: Counter[str] = Counter()
    words = 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        words += len(text.split())
        for number, line in enumerate(text.splitlines(), 1):
            category = classify_line(line)
            if category is None:
                continue
            totals[category] += 1
            records.append(
                {
                    "path": path.relative_to(root).as_posix(),
                    "line": number,
                    "category": category,
                    "text": line.strip(),
                }
            )
    return {
        "schema_version": 1,
        "root": str(root.resolve()),
        "skill_files": len(files),
        "skill_words": words,
        "hard_rules": len(records),
        "counts": dict(sorted(totals.items())),
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"root is not a directory: {root}")
    report = audit(root)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Skills: {report['skill_files']}")
        print(f"SKILL.md words: {report['skill_words']}")
        print(f"Hard rules: {report['hard_rules']}")
        for category, count in report["counts"].items():
            print(f"{category}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
