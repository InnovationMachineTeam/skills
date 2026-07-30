#!/usr/bin/env python3
"""Validate the routing and behavior eval datasets for skill-optimizer."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


ROUTES = {
    "routing-discovery",
    "context-architecture",
    "workflow-reliability",
    "scripts-tools",
    "safety-authority",
    "evaluation-regression",
    "portability-packaging",
    "performance-cost",
}


@dataclass
class Finding:
    code: str
    message: str
    path: str


def load(path: Path, findings: list[Finding]) -> dict[str, object] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        findings.append(Finding("json", f"Cannot read valid JSON: {exc}", str(path)))
        return None
    if not isinstance(payload, dict):
        findings.append(Finding("shape", "Eval root must be an object.", str(path)))
        return None
    if payload.get("skill") != "skill-optimizer":
        findings.append(
            Finding("skill", "Eval must identify skill-optimizer.", str(path))
        )
    return payload


def cases(payload: dict[str, object], path: Path, findings: list[Finding]) -> list[dict[str, object]]:
    value = payload.get("cases")
    if not isinstance(value, list) or not value:
        findings.append(Finding("cases", "cases must be a non-empty array.", str(path)))
        return []
    output: list[dict[str, object]] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            findings.append(
                Finding("case-shape", f"Case {index} must be an object.", str(path))
            )
            continue
        case_id = item.get("id")
        if not isinstance(case_id, str) or not case_id:
            findings.append(
                Finding("case-id", f"Case {index} requires a string id.", str(path))
            )
        elif case_id in seen:
            findings.append(
                Finding("case-id", f"Duplicate case id: {case_id}", str(path))
            )
        else:
            seen.add(case_id)
        output.append(item)
    return output


def validate_routing(path: Path, findings: list[Finding]) -> None:
    payload = load(path, findings)
    if payload is None:
        return
    values = cases(payload, path, findings)
    routes = {item.get("expected_primary_route") for item in values}
    missing = ROUTES - routes
    if missing:
        findings.append(
            Finding(
                "route-coverage",
                "Missing primary routes: " + ", ".join(sorted(missing)),
                str(path),
            )
        )
    triggers = {item.get("expected_trigger") for item in values}
    if not {True, False}.issubset(triggers):
        findings.append(
            Finding("trigger-coverage", "Include positive and negative triggers.", str(path))
        )
    actions = {item.get("expected_action") for item in values}
    for required in ("baseline-and-optimize", "clarify", "do-not-trigger"):
        if required not in actions:
            findings.append(
                Finding("action-coverage", f"Missing action: {required}", str(path))
            )


def validate_behavior(path: Path, findings: list[Finding]) -> None:
    payload = load(path, findings)
    if payload is None:
        return
    for item in cases(payload, path, findings):
        for key in ("expected_properties", "forbidden_properties"):
            value = item.get(key)
            if not isinstance(value, list) or not value:
                findings.append(
                    Finding(
                        "behavior-properties",
                        f"Case {item.get('id', '?')} requires non-empty {key}.",
                        str(path),
                    )
                )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("eval_dir", type=Path, nargs="?", default=Path("evals"))
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    eval_dir = args.eval_dir.expanduser().resolve()
    findings: list[Finding] = []
    validate_routing(eval_dir / "routing.json", findings)
    validate_behavior(eval_dir / "behavior.json", findings)

    if args.format == "json":
        print(
            json.dumps(
                {
                    "eval_dir": str(eval_dir),
                    "count": len(findings),
                    "findings": [asdict(item) for item in findings],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(f"Eval directory: {eval_dir}")
        print(f"Findings: {len(findings)}")
        for item in findings:
            print(f"[ERROR] {item.code}: {item.message} ({item.path})")
        if not findings:
            print("Routing and behavior eval datasets are structurally complete.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())

