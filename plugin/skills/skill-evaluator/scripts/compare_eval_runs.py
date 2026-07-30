#!/usr/bin/env python3
"""Compare normalized baseline and candidate skill evaluation reports."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


VERDICTS = {"PASS", "FAIL", "INCONCLUSIVE", "BLOCKED", "NOT_EVALUATED"}
HASH = re.compile(r"^sha256:[0-9a-f]{64}$")


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema_version") != "1.0" or not isinstance(value.get("cases"), list) or not value["cases"]:
        raise ValueError(f"invalid run report: {path}")
    for key in ("run_id", "environment_id", "evaluation_revision"):
        if not isinstance(value.get(key), str) or not value[key].strip():
            raise ValueError(f"run report requires {key}: {path}")
    if not isinstance(value.get("target_hash"), str) or not HASH.fullmatch(value["target_hash"]):
        raise ValueError(f"run report requires sha256 target_hash: {path}")
    return value


def case_map(value: dict[str, Any], path: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in value["cases"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"].strip() or item["id"] in result or item.get("verdict") not in VERDICTS or not isinstance(item.get("layer"), str) or not item["layer"].strip():
            raise ValueError(f"invalid or duplicate case in {path}")
        result[item["id"]] = item
    return result


def compare(before: dict[str, Any], after: dict[str, Any], before_path: Path, after_path: Path) -> dict[str, Any]:
    comparable = before.get("environment_id") == after.get("environment_id") and before.get("evaluation_revision") == after.get("evaluation_revision")
    old = case_map(before, before_path)
    new = case_map(after, after_path)
    rows: list[dict[str, Any]] = []
    regressions: list[str] = []
    improvements: list[str] = []
    unresolved_changes: list[str] = []
    added_nonpasses: list[str] = []
    for case_id in sorted(set(old) | set(new)):
        left = old.get(case_id)
        right = new.get(case_id)
        if left is None:
            change = "added"
            if right["verdict"] != "PASS":
                added_nonpasses.append(case_id)
        elif right is None:
            change = "removed"
        elif left["verdict"] == right["verdict"]:
            change = "unchanged"
        elif right["verdict"] == "PASS" and left["verdict"] != "PASS":
            change = "improved"
            improvements.append(case_id)
        elif left["verdict"] == "PASS" and right["verdict"] != "PASS":
            change = "regressed"
            regressions.append(case_id)
        else:
            change = "changed"
            unresolved_changes.append(case_id)
        rows.append({"id": case_id, "baseline": left.get("verdict") if left else None, "candidate": right.get("verdict") if right else None, "change": change})
    metrics: dict[str, dict[str, float]] = {}
    old_metrics = before.get("metrics", {})
    new_metrics = after.get("metrics", {})
    if isinstance(old_metrics, dict) and isinstance(new_metrics, dict):
        for key in sorted(set(old_metrics) & set(new_metrics)):
            if isinstance(old_metrics[key], (int, float)) and not isinstance(old_metrics[key], bool) and isinstance(new_metrics[key], (int, float)) and not isinstance(new_metrics[key], bool):
                metrics[key] = {"baseline": old_metrics[key], "candidate": new_metrics[key], "delta": round(new_metrics[key] - old_metrics[key], 6)}
    removed = [row["id"] for row in rows if row["change"] == "removed"]
    candidate_blocked = sorted(case_id for case_id, item in new.items() if item["verdict"] == "BLOCKED")
    candidate_unresolved = sorted(case_id for case_id, item in new.items() if item["verdict"] in {"INCONCLUSIVE", "NOT_EVALUATED"})
    candidate_new_failures = sorted(case_id for case_id, item in new.items() if item["verdict"] == "FAIL" and (case_id not in old or old[case_id]["verdict"] != "FAIL"))
    reason_codes: list[str] = []
    if not comparable:
        decision = "INCONCLUSIVE"
        reason_codes.append("environment-or-evaluation-revision-mismatch")
    elif candidate_blocked:
        decision = "BLOCKED"
        reason_codes.append("candidate-has-blocked-cases")
    elif regressions or candidate_new_failures:
        decision = "REJECT"
        reason_codes.append("candidate-has-new-failures")
    elif removed or unresolved_changes or added_nonpasses or candidate_unresolved:
        decision = "INCONCLUSIVE"
        reason_codes.append("coverage-or-verdict-unresolved")
    elif improvements:
        decision = "ACCEPT"
    else:
        decision = "NO_CHANGE"
    return {"comparable": comparable, "decision": decision, "reason_codes": reason_codes, "regressions": regressions, "improvements": improvements, "unresolved_changes": unresolved_changes, "added_nonpasses": added_nonpasses, "candidate_blocked": candidate_blocked, "candidate_unresolved": candidate_unresolved, "candidate_new_failures": candidate_new_failures, "removed": removed, "metric_deltas": metrics, "cases": rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    before_path = args.baseline.expanduser().resolve()
    after_path = args.candidate.expanduser().resolve()
    try:
        result = compare(load(before_path), load(after_path), before_path, after_path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"Evaluation comparison failed: {exc}", file=sys.stderr)
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
