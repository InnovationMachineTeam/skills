#!/usr/bin/env python3
"""Portable structural validator for SKILL.md-based agent skills."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|FIXME|TBD)\b|\[TODO[^\]]*\]", re.IGNORECASE)
ARCHETYPES = {
    "knowledge-reference",
    "workflow-procedure",
    "tool-integration",
    "script-automation",
    "artifact-template",
    "evaluation-review",
    "orchestration",
    "meta-router",
}


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    path: str | None = None


def add(
    findings: list[Finding],
    severity: str,
    code: str,
    message: str,
    path: Path | None = None,
) -> None:
    findings.append(
        Finding(severity, code, message, str(path) if path is not None else None)
    )


def parse_frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "SKILL.md must start with YAML frontmatter."
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, "SKILL.md frontmatter is not closed."

    data: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return {}, f"Unsupported frontmatter syntax on line {number}."
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            return {}, f"Empty frontmatter key or value on line {number}."
        if value[:1] == value[-1:] and value[:1] in {'"', "'"}:
            value = value[1:-1]
        data[key] = value
    return data, None


def validate_frontmatter(root: Path, skill_file: Path, findings: list[Finding]) -> str | None:
    text = skill_file.read_text(encoding="utf-8")
    frontmatter, error = parse_frontmatter(text)
    if error:
        add(findings, "error", "frontmatter", error, skill_file)
        return None

    keys = set(frontmatter)
    required = {"name", "description"}
    if keys != required:
        add(
            findings,
            "error",
            "frontmatter-keys",
            "Frontmatter must contain exactly name and description; found: "
            + ", ".join(sorted(keys)),
            skill_file,
        )

    name = frontmatter.get("name")
    description = frontmatter.get("description", "")
    if name:
        if len(name) > 63 or not NAME_RE.fullmatch(name):
            add(
                findings,
                "error",
                "name",
                "Skill name must be under 64 characters and use lowercase letters, digits, and single hyphens.",
                skill_file,
            )
        if root.name != name:
            add(
                findings,
                "error",
                "folder-name",
                f"Folder name '{root.name}' does not match skill name '{name}'.",
                root,
            )
    else:
        add(findings, "error", "name-missing", "Skill name is missing.", skill_file)

    if len(description.strip()) < 20:
        add(
            findings,
            "error",
            "description",
            "Description is too short to explain capability and trigger context.",
            skill_file,
        )

    line_count = len(text.splitlines())
    if line_count > 500:
        add(
            findings,
            "warning",
            "skill-size",
            f"SKILL.md has {line_count} lines; move conditional details to resources.",
            skill_file,
        )
    return name


def iter_markdown(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def validate_links(root: Path, findings: list[Finding]) -> None:
    for source in iter_markdown(root):
        text = source.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
                continue
            resolved = (source.parent / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                add(
                    findings,
                    "warning",
                    "external-relative-link",
                    f"Relative link leaves the skill folder: {raw_target}",
                    source,
                )
                continue
            if not resolved.exists():
                add(
                    findings,
                    "error",
                    "broken-link",
                    f"Linked resource does not exist: {raw_target}",
                    source,
                )


def validate_placeholders(root: Path, findings: list[Finding]) -> None:
    candidates = [root / "SKILL.md"]
    for folder in ("references", "prompts"):
        if (root / folder).is_dir():
            candidates.extend(sorted((root / folder).rglob("*.md")))
    for path in candidates:
        if path.is_file() and PLACEHOLDER_RE.search(path.read_text(encoding="utf-8")):
            add(
                findings,
                "error",
                "placeholder",
                "Unresolved TODO, FIXME, or TBD marker found.",
                path,
            )


def yaml_string(text: str, key: str) -> str | None:
    match = re.search(
        rf"^\s*{re.escape(key)}:\s*([\"'])(.*?)\1\s*$", text, re.MULTILINE
    )
    return match.group(2) if match else None


def validate_openai_yaml(root: Path, name: str | None, findings: list[Finding]) -> None:
    path = root / "agents" / "openai.yaml"
    if not path.exists():
        add(
            findings,
            "warning",
            "openai-yaml",
            "agents/openai.yaml is recommended for UI discovery.",
            path,
        )
        return
    text = path.read_text(encoding="utf-8")
    for key in ("display_name", "short_description", "default_prompt"):
        if yaml_string(text, key) is None:
            add(
                findings,
                "error",
                "openai-yaml-field",
                f"{key} must exist and use a quoted string value.",
                path,
            )
    short = yaml_string(text, "short_description")
    if short is not None and not 25 <= len(short) <= 64:
        add(
            findings,
            "error",
            "short-description-length",
            "short_description must contain 25 to 64 characters.",
            path,
        )
    default = yaml_string(text, "default_prompt")
    if name and default is not None and f"${name}" not in default:
        add(
            findings,
            "error",
            "default-prompt",
            f"default_prompt must explicitly mention ${name}.",
            path,
        )


def validate_eval_payload(
    path: Path, payload: object, root_name: str, findings: list[Finding]
) -> None:
    if not isinstance(payload, dict):
        add(findings, "error", "eval-shape", "Eval root must be an object.", path)
        return
    if payload.get("skill") != root_name:
        add(
            findings,
            "error",
            "eval-skill-name",
            f"Eval must identify skill '{root_name}'.",
            path,
        )
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        add(
            findings,
            "error",
            "eval-cases",
            "Eval must contain a non-empty cases array.",
            path,
        )
        return

    ids: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            add(
                findings,
                "error",
                "eval-case-shape",
                f"Case {index} must be an object.",
                path,
            )
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            add(
                findings,
                "error",
                "eval-case-id",
                f"Case {index} requires a non-empty string id.",
                path,
            )
        elif case_id in ids:
            add(
                findings,
                "error",
                "eval-case-id",
                f"Duplicate eval case id: {case_id}",
                path,
            )
        else:
            ids.add(case_id)

    if path.name == "routing.json":
        routed = {
            case.get("expected_primary_archetype")
            for case in cases
            if isinstance(case, dict)
        }
        missing = ARCHETYPES - routed
        if missing:
            add(
                findings,
                "error",
                "routing-coverage",
                "Routing cases do not cover archetypes: " + ", ".join(sorted(missing)),
                path,
            )
        trigger_values = {
            case.get("expected_trigger") for case in cases if isinstance(case, dict)
        }
        if not {True, False}.issubset(trigger_values):
            add(
                findings,
                "error",
                "trigger-coverage",
                "Routing eval must include positive and negative trigger cases.",
                path,
            )
        actions = {
            case.get("expected_action") for case in cases if isinstance(case, dict)
        }
        for required in ("classify-and-create", "clarify", "do-not-trigger"):
            if required not in actions:
                add(
                    findings,
                    "error",
                    "routing-action-coverage",
                    f"Routing eval is missing action '{required}'.",
                    path,
                )

    if path.name == "behavior.json":
        for case in cases:
            if not isinstance(case, dict):
                continue
            for key in ("expected_properties", "forbidden_properties"):
                value = case.get(key)
                if not isinstance(value, list) or not value:
                    add(
                        findings,
                        "error",
                        "behavior-properties",
                        f"Behavior case '{case.get('id', '?')}' requires non-empty {key}.",
                        path,
                    )


def validate_files(root: Path, findings: list[Finding]) -> None:
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        if path.name == ".DS_Store" or path.suffix in {".pyc", ".pyo"}:
            add(
                findings,
                "warning",
                "junk-file",
                "Remove generated operating-system or bytecode files from the skill bundle.",
                path,
            )
        if path.stat().st_size == 0:
            add(findings, "error", "empty-file", "File is empty.", path)
        if path.suffix == ".py":
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except (SyntaxError, UnicodeDecodeError) as exc:
                add(
                    findings,
                    "error",
                    "python-syntax",
                    f"Python source is invalid: {exc}",
                    path,
                )
        if path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                add(
                    findings,
                    "error",
                    "json-syntax",
                    f"JSON resource is invalid: {exc}",
                    path,
                )

    for folder_name in ("scripts", "references", "assets", "prompts", "evals"):
        folder = root / folder_name
        if folder.is_dir() and not any(item.is_file() for item in folder.rglob("*")):
            add(
                findings,
                "warning",
                "empty-resource-folder",
                f"Remove unused empty resource folder '{folder_name}'.",
                folder,
            )

    legacy_prompts = root / "master-prompts"
    if legacy_prompts.exists():
        add(
            findings,
            "error",
            "legacy-prompt-folder",
            "Use prompts/ rather than master-prompts/ for routed prompt resources.",
            legacy_prompts,
        )

    prompts = root / "prompts"
    if prompts.is_dir():
        if not (prompts / "base.md").is_file():
            add(
                findings,
                "error",
                "master-prompt-base",
                "prompts/base.md is required when routed prompts are present.",
                prompts,
            )
        variants = [path for path in prompts.glob("*.md") if path.name != "base.md"]
        if not variants:
            add(
                findings,
                "error",
                "master-prompt-variants",
                "At least one routed master prompt is required.",
                prompts,
            )

    evals = root / "evals"
    if evals.is_dir():
        for filename in ("routing.json", "behavior.json"):
            path = evals / filename
            if not path.is_file():
                add(
                    findings,
                    "error",
                    "eval-file",
                    f"evals/{filename} is required for this meta-skill.",
                    path,
                )
                continue
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue
            validate_eval_payload(path, payload, root.name, findings)


def validate(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not root.is_dir():
        add(findings, "error", "path", "Skill path is not a directory.", root)
        return findings
    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        add(findings, "error", "skill-file", "SKILL.md is missing.", skill_file)
        return findings

    name = validate_frontmatter(root, skill_file, findings)
    validate_links(root, findings)
    validate_placeholders(root, findings)
    validate_openai_yaml(root, name, findings)
    validate_files(root, findings)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_path", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument(
        "--fail-on", choices=("error", "warning"), default="error"
    )
    args = parser.parse_args()

    root = args.skill_path.expanduser().resolve()
    findings = validate(root)
    counts = {
        severity: sum(item.severity == severity for item in findings)
        for severity in ("error", "warning")
    }

    if args.format == "json":
        print(
            json.dumps(
                {
                    "skill": str(root),
                    "counts": counts,
                    "findings": [asdict(item) for item in findings],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(f"Skill: {root}")
        print(f"Findings: {counts['error']} errors, {counts['warning']} warnings")
        for item in findings:
            location = f" ({item.path})" if item.path else ""
            print(f"[{item.severity.upper()}] {item.code}: {item.message}{location}")
        if not findings:
            print("No structural findings.")

    if counts["error"]:
        return 1
    if args.fail_on == "warning" and counts["warning"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
