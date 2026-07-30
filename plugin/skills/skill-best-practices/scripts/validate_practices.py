#!/usr/bin/env python3
"""Validate the regenerated best-practices corpus and source references."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


REQUIRED_FILES = {
    "INDEX.md",
    "01-specification-and-portability.md",
    "02-authoring-and-progressive-disclosure.md",
    "03-descriptions-discovery-and-routing.md",
    "04-workflows-scripts-and-tools.md",
    "05-evaluation-and-optimization.md",
    "06-security-and-authority.md",
    "07-client-implementation.md",
    "08-enterprise-lifecycle-and-governance.md",
    "09-meta-skills-and-orchestration.md",
    "10-conflicts-and-decisions.md",
    "11-checklists.md",
}
HEADER_PATTERN = re.compile(r"^(Practice-ID|Scope|Status|Sources|Last-rebuilt|Revision):\s*(.+)$", re.MULTILINE)
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+\.md)\)")
SECTION_PATTERN = re.compile(r"^##\s+(.+)$", re.MULTILINE)
HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


@dataclass
class Finding:
    code: str
    message: str
    path: str


def section_map(path: Path, text: str) -> dict[tuple[str, str], str]:
    matches = list(SECTION_PATTERN.finditer(text))
    if not matches:
        return {(path.name, "__document__"): text.strip()}
    result: dict[tuple[str, str], str] = {(path.name, "__preamble__"): text[:matches[0].start()].strip()}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        key = (path.name, match.group(1).strip())
        if key in result:
            raise ValueError(f"duplicate level-two heading: {key[1]}")
        result[key] = text[match.start():end].strip()
    return result


def digest_files(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.name):
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return "sha256:" + digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("practices", type=Path)
    parser.add_argument("registry", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.practices.expanduser().resolve()
    registry_path = args.registry.expanduser().resolve()
    findings: list[Finding] = []
    try:
        registry_bytes = registry_path.read_bytes()
        registry = json.loads(registry_bytes.decode("utf-8"))
        source_ids = {item["id"] for item in registry["sources"] if isinstance(item, dict) and isinstance(item.get("id"), str)}
        registry_hash = "sha256:" + hashlib.sha256(registry_bytes).hexdigest()
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        findings.append(Finding("registry", f"cannot read registry: {exc}", str(registry_path)))
        source_ids = set()
        registry_hash = None
    revision = None
    actual_sections: dict[tuple[str, str], str] = {}
    if not root.is_dir():
        findings.append(Finding("directory", "practices directory does not exist", str(root)))
    else:
        actual = {path.name for path in root.glob("*.md")}
        for name in sorted(REQUIRED_FILES - actual):
            findings.append(Finding("missing-file", f"missing required file: {name}", str(root)))
        ids: set[str] = set()
        for path in sorted(root.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            try:
                actual_sections.update(section_map(path, text))
            except ValueError as exc:
                findings.append(Finding("duplicate-heading", str(exc), str(path)))
            headers = dict(HEADER_PATTERN.findall("\n".join(text.splitlines()[:16])))
            for key in ("Practice-ID", "Scope", "Status", "Sources", "Last-rebuilt"):
                if not headers.get(key):
                    findings.append(Finding("header", f"missing {key} header", str(path)))
            practice_id = headers.get("Practice-ID")
            if practice_id:
                if practice_id in ids:
                    findings.append(Finding("practice-id", f"duplicate Practice-ID: {practice_id}", str(path)))
                ids.add(practice_id)
            try:
                date.fromisoformat(headers.get("Last-rebuilt", ""))
            except ValueError:
                findings.append(Finding("date", "Last-rebuilt must be YYYY-MM-DD", str(path)))
            referenced = [item.strip() for item in headers.get("Sources", "").split(",") if item.strip()]
            if not referenced:
                findings.append(Finding("sources", "Sources must include at least one source ID", str(path)))
            for source_id in referenced:
                if source_id not in source_ids:
                    findings.append(Finding("source-id", f"unknown source ID: {source_id}", str(path)))
            for target in LINK_PATTERN.findall(text):
                if target.startswith(("http://", "https://")):
                    continue
                resolved = (path.parent / target).resolve()
                if not resolved.is_file():
                    findings.append(Finding("link", f"broken Markdown link: {target}", str(path)))
        index = root / "INDEX.md"
        if index.is_file():
            index_text = index.read_text(encoding="utf-8")
            revision_match = re.search(r"^Revision:\s*(.+)$", "\n".join(index_text.splitlines()[:16]), re.MULTILINE)
            if not revision_match:
                findings.append(Finding("revision", "INDEX.md must declare Revision", str(index)))
            else:
                revision = revision_match.group(1).strip()
            linked_names = {Path(target).name for target in LINK_PATTERN.findall(index_text)}
            for name in sorted((REQUIRED_FILES - {"INDEX.md"}) - linked_names):
                findings.append(Finding("index-coverage", f"INDEX.md does not link required topic: {name}", str(index)))

        claims_path = root / "claims.json"
        try:
            claims_root = json.loads(claims_path.read_text(encoding="utf-8"))
            claims = claims_root["claims"]
            if claims_root.get("schema_version") != 1 or not isinstance(claims, list):
                raise ValueError("claims root must use schema_version 1 and a claims array")
            if claims_root.get("practices_revision") != revision:
                findings.append(Finding("claims-revision", "claims revision does not match INDEX.md", str(claims_path)))
            seen_ids: set[str] = set()
            seen_sections: set[tuple[str, str]] = set()
            seen_hashes: set[str] = set()
            for number, claim in enumerate(claims):
                if not isinstance(claim, dict):
                    findings.append(Finding("claim-shape", f"claim {number} must be an object", str(claims_path)))
                    continue
                claim_id = claim.get("claim_id")
                key = (claim.get("file"), claim.get("section"))
                claim_sources = claim.get("sources")
                text_hash = claim.get("text_sha256")
                if not isinstance(claim_id, str) or not claim_id or claim_id in seen_ids:
                    findings.append(Finding("claim-id", f"claim {number} needs a unique claim_id", str(claims_path)))
                else:
                    seen_ids.add(claim_id)
                if not all(isinstance(item, str) and item for item in key) or key in seen_sections:
                    findings.append(Finding("claim-owner", f"claim {number} needs one unique file/section owner", str(claims_path)))
                    continue
                seen_sections.add(key)
                if key not in actual_sections:
                    findings.append(Finding("claim-section", f"claim references missing section: {key[0]}#{key[1]}", str(claims_path)))
                if not isinstance(claim_sources, list) or not claim_sources:
                    findings.append(Finding("claim-sources", f"claim {number} needs source IDs", str(claims_path)))
                else:
                    for source_id in claim_sources:
                        if source_id not in source_ids:
                            findings.append(Finding("claim-source-id", f"unknown claim source ID: {source_id}", str(claims_path)))
                if not isinstance(text_hash, str) or not HASH_PATTERN.fullmatch(text_hash):
                    findings.append(Finding("claim-hash", f"claim {number} needs a sha256 text hash", str(claims_path)))
                elif key in actual_sections:
                    actual_hash = "sha256:" + hashlib.sha256(actual_sections[key].encode("utf-8")).hexdigest()
                    if actual_hash != text_hash:
                        findings.append(Finding("claim-drift", f"section text changed without claim-manifest update: {key[0]}#{key[1]}", str(claims_path)))
                    if text_hash in seen_hashes:
                        findings.append(Finding("duplicate-rule", f"identical section content has multiple owners: {text_hash}", str(claims_path)))
                    seen_hashes.add(text_hash)
            for key in sorted(set(actual_sections) - seen_sections):
                findings.append(Finding("claim-coverage", f"section lacks provenance record: {key[0]}#{key[1]}", str(claims_path)))
            for key in sorted(seen_sections - set(actual_sections)):
                findings.append(Finding("claim-orphan", f"provenance record has no section: {key[0]}#{key[1]}", str(claims_path)))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            findings.append(Finding("claims", f"cannot read claims manifest: {exc}", str(claims_path)))

    corpus_files = sorted(root.glob("*.md")) + ([root / "claims.json"] if (root / "claims.json").is_file() else [])
    payload = {
        "schema_version": 1,
        "valid": not findings,
        "count": len(findings),
        "practices_revision": revision,
        "corpus_hash": digest_files(corpus_files) if corpus_files else None,
        "registry_hash": registry_hash,
        "findings": [asdict(item) for item in findings],
    }
    if args.output:
        output = args.output.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Findings: {len(findings)}")
        for finding in findings:
            print(f"[ERROR] {finding.code}: {finding.message} ({finding.path})")
        if not findings:
            print("Best-practices corpus is structurally valid.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
