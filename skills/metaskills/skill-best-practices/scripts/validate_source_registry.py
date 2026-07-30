#!/usr/bin/env python3
"""Validate the skill-best-practices source registry."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any


ID_PATTERN = re.compile(r"^SRC-[A-Z]+-\d{3}$")
REQUIRED = {
    "id",
    "title",
    "locator",
    "publisher",
    "category",
    "authority_tier",
    "scope",
    "source_type",
    "update_method",
    "status",
    "last_checked",
    "summary_file",
    "principal_findings",
}
STATUSES = {"available", "unavailable", "partial", "moved", "unknown"}


@dataclass
class Finding:
    code: str
    message: str
    path: str


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [Finding("json", f"cannot read valid JSON: {exc}", str(path))]
    if not isinstance(value, dict):
        return [Finding("root", "registry root must be an object", "$")]
    if value.get("schema_version") != 1:
        findings.append(Finding("schema", "schema_version must equal 1", "$.schema_version"))
    sources = value.get("sources")
    if not isinstance(sources, list) or not sources:
        findings.append(Finding("sources", "sources must be a non-empty array", "$.sources"))
        return findings

    ids: set[str] = set()
    locators: set[str] = set()
    for index, source in enumerate(sources):
        base = f"$.sources[{index}]"
        if not isinstance(source, dict):
            findings.append(Finding("source", "source must be an object", base))
            continue
        missing = REQUIRED - set(source)
        if missing:
            findings.append(Finding("fields", "missing fields: " + ", ".join(sorted(missing)), base))
        source_id = source.get("id")
        if not isinstance(source_id, str) or not ID_PATTERN.fullmatch(source_id):
            findings.append(Finding("id", "source id must match SRC-GROUP-000", f"{base}.id"))
        elif source_id in ids:
            findings.append(Finding("id", f"duplicate source id: {source_id}", f"{base}.id"))
        else:
            ids.add(source_id)
        locator = source.get("locator")
        if not nonempty(locator):
            findings.append(Finding("locator", "locator must be a non-empty string", f"{base}.locator"))
        elif locator in locators:
            findings.append(Finding("locator", f"duplicate locator: {locator}", f"{base}.locator"))
        else:
            locators.add(locator)
        for key in ("title", "publisher", "category", "scope", "source_type", "update_method"):
            if not nonempty(source.get(key)):
                findings.append(Finding("field", f"{key} must be a non-empty string", f"{base}.{key}"))
        tier = source.get("authority_tier")
        if not isinstance(tier, int) or not 1 <= tier <= 6:
            findings.append(Finding("authority", "authority_tier must be an integer from 1 to 6", f"{base}.authority_tier"))
        if source.get("status") not in STATUSES:
            findings.append(Finding("status", "unknown source status", f"{base}.status"))
        try:
            date.fromisoformat(str(source.get("last_checked")))
        except ValueError:
            findings.append(Finding("date", "last_checked must be YYYY-MM-DD", f"{base}.last_checked"))
        summary = source.get("summary_file")
        if not nonempty(summary) or Path(summary).name != summary or not summary.endswith(".md"):
            findings.append(Finding("summary", "summary_file must name a Markdown file in sources/", f"{base}.summary_file"))
        elif not (path.parent / summary).is_file():
            findings.append(Finding("summary", f"missing summary file: {summary}", f"{base}.summary_file"))
        principal = source.get("principal_findings")
        if not isinstance(principal, list) or not principal or not all(nonempty(item) for item in principal):
            findings.append(Finding("principal-findings", "principal_findings must be a non-empty string array", f"{base}.principal_findings"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    findings = validate(args.registry.expanduser().resolve())
    if args.format == "json":
        print(json.dumps({"valid": not findings, "count": len(findings), "findings": [asdict(item) for item in findings]}, ensure_ascii=False, indent=2))
    else:
        print(f"Findings: {len(findings)}")
        for finding in findings:
            print(f"[ERROR] {finding.code}: {finding.message} ({finding.path})")
        if not findings:
            print("Source registry is structurally valid.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
