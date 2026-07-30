#!/usr/bin/env python3
"""Validate a skill-scout opportunity manifest."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


TYPES = {"knowledge", "workflow", "tool", "artifact", "evaluation", "safety", "routing", "portfolio", "agent-system"}
DECISIONS = {"CREATE_NEW", "EXTEND_EXISTING", "USE_EXISTING", "USE_AUTOMATION", "KEEP_AD_HOC", "RESEARCH"}
CONFIDENCE = {"high", "medium", "low"}
SCORES = {"frequency", "leverage", "repeatability", "specificity", "gap", "evalability", "risk", "maintenance"}


@dataclass
class Finding:
    code: str
    message: str
    location: str


def present(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(value: object) -> list[Finding]:
    findings: list[Finding] = []
    if not isinstance(value, dict):
        return [Finding("root", "Manifest root must be an object.", "/")]
    for key in ("schema_version", "scout_id", "scope"):
        if not present(value.get(key)):
            findings.append(Finding("required", f"{key} must be a non-empty string.", f"/{key}"))
    if value.get("schema_version") != "1.0":
        findings.append(Finding("schema", "schema_version must be 1.0.", "/schema_version"))
    for key in ("rejected", "open_questions"):
        if not isinstance(value.get(key), list):
            findings.append(Finding("array", f"{key} must be an array.", f"/{key}"))

    source_ids: set[str] = set()
    sources = value.get("sources")
    if not isinstance(sources, list) or not sources:
        findings.append(Finding("sources", "sources must be a non-empty array.", "/sources"))
    else:
        for index, source in enumerate(sources):
            where = f"/sources/{index}"
            if not isinstance(source, dict):
                findings.append(Finding("source", "Source must be an object.", where))
                continue
            source_id = source.get("source_id")
            if not present(source_id) or source_id in source_ids:
                findings.append(Finding("source-id", "source_id must be non-empty and unique.", where))
            else:
                source_ids.add(str(source_id))
            for key in ("locator", "consent", "sensitivity"):
                if not present(source.get(key)):
                    findings.append(Finding("source-field", f"{key} is required.", where))

    candidate_ids: set[str] = set()
    candidates = value.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        findings.append(Finding("candidates", "candidates must be a non-empty array.", "/candidates"))
    else:
        for index, candidate in enumerate(candidates):
            where = f"/candidates/{index}"
            if not isinstance(candidate, dict):
                findings.append(Finding("candidate", "Candidate must be an object.", where))
                continue
            candidate_id = candidate.get("id")
            if not present(candidate_id) or candidate_id in candidate_ids:
                findings.append(Finding("candidate-id", "id must be non-empty and unique.", where))
            else:
                candidate_ids.add(str(candidate_id))
            for key in ("title", "problem", "current_workaround", "next_step"):
                if not present(candidate.get(key)):
                    findings.append(Finding("candidate-field", f"{key} is required.", where))
            if candidate.get("opportunity_type") not in TYPES:
                findings.append(Finding("type", "Invalid opportunity_type.", where))
            if candidate.get("decision") not in DECISIONS:
                findings.append(Finding("decision", "Invalid decision.", where))
            if candidate.get("confidence") not in CONFIDENCE:
                findings.append(Finding("confidence", "Invalid confidence.", where))
            for key in ("existing_coverage", "users", "trigger_examples", "negative_triggers", "resources", "tools", "permissions", "risks", "evaluation"):
                if not isinstance(candidate.get(key), list):
                    findings.append(Finding("array", f"{key} must be an array.", where))
            if isinstance(candidate.get("evaluation"), list) and not candidate["evaluation"]:
                findings.append(Finding("evaluation", "evaluation must contain at least one check.", where))
            if not isinstance(candidate.get("context_plan"), dict):
                findings.append(Finding("context", "context_plan must be an object.", where))
            scores = candidate.get("scores")
            if not isinstance(scores, dict) or set(scores) != SCORES:
                findings.append(Finding("scores", "scores must contain exactly the eight required dimensions.", where))
            else:
                for name, score in scores.items():
                    if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 5:
                        findings.append(Finding("score", f"{name} must be an integer from 0 to 5.", where))
            evidence = candidate.get("evidence")
            if not isinstance(evidence, list) or not evidence:
                findings.append(Finding("evidence", "evidence must be a non-empty array.", where))
            else:
                for evidence_index, item in enumerate(evidence):
                    item_where = f"{where}/evidence/{evidence_index}"
                    if not isinstance(item, dict) or item.get("source_id") not in source_ids:
                        findings.append(Finding("evidence-source", "Evidence must reference a known source_id.", item_where))
                    elif not present(item.get("locator")) or not present(item.get("observation")):
                        findings.append(Finding("evidence-field", "Evidence locator and observation are required.", item_where))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    try:
        value = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"Error: cannot read valid JSON: {exc}", file=sys.stderr)
        return 2
    findings = validate(value)
    payload = {"manifest": str(args.manifest.resolve()), "count": len(findings), "findings": [asdict(item) for item in findings]}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Manifest: {payload['manifest']}")
        print(f"Findings: {len(findings)}")
        for item in findings:
            print(f"[ERROR] {item.code}: {item.message} ({item.location})")
        if not findings:
            print("Opportunity manifest is structurally valid.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
