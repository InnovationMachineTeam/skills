#!/usr/bin/env python3
"""Rank validated skill opportunities with an explicit heuristic."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def score(candidate: dict[str, object]) -> int:
    scores = candidate.get("scores")
    if not isinstance(scores, dict):
        raise ValueError(f"candidate {candidate.get('id', '?')} has no scores object")
    positive = sum(int(scores[name]) for name in ("frequency", "leverage", "repeatability", "specificity", "gap", "evalability"))
    negative = int(scores["risk"]) + int(scores["maintenance"])
    return positive - negative


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    try:
        value = json.loads(args.manifest.read_text(encoding="utf-8"))
        candidates = value["candidates"]
        if not isinstance(candidates, list):
            raise ValueError("candidates must be an array")
        ranked = sorted(
            ({"id": item.get("id"), "title": item.get("title"), "decision": item.get("decision"), "heuristic_score": score(item)} for item in candidates if isinstance(item, dict)),
            key=lambda item: (-int(item["heuristic_score"]), str(item["id"])),
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps({"ranking": ranked, "note": "Heuristic ordering is not evidence of demand, ROI, safety, or approval."}, ensure_ascii=False, indent=2))
    else:
        for index, item in enumerate(ranked, start=1):
            print(f"{index}. {item['id']} — {item['heuristic_score']} — {item['decision']} — {item['title']}")
        print("Heuristic ordering is not evidence of demand, ROI, safety, or approval.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
