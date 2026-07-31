#!/usr/bin/env python3
"""Classify E2E findings without repairing agentkit or donor skills."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def safe_output(path: Path) -> Path:
    resolved = path.resolve()
    if resolved.exists():
        raise ValueError(f"output already exists: {resolved}")
    if not resolved.parent.is_dir() or resolved.parent.is_symlink():
        raise ValueError("output parent must be an existing real directory")
    if resolved == Path(resolved.anchor) or resolved == Path.home().resolve():
        raise ValueError("refusing broad output")
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--findings", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    findings_doc = json.loads(args.findings.read_text(encoding="utf-8"))
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    output = safe_output(args.output)
    donors = {item["name"]: item for item in manifest.get("donors", [])}
    decisions = []
    for finding in findings_doc.get("findings", []):
        finding_id = finding.get("id")
        owner = finding.get("owner")
        kind = finding.get("kind")
        if kind not in {"defect", "improvement"}:
            raise ValueError(f"{finding_id}: kind must be defect or improvement")
        base = {
            "finding_id": finding_id,
            "owner": owner,
            "kind": kind,
            "severity": finding.get("severity"),
            "evidence": finding.get("evidence"),
            "proposed_change": finding.get("proposed_change"),
        }
        if owner == "agentkit":
            base.update({"action": "stage-agentkit-candidate", "approval": {"status": "covered-by-agentkit-candidate-scope"}})
        elif owner in donors:
            scenario = "repair-and-improve" if kind == "defect" else "optimize-existing"
            lock = donors[owner]
            base.update({
                "action": "ask-user-then-dispatch",
                "scenario": scenario,
                "donor": {"name": owner, "version": lock["version"], "source_tree_sha256": lock["source_tree_sha256"]},
                "approval": {
                    "status": "required",
                    "subject": f"Create an improvement prompt and launch {scenario} for a staged {owner} candidate",
                    "scope": "prompt-and-staged-process",
                },
                "approval_question": (
                    f"Разрешить создать prompt и запустить `{scenario}` для нового staged candidate "
                    f"`{owner}@{lock['version']}`? Канонический и vendored donor останутся read-only; "
                    "установка и публикация не входят в это разрешение."
                ),
            })
        elif owner == "environment":
            base.update({"action": "repair-environment-or-mark-blocked", "approval": {"status": "not-applicable"}})
        elif owner == "test":
            base.update({"action": "repair-evaluation-before-rerun", "approval": {"status": "not-applicable"}})
        else:
            raise ValueError(f"{finding_id}: unknown owner {owner!r}")
        decisions.append(base)

    payload = {
        "schema_version": 1,
        "run_id": findings_doc.get("run_id"),
        "source_findings": str(args.findings),
        "decisions": decisions,
        "donor_mutations_performed": False,
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"decisions": len(decisions), "output": str(output)}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        raise SystemExit(1)
