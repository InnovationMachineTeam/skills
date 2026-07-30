#!/usr/bin/env python3
"""Score expected versus observed routing decisions."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


def ratio(numerator: int, denominator: int) -> float | None:
    return round(numerator / denominator, 6) if denominator else None


def wilson(successes: int, total: int, z: float = 1.96) -> list[float] | None:
    if total == 0:
        return None
    probability = successes / total
    denominator = 1 + z * z / total
    center = (probability + z * z / (2 * total)) / denominator
    half = z * math.sqrt(probability * (1 - probability) / total + z * z / (4 * total * total)) / denominator
    return [round(max(0.0, center - half), 6), round(min(1.0, center + half), 6)]


def score(cases: list[dict[str, Any]]) -> dict[str, Any]:
    tp = fp = tn = fn = 0
    failures: list[str] = []
    ids: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise ValueError(f"case {index} must be an object")
        case_id = case.get("id", str(index))
        if not isinstance(case_id, str) or not case_id.strip() or case_id in ids:
            raise ValueError(f"case {index} needs a unique non-empty string id")
        ids.add(case_id)
        expected = case.get("expected_trigger")
        observed = case.get("observed_trigger")
        if not isinstance(expected, bool) or not isinstance(observed, bool):
            raise ValueError(f"case {case_id} needs boolean expected_trigger and observed_trigger")
        if expected and observed:
            tp += 1
        elif not expected and observed:
            fp += 1
            failures.append(case_id)
        elif not expected and not observed:
            tn += 1
        else:
            fn += 1
            failures.append(case_id)
    total = tp + fp + tn + fn
    precision = ratio(tp, tp + fp)
    recall = ratio(tp, tp + fn)
    return {
        "counts": {"tp": tp, "fp": fp, "tn": tn, "fn": fn, "total": total},
        "metrics": {
            "accuracy": ratio(tp + tn, total),
            "precision": precision,
            "recall": recall,
            "specificity": ratio(tn, tn + fp),
            "f1": round(2 * precision * recall / (precision + recall), 6) if precision is not None and recall is not None and precision + recall else None,
            "false_positive_rate": ratio(fp, fp + tn),
            "false_negative_rate": ratio(fn, fn + tp),
            "accuracy_wilson_95": wilson(tp + tn, total),
            "precision_wilson_95": wilson(tp, tp + fp),
            "recall_wilson_95": wilson(tp, tp + fn),
            "specificity_wilson_95": wilson(tn, tn + fp),
        },
        "misclassified_case_ids": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.results.expanduser().resolve().read_text(encoding="utf-8"))
        cases = value if isinstance(value, list) else value.get("cases")
        if not isinstance(cases, list) or not cases:
            raise ValueError("results must contain a non-empty cases array")
        result = score(cases)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"Routing scoring failed: {exc}", file=sys.stderr)
        return 1
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = args.output.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
