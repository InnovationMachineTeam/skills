#!/usr/bin/env python3
"""Validate an agent-skill mapping proposal against an asset registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DECISIONS = {"MATCH", "CONDITIONAL", "GAP", "CONFLICT", "REJECT"}


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(proposal: object, registry: object) -> list[str]:
    failures: list[str] = []
    if not isinstance(proposal, dict) or not isinstance(registry, dict):
        return ["proposal and registry roots must be objects"]
    if proposal.get("schema_version") != 1:
        failures.append("proposal schema_version must be 1")
    if not isinstance(proposal.get("registry_revision"), str) or not proposal["registry_revision"]:
        failures.append("registry_revision is required")
    if not isinstance(proposal.get("map_revision"), str) or not proposal["map_revision"]:
        failures.append("map_revision is required")
    assets = registry.get("assets")
    if not isinstance(assets, list):
        return failures + ["registry.assets must be an array"]
    by_ref: dict[str, dict] = {}
    for asset in assets:
        if isinstance(asset, dict) and isinstance(asset.get("id"), str):
            by_ref[asset["id"]] = asset
    agents = proposal.get("agents")
    if not isinstance(agents, list) or not agents:
        return failures + ["agents must be a non-empty array"]
    for index, item in enumerate(agents):
        if not isinstance(item, dict):
            failures.append(f"agents[{index}] must be an object")
            continue
        agent_ref = item.get("agent_ref")
        if agent_ref not in by_ref or by_ref[agent_ref].get("kind") != "agent":
            failures.append(f"agents[{index}].agent_ref does not resolve to an agent")
        budget = item.get("max_capabilities")
        recommendations = item.get("recommendations")
        if not isinstance(budget, int) or budget < 0:
            failures.append(f"agents[{index}].max_capabilities must be non-negative")
            budget = 0
        if not isinstance(recommendations, list):
            failures.append(f"agents[{index}].recommendations must be an array")
            continue
        active = 0
        for rec_index, rec in enumerate(recommendations):
            label = f"agents[{index}].recommendations[{rec_index}]"
            if not isinstance(rec, dict) or rec.get("decision") not in DECISIONS:
                failures.append(f"{label} has invalid decision")
                continue
            if not isinstance(rec.get("evidence"), list) or not rec["evidence"]:
                failures.append(f"{label}.evidence must be non-empty")
            capability_ref = rec.get("capability_ref")
            if rec["decision"] in {"MATCH", "CONDITIONAL"}:
                active += 1
                asset = by_ref.get(capability_ref)
                if asset is None:
                    failures.append(f"{label}.capability_ref does not resolve")
                    continue
                if asset.get("lifecycle") in {"retired", "quarantined"}:
                    failures.append(f"{label} references unavailable lifecycle")
                if asset.get("visibility") == "private":
                    if asset.get("owner_agent_ref") != agent_ref:
                        failures.append(f"{label} violates private ownership")
                    if asset.get("allowed_consumers") != [agent_ref]:
                        failures.append(f"{label} has invalid private consumers")
        if active > budget:
            failures.append(f"agents[{index}] exceeds capability budget")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proposal", type=Path)
    parser.add_argument("registry", type=Path)
    args = parser.parse_args()
    try:
        failures = validate(load(args.proposal), load(args.registry))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        return 1
    print("PASS agent-skill mapping proposal is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
