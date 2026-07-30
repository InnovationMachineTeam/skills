#!/usr/bin/env python3
"""Validate the structure and internal references of a harvest manifest."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


TYPES = {"trigger", "workflow", "knowledge", "prompt-template", "script-tool", "eval-failure", "safety-governance", "anti-pattern"}
CONFIDENCE = {"verified", "supported", "inferred", "speculative"}
MATURITY = {"observed", "recurring", "generalized", "validated", "adoptable"}
DECISIONS = {"adopt", "adapt", "research", "reject"}
RIGHTS = {"cleared", "restricted", "unknown"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    location: str


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(value: object) -> list[Finding]:
    findings: list[Finding] = []
    if not isinstance(value, dict):
        return [Finding("error", "root", "Manifest root must be an object.", "/")]
    for key in ("schema_version", "harvest_id", "objective"):
        if not nonempty(value.get(key)):
            findings.append(Finding("error", "required", f"{key} must be a non-empty string.", f"/{key}"))
    if value.get("schema_version") != "1.0":
        findings.append(Finding("error", "schema", "schema_version must be 1.0.", "/schema_version"))
    for key in ("contradictions", "exclusions", "downstream_handoffs"):
        if not isinstance(value.get(key), list):
            findings.append(Finding("error", "array", f"{key} must be an array.", f"/{key}"))

    raw_sources = value.get("sources")
    source_ids: set[str] = set()
    if not isinstance(raw_sources, list) or not raw_sources:
        findings.append(Finding("error", "sources", "sources must be a non-empty array.", "/sources"))
    else:
        for index, source in enumerate(raw_sources):
            where = f"/sources/{index}"
            if not isinstance(source, dict):
                findings.append(Finding("error", "source-shape", "Source must be an object.", where))
                continue
            source_id = source.get("source_id")
            if not nonempty(source_id):
                findings.append(Finding("error", "source-id", "source_id is required.", where))
            elif source_id in source_ids:
                findings.append(Finding("error", "source-id", f"Duplicate source_id: {source_id}", where))
            else:
                source_ids.add(str(source_id))
            if not nonempty(source.get("locator")):
                findings.append(Finding("error", "source-locator", "locator is required.", where))
            digest = source.get("sha256")
            if digest is not None and (not isinstance(digest, str) or not SHA256_RE.fullmatch(digest)):
                findings.append(Finding("error", "sha256", "sha256 must be lowercase 64-character hex or null.", where))
            if source.get("rights_status") not in RIGHTS:
                findings.append(Finding("error", "rights", "Invalid rights_status.", where))
            if not nonempty(source.get("license")):
                findings.append(Finding("error", "license", "license must be a string; use unknown when absent.", where))

    raw_candidates = value.get("candidates")
    candidate_ids: set[str] = set()
    if not isinstance(raw_candidates, list) or not raw_candidates:
        findings.append(Finding("error", "candidates", "candidates must be a non-empty array.", "/candidates"))
    else:
        for index, candidate in enumerate(raw_candidates):
            where = f"/candidates/{index}"
            if not isinstance(candidate, dict):
                findings.append(Finding("error", "candidate-shape", "Candidate must be an object.", where))
                continue
            candidate_id = candidate.get("id")
            if not nonempty(candidate_id):
                findings.append(Finding("error", "candidate-id", "id is required.", where))
            elif candidate_id in candidate_ids:
                findings.append(Finding("error", "candidate-id", f"Duplicate candidate id: {candidate_id}", where))
            else:
                candidate_ids.add(str(candidate_id))
            for key in ("title", "summary"):
                if not nonempty(candidate.get(key)):
                    findings.append(Finding("error", "candidate-text", f"{key} is required.", where))
            for key, allowed in (("type", TYPES), ("confidence", CONFIDENCE), ("maturity", MATURITY), ("decision", DECISIONS)):
                if candidate.get(key) not in allowed:
                    findings.append(Finding("error", "enum", f"Invalid {key}.", where))
            for key in ("assumptions", "risks", "validation"):
                raw = candidate.get(key)
                if not isinstance(raw, list):
                    findings.append(Finding("error", "array", f"{key} must be an array.", where))
            if isinstance(candidate.get("validation"), list) and not candidate["validation"]:
                findings.append(Finding("error", "validation", "validation must contain at least one falsifiable check.", where))
            evidence = candidate.get("evidence")
            if not isinstance(evidence, list) or not evidence:
                findings.append(Finding("error", "evidence", "evidence must be a non-empty array.", where))
            else:
                for evidence_index, item in enumerate(evidence):
                    evidence_where = f"{where}/evidence/{evidence_index}"
                    if not isinstance(item, dict):
                        findings.append(Finding("error", "evidence-shape", "Evidence must be an object.", evidence_where))
                        continue
                    if item.get("source_id") not in source_ids:
                        findings.append(Finding("error", "evidence-source", "Evidence references an unknown source_id.", evidence_where))
                    for key in ("locator", "observation"):
                        if not nonempty(item.get(key)):
                            findings.append(Finding("error", "evidence-text", f"{key} is required.", evidence_where))
            if candidate.get("decision") == "adopt" and candidate.get("maturity") != "adoptable":
                findings.append(Finding("error", "premature-adoption", "adopt requires adoptable maturity.", where))
            if candidate.get("decision") == "adopt":
                evidence_sources = {item.get("source_id") for item in evidence if isinstance(item, dict)} if isinstance(evidence, list) else set()
                blocked = [source for source in raw_sources if isinstance(source, dict) and source.get("source_id") in evidence_sources and source.get("rights_status") != "cleared"] if isinstance(raw_sources, list) else []
                if blocked:
                    findings.append(Finding("error", "rights-block", "adopt requires cleared rights for all evidence sources.", where))
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
            print(f"[{item.severity.upper()}] {item.code}: {item.message} ({item.location})")
        if not findings:
            print("Harvest manifest is structurally valid and internally consistent.")
    return 1 if any(item.severity == "error" for item in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
