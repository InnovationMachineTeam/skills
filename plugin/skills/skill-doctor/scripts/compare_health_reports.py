#!/usr/bin/env python3
"""Compare before and after reports from doctor_skill.py."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


HEALTH_ORDER = {"HEALTHY": 0, "DEGRADED": 1, "BROKEN": 2, "UNSAFE": 3}


def load(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("health") not in HEALTH_ORDER:
        raise ValueError(f"invalid doctor report: {path}")
    if not isinstance(payload.get("findings"), list):
        raise ValueError(f"report lacks findings: {path}")
    return payload


def finding_keys(payload: dict[str, object]) -> set[str]:
    output: set[str] = set()
    findings = payload["findings"]
    assert isinstance(findings, list)
    for item in findings:
        if isinstance(item, dict):
            output.add(f"{item.get('domain')}/{item.get('code')}@{item.get('path')}")
    return output


def compare(before: dict[str, object], after: dict[str, object]) -> dict[str, object]:
    before_health = str(before["health"])
    after_health = str(after["health"])
    before_skill = str(before.get("skill", ""))
    after_skill = str(after.get("skill", ""))
    comparable_identity = Path(before_skill).name == Path(after_skill).name
    before_findings = finding_keys(before)
    after_findings = finding_keys(after)
    resolved = before_findings - after_findings if comparable_identity else set()
    new = after_findings - before_findings if comparable_identity else set()
    return {
        "before_skill": before_skill,
        "after_skill": after_skill,
        "comparable_identity": comparable_identity,
        "before_health": before_health,
        "after_health": after_health,
        "health_delta": HEALTH_ORDER[after_health] - HEALTH_ORDER[before_health],
        "resolved_findings": sorted(resolved),
        "new_findings": sorted(new),
        "static_decision": "incomparable-identity" if not comparable_identity else (
            "regressed"
            if HEALTH_ORDER[after_health] > HEALTH_ORDER[before_health] or new
            else "improved-static"
            if HEALTH_ORDER[after_health] < HEALTH_ORDER[before_health] or resolved
            else "unchanged-static"
        ),
        "recovery_note": (
            "Reports refer to different skill identities and cannot establish improvement."
            if not comparable_identity
            else "Static comparison cannot assign RECOVERED without rerunning the original symptom and regressions."
        ),
    }


def render_text(payload: dict[str, object]) -> str:
    lines = [
        f"Before health: {payload['before_health']}",
        f"After health:  {payload['after_health']}",
        f"Static decision: {payload['static_decision']}",
        "Resolved findings:",
    ]
    resolved = payload["resolved_findings"]
    new = payload["new_findings"]
    assert isinstance(resolved, list) and isinstance(new, list)
    if resolved:
        lines.extend(f"  - {item}" for item in resolved)
    else:
        lines.append("  - none")
    lines.append("New findings:")
    if new:
        lines.extend(f"  - {item}" for item in new)
    else:
        lines.append("  - none")
    lines.append(str(payload["recovery_note"]))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    try:
        payload = compare(load(args.before), load(args.after))
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_text(payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
