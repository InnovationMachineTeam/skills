#!/usr/bin/env python3
"""Validate skill-best-practices routing and behavior eval datasets."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROUTES = {"query-practices", "source-audit", "refresh-sources", "reconcile-practices", "rebuild-practices", "generate-modification-prompt", "apply-practices", "full-refresh"}


@dataclass
class Finding:
    code: str
    message: str
    path: str


def load(path: Path, findings: list[Finding]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        findings.append(Finding("json", f"cannot read valid JSON: {exc}", str(path)))
        return None
    if not isinstance(value, dict) or value.get("skill") != "skill-best-practices":
        findings.append(Finding("shape", "eval root must identify skill-best-practices", str(path)))
        return None
    return value


def cases(value: dict[str, Any], path: Path, findings: list[Finding]) -> list[dict[str, Any]]:
    raw = value.get("cases")
    if not isinstance(raw, list) or not raw:
        findings.append(Finding("cases", "cases must be a non-empty array", str(path)))
        return []
    result: list[dict[str, Any]] = []
    ids: set[str] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            findings.append(Finding("case", f"case {index} must be an object", str(path)))
            continue
        case_id = item.get("id")
        if not isinstance(case_id, str) or not case_id or case_id in ids:
            findings.append(Finding("case-id", f"case {index} needs a unique id", str(path)))
        else:
            ids.add(case_id)
        result.append(item)
    return result


def validate(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    routing_path = root / "routing.json"
    routing = load(routing_path, findings)
    if routing:
        items = cases(routing, routing_path, findings)
        covered = {item.get("expected_route") for item in items if item.get("expected_route")}
        for item in items:
            if isinstance(item.get("expected_routes"), list):
                covered.update(route for route in item["expected_routes"] if isinstance(route, str))
        missing = ROUTES - covered
        if missing:
            findings.append(Finding("route-coverage", "missing routes: " + ", ".join(sorted(missing)), str(routing_path)))
        actions = {item.get("expected_action") for item in items}
        for action in ("route", "clarify", "do-not-trigger"):
            if action not in actions:
                findings.append(Finding("action-coverage", f"missing action: {action}", str(routing_path)))
        if not {True, False}.issubset({item.get("expected_trigger") for item in items}):
            findings.append(Finding("trigger-coverage", "include positive and negative triggers", str(routing_path)))
    behavior_path = root / "behavior.json"
    behavior = load(behavior_path, findings)
    if behavior:
        for item in cases(behavior, behavior_path, findings):
            for key in ("expected_properties", "forbidden_properties"):
                if not isinstance(item.get(key), list) or not item[key]:
                    findings.append(Finding("behavior", f"case {item.get('id', '?')} requires {key}", str(behavior_path)))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("eval_dir", type=Path, nargs="?", default=Path("evals"))
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    findings = validate(args.eval_dir.expanduser().resolve())
    if args.format == "json":
        print(json.dumps({"count": len(findings), "findings": [asdict(item) for item in findings]}, ensure_ascii=False, indent=2))
    else:
        print(f"Findings: {len(findings)}")
        for finding in findings:
            print(f"[ERROR] {finding.code}: {finding.message} ({finding.path})")
        if not findings:
            print("Routing and behavior eval datasets are structurally complete.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
