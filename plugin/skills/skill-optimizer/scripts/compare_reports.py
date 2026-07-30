#!/usr/bin/env python3
"""Compare two JSON reports emitted by analyze_skill.py."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_report(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read report {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"report root must be an object: {path}")
    if not isinstance(payload.get("metrics"), dict) or not isinstance(
        payload.get("counts"), dict
    ):
        raise ValueError(f"report lacks metrics or counts: {path}")
    return payload


def numeric_delta(before: object, after: object) -> int | float | None:
    if isinstance(before, (int, float)) and isinstance(after, (int, float)):
        return after - before
    return None


def compare(before: dict[str, object], after: dict[str, object]) -> dict[str, object]:
    before_metrics = before["metrics"]
    after_metrics = after["metrics"]
    before_counts = before["counts"]
    after_counts = after["counts"]
    assert isinstance(before_metrics, dict) and isinstance(after_metrics, dict)
    assert isinstance(before_counts, dict) and isinstance(after_counts, dict)

    metric_keys = sorted(set(before_metrics) | set(after_metrics))
    count_keys = sorted(set(before_counts) | set(after_counts))
    metric_deltas = {
        key: {
            "before": before_metrics.get(key),
            "after": after_metrics.get(key),
            "delta": numeric_delta(before_metrics.get(key), after_metrics.get(key)),
        }
        for key in metric_keys
    }
    finding_deltas = {
        key: {
            "before": before_counts.get(key, 0),
            "after": after_counts.get(key, 0),
            "delta": numeric_delta(before_counts.get(key, 0), after_counts.get(key, 0)),
        }
        for key in count_keys
    }
    return {
        "before_skill": before.get("skill"),
        "after_skill": after.get("skill"),
        "metric_deltas": metric_deltas,
        "finding_deltas": finding_deltas,
        "interpretation": "Structural deltas are evidence inputs, not proof of behavioral improvement.",
    }


def render_text(report: dict[str, object]) -> str:
    lines = [
        f"Before: {report['before_skill']}",
        f"After:  {report['after_skill']}",
        "Finding deltas:",
    ]
    finding_deltas = report["finding_deltas"]
    assert isinstance(finding_deltas, dict)
    for key, values in finding_deltas.items():
        assert isinstance(values, dict)
        lines.append(
            f"  {key}: {values['before']} -> {values['after']} ({values['delta']:+})"
        )
    lines.append("Metric deltas:")
    metric_deltas = report["metric_deltas"]
    assert isinstance(metric_deltas, dict)
    for key, values in metric_deltas.items():
        assert isinstance(values, dict)
        delta = values["delta"]
        delta_text = f"{delta:+}" if isinstance(delta, (int, float)) else "n/a"
        lines.append(
            f"  {key}: {values['before']} -> {values['after']} ({delta_text})"
        )
    lines.append(str(report["interpretation"]))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    try:
        result = compare(load_report(args.before), load_report(args.after))
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
