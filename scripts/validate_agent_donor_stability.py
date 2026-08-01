#!/usr/bin/env python3
"""Validate the individual-agent donor stability ledger and maturity gate."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path


DONORS = (
    "agent-architect",
    "agent-best-practices",
    "agent-builder",
    "agent-context",
    "agent-doctor",
    "agent-evaluator",
    "agent-manager",
    "agent-optimizer",
    "agent-refactor",
    "agent-scout",
)
BLOCKING_LAYERS = (
    "structure",
    "routing",
    "behavior",
    "authority",
    "documentation",
    "coexistence",
    "lifecycle",
)
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
SHA256 = re.compile(r"^sha256:[a-f0-9]{64}$")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def semver(value: str) -> tuple[int, int, int]:
    match = SEMVER.fullmatch(value)
    if not match:
        raise ValueError(f"invalid release SemVer: {value}")
    return tuple(int(part) for part in match.groups())


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(
        item
        for item in root.rglob("*")
        if item.is_file()
        and "__pycache__" not in item.parts
        and item.suffix not in {".pyc", ".pyo"}
        and item.name != ".DS_Store"
    ):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def portfolio_hash(donors: list[dict]) -> str:
    payload = "\n".join(
        f"{item['name']}@{item['version']}:{item['content_sha256']}"
        for item in sorted(donors, key=lambda value: value["name"])
    )
    return f"sha256:{hashlib.sha256(payload.encode('utf-8')).hexdigest()}"


def validate(root: Path, ledger_path: Path) -> list[str]:
    failures: list[str] = []
    try:
        ledger = load(ledger_path)
        registry = load(root / "docs" / "AGENT-ASSET-REGISTRY.json")
        release = load(root / "catalog" / "release.json")
    except (OSError, json.JSONDecodeError) as exc:
        return [str(exc)]

    if ledger.get("schema_version") != 1:
        failures.append("schema_version must be 1")
    if ledger.get("required_stable_cycles") != 2:
        failures.append("required_stable_cycles must remain 2")
    if ledger.get("initial_donor_release") != "3.2.0":
        failures.append("initial_donor_release must remain 3.2.0")
    try:
        stability_epoch = semver(ledger.get("stability_epoch_release", ""))
        if stability_epoch < semver(ledger.get("initial_donor_release", "0.0.0")):
            failures.append("stability epoch cannot precede the initial donor release")
    except ValueError as exc:
        failures.append(str(exc))
        stability_epoch = (0, 0, 0)

    donors = ledger.get("donors")
    if not isinstance(donors, list) or {item.get("name") for item in donors} != set(DONORS):
        failures.append("ledger must contain exactly the ten individual-agent donors")
        donors = []

    registered = {
        item.get("name"): item
        for item in registry.get("assets", [])
        if item.get("kind") == "skill" and item.get("scope") == "repository"
    }
    for donor in donors:
        name = donor.get("name")
        asset = registered.get(name)
        if not asset:
            failures.append(f"{name}: missing registry asset")
            continue
        skill_root = root / asset["locator"]
        actual_hash = tree_hash(skill_root)
        for key, expected, actual in (
            ("version", donor.get("version"), asset.get("version")),
            ("content_sha256", donor.get("content_sha256"), asset.get("content_sha256")),
            ("tree hash", donor.get("content_sha256"), actual_hash),
        ):
            if expected != actual:
                failures.append(f"{name}: {key} drift ({expected!r} != {actual!r})")

    expected_portfolio_hash = portfolio_hash(donors) if donors else None

    cycles = ledger.get("cycles")
    if not isinstance(cycles, list):
        failures.append("cycles must be a list")
        cycles = []
    previous_release = stability_epoch
    stable_count = 0
    cycle_ids: set[str] = set()
    observation_times: list[datetime] = []
    for cycle in cycles:
        cycle_id = cycle.get("id")
        if not cycle_id or cycle_id in cycle_ids:
            failures.append(f"missing or duplicate cycle id: {cycle_id}")
        cycle_ids.add(cycle_id)
        try:
            current_release = semver(cycle.get("release", ""))
        except ValueError as exc:
            failures.append(str(exc))
            continue
        if current_release <= previous_release:
            failures.append(f"{cycle_id}: releases must be strictly increasing")
        previous_release = current_release
        if cycle.get("status") != "stable":
            continue
        stable_count += 1
        # Stability cycles are immutable historical observations. A later
        # maintenance release may legitimately advance the current donor
        # snapshot without rewriting the portfolio hash evaluated by a prior
        # cycle.
        if not SHA256.fullmatch(str(cycle.get("portfolio_hash", ""))):
            failures.append(f"{cycle_id}: portfolio hash must be a sha256 digest")
        if cycle.get("blocking_findings"):
            failures.append(f"{cycle_id}: stable cycle cannot have blocking findings")
        layer_verdicts = cycle.get("layer_verdicts", {})
        for layer in BLOCKING_LAYERS:
            if layer_verdicts.get(layer) != "PASS":
                failures.append(f"{cycle_id}: blocking layer {layer} must PASS")
        evidence = cycle.get("evidence", [])
        if not isinstance(evidence, list) or len(evidence) < 5:
            failures.append(f"{cycle_id}: at least five evidence locators are required")
        for locator in evidence if isinstance(evidence, list) else []:
            if not isinstance(locator, str) or not locator or not (root / locator).exists():
                failures.append(f"{cycle_id}: missing evidence locator {locator!r}")
        try:
            observed = datetime.fromisoformat(cycle.get("observed_at", "").replace("Z", "+00:00"))
            if observed.tzinfo is None:
                raise ValueError("timezone required")
            observation_times.append(observed)
        except (AttributeError, ValueError):
            failures.append(f"{cycle_id}: observed_at must be a timezone-aware ISO timestamp")

    if any(later <= earlier for earlier, later in zip(observation_times, observation_times[1:])):
        failures.append("stable cycles require distinct increasing observation timestamps")

    gate = ledger.get("agentkit_gate", {})
    completed = gate.get("stable_cycles_completed")
    if completed != stable_count:
        failures.append("agentkit_gate stable cycle count does not match ledger")
    workflows = gate.get("real_workflows_observed", [])
    if isinstance(workflows, list):
        workflow_ids: set[str] = set()
        for workflow in workflows:
            if not isinstance(workflow, dict) or not workflow.get("id") or workflow.get("id") in workflow_ids:
                failures.append("real workflow observations require unique object identities")
                continue
            workflow_ids.add(workflow["id"])
            evidence = workflow.get("evidence")
            if not isinstance(evidence, str) or not (root / evidence).is_file():
                failures.append(f"{workflow['id']}: missing workflow evidence")
                continue
            actual_evidence_hash = f"sha256:{hashlib.sha256((root / evidence).read_bytes()).hexdigest()}"
            if workflow.get("sha256") != actual_evidence_hash:
                failures.append(f"{workflow['id']}: evidence hash drift")
            try:
                observation = load(root / evidence)
                run_root = (root / evidence).parent
                run_state = load(run_root / "run-state.json")
                if observation.get("workflow_id") != workflow["id"]:
                    failures.append(f"{workflow['id']}: evidence identity differs")
                if observation.get("outcome", {}).get("verdict") != "PASS":
                    failures.append(f"{workflow['id']}: observation outcome must PASS")
                if run_state.get("real_workflow_observation") is not True or run_state.get("execution_kind") != "semantic-donor-run":
                    failures.append(f"{workflow['id']}: synthetic runs cannot satisfy maturity")
                if run_state.get("verdict") != "PASS":
                    failures.append(f"{workflow['id']}: run must PASS")
            except (OSError, json.JSONDecodeError) as exc:
                failures.append(f"{workflow['id']}: {exc}")
    contracts = (
        gate.get("upgrade_contract_frozen") is True,
        gate.get("rollback_contract_frozen") is True,
        gate.get("pack_holdout_frozen") is True,
    )
    mature = (
        stable_count >= ledger.get("required_stable_cycles", 2)
        and isinstance(workflows, list)
        and len(workflows) >= 3
        and all(contracts)
    )
    if not mature and gate.get("status") != "deferred":
        failures.append("agentkit must remain deferred until every maturity requirement passes")
    agentkit_exists = (root / "skills" / "agent-skills" / "agentkit" / "SKILL.md").exists()
    if agentkit_exists and not mature:
        failures.append("agentkit bundle exists before maturity gate passes")
    if agentkit_exists and gate.get("status") != "released":
        failures.append("published agentkit requires released maturity state")
    if gate.get("status") in {"ready", "released"} and not mature:
        failures.append("agentkit cannot be ready without cycles, workflows and frozen contracts")
    if mature and gate.get("status") not in {"ready", "released"}:
        failures.append("mature agentkit gate must be ready or released")

    candidate = gate.get("candidate")
    candidate_root = root / "candidates" / "agentkit"
    if candidate:
        locator = candidate.get("locator")
        if locator != "candidates/agentkit":
            failures.append("agentkit candidate locator must remain candidates/agentkit")
        if candidate.get("status") != "experimental" or candidate.get("discoverable") is not False:
            failures.append("pre-maturity agentkit candidate must be experimental and non-discoverable")
        try:
            semver(candidate.get("version", ""))
        except ValueError as exc:
            failures.append(str(exc))
        if not (candidate_root / "SKILL.md").is_file():
            failures.append("declared agentkit candidate is missing SKILL.md")
        if candidate_root.is_dir() and tree_hash(candidate_root) != candidate.get("content_sha256"):
            failures.append("agentkit candidate content hash drift")
        for artifact_key in ("evaluation_plan", "evaluation_result"):
            artifact = root / str(candidate.get(artifact_key, ""))
            if not artifact.is_file():
                failures.append(f"agentkit candidate missing {artifact_key}")
                continue
            try:
                artifact_data = load(artifact)
                artifact_hash = (
                    artifact_data.get("target", {}).get("hash")
                    if artifact_key == "evaluation_plan"
                    else artifact_data.get("target_hash")
                )
                if artifact_hash != candidate.get("content_sha256"):
                    failures.append(f"agentkit candidate {artifact_key} hash drift")
            except json.JSONDecodeError as exc:
                failures.append(f"invalid agentkit candidate {artifact_key}: {exc}")
        try:
            lock = load(candidate_root / "donors.json")
            locked = {item.get("name"): item for item in lock.get("donors", [])}
            if set(locked) != set(DONORS):
                failures.append("agentkit candidate must lock exactly the ten donors")
            for donor in donors:
                entry = locked.get(donor.get("name"), {})
                if entry.get("version") != donor.get("version"):
                    failures.append(f"agentkit candidate version drift: {donor.get('name')}")
                if entry.get("source_tree_sha256") != donor.get("content_sha256"):
                    failures.append(f"agentkit candidate hash drift: {donor.get('name')}")
            if list((candidate_root / "vendor").rglob("SKILL.md")):
                failures.append("agentkit vendor contains nested discoverable SKILL.md")
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"invalid agentkit candidate lock: {exc}")
        catalog = load(root / "catalog" / "entries.json")
        if "agentkit" in {item.get("name") for item in catalog.get("entries", [])}:
            failures.append("experimental agentkit candidate must not be in catalog")
        if (root / "plugins" / "agentkit").exists():
            failures.append("experimental agentkit candidate must not have a generated plugin")
        for marketplace in (
            root / ".claude-plugin" / "marketplace.json",
            root / ".agents" / "plugins" / "marketplace.json",
            root / ".cursor-plugin" / "marketplace.json",
        ):
            manifest = load(marketplace)
            if "agentkit" in {item.get("name") for item in manifest.get("plugins", [])}:
                failures.append(f"experimental agentkit candidate leaked into {marketplace}")
    elif candidate_root.exists():
        failures.append("agentkit candidate exists but is not declared in the maturity ledger")

    released = gate.get("release")
    if gate.get("status") == "released":
        if not isinstance(released, dict):
            failures.append("released agentkit requires a release declaration")
        else:
            stable_root = root / str(released.get("locator", ""))
            if released.get("locator") != "skills/agent-skills/agentkit" or not (stable_root / "SKILL.md").is_file():
                failures.append("released agentkit locator is missing or invalid")
            else:
                try:
                    if semver(released.get("version", "")) < (1, 0, 0):
                        failures.append("stable agentkit release cannot precede 1.0.0")
                except ValueError as exc:
                    failures.append(str(exc))
                if tree_hash(stable_root) != released.get("content_sha256"):
                    failures.append("released agentkit content hash drift")
                asset = registered.get("agentkit", {})
                if asset.get("version") != released.get("version") or asset.get("content_sha256") != released.get("content_sha256"):
                    failures.append("released agentkit registry identity drift")
                try:
                    lock = load(stable_root / "donors.json")
                    locked = {item.get("name"): item for item in lock.get("donors", [])}
                    if set(locked) != set(DONORS) or lock.get("pack_version") != released.get("version"):
                        failures.append("released agentkit donor lock identity drift")
                    for donor in donors:
                        entry = locked.get(donor.get("name"), {})
                        if entry.get("version") != donor.get("version") or entry.get("source_tree_sha256") != donor.get("content_sha256"):
                            failures.append(f"released agentkit donor drift: {donor.get('name')}")
                    if list((stable_root / "vendor").rglob("SKILL.md")):
                        failures.append("released agentkit vendor contains nested discoverable SKILL.md")
                except (OSError, json.JSONDecodeError) as exc:
                    failures.append(f"invalid released agentkit lock: {exc}")
                for artifact_key in ("evaluation_plan", "evaluation_result"):
                    artifact = root / str(released.get(artifact_key, ""))
                    if not artifact.is_file():
                        failures.append(f"released agentkit missing {artifact_key}")
                        continue
                    try:
                        artifact_data = load(artifact)
                        artifact_hash = artifact_data.get("target", {}).get("hash") if artifact_key == "evaluation_plan" else artifact_data.get("target_hash")
                        if artifact_hash != released.get("content_sha256"):
                            failures.append(f"released agentkit {artifact_key} hash drift")
                    except json.JSONDecodeError as exc:
                        failures.append(f"invalid released agentkit {artifact_key}: {exc}")
            catalog = load(root / "catalog" / "entries.json")
            if "agentkit" not in {item.get("name") for item in catalog.get("entries", [])}:
                failures.append("released agentkit is missing from catalog")
            if not (root / "plugins" / "agentkit").is_dir():
                failures.append("released agentkit is missing its generated plugin")
            for marketplace in (
                root / ".claude-plugin" / "marketplace.json",
                root / ".agents" / "plugins" / "marketplace.json",
                root / ".cursor-plugin" / "marketplace.json",
            ):
                manifest = load(marketplace)
                if "agentkit" not in {item.get("name") for item in manifest.get("plugins", [])}:
                    failures.append(f"released agentkit missing from {marketplace}")

    current_release = release.get("marketplace", {}).get("version")
    if cycles and semver(current_release) < semver(cycles[-1].get("release")):
        failures.append("catalog release cannot precede the latest stability cycle")
    if release.get("aggregate_plugin", {}).get("version") != current_release:
        failures.append("aggregate and marketplace release versions must match")
    return failures


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    ledger = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else root / "docs/agents/evals/individual-agent-stability-cycles.json"
    try:
        failures = validate(root, ledger)
    except (KeyError, TypeError, ValueError) as exc:
        failures = [str(exc)]
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    data = load(ledger)
    print(
        "PASS individual-agent donor stability: "
        f"{data['agentkit_gate']['stable_cycles_completed']}/{data['required_stable_cycles']} cycles"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
