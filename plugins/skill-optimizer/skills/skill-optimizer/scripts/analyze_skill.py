#!/usr/bin/env python3
"""Analyze the structure and static optimization signals of an agent skill."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|FIXME|TBD)\b|\[TODO[^\]]*\]", re.IGNORECASE)
ABSOLUTE_RE = re.compile(r"\b(?:always|never|must|всегда|никогда|обязан\w*)\b", re.IGNORECASE)


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

    values: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            return {}, f"Unsupported frontmatter syntax on line {number}."
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value[:1] == value[-1:] and value[:1] in {'"', "'"}:
            value = value[1:-1]
        values[key] = value
    return values, None


def normalized_paragraphs(text: str) -> list[str]:
    paragraphs: list[str] = []
    for block in re.split(r"\n\s*\n", text):
        value = re.sub(r"\s+", " ", block.strip().lower())
        if len(value) >= 100 and not value.startswith("```"):
            paragraphs.append(value)
    return paragraphs


def relative_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file())


def resource_count(files: list[Path], root: Path, folder: str) -> int:
    target = root / folder
    return sum(target in path.parents for path in files)


def analyze(root: Path) -> dict[str, object]:
    findings: list[Finding] = []
    metrics: dict[str, int] = {}
    if not root.is_dir():
        add(findings, "error", "path", "Skill path is not a directory.", root)
        return build_report(root, metrics, findings)

    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        add(findings, "error", "skill-file", "SKILL.md is missing.", skill_file)
        return build_report(root, metrics, findings)

    files = relative_files(root)
    skill_text = skill_file.read_text(encoding="utf-8")
    frontmatter, frontmatter_error = parse_frontmatter(skill_text)
    if frontmatter_error:
        add(findings, "error", "frontmatter", frontmatter_error, skill_file)

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if set(frontmatter) != {"name", "description"}:
        add(
            findings,
            "error",
            "frontmatter-keys",
            "Frontmatter should contain exactly name and description.",
            skill_file,
        )
    if not NAME_RE.fullmatch(name) or len(name) > 63:
        add(findings, "error", "name", "Skill name is invalid.", skill_file)
    if name and name != root.name:
        add(
            findings,
            "error",
            "folder-name",
            f"Folder '{root.name}' does not match skill name '{name}'.",
            root,
        )
    if not 20 <= len(description) <= 1024:
        add(
            findings,
            "error",
            "description-length",
            "Description should contain 20 to 1024 characters.",
            skill_file,
        )
    if description and not re.search(r"\b(?:use|when|for|использ|когда|для)\b", description, re.IGNORECASE):
        add(
            findings,
            "info",
            "description-trigger",
            "Description may not state concrete trigger context.",
            skill_file,
        )

    skill_lines = len(skill_text.splitlines())
    if skill_lines > 500:
        add(
            findings,
            "warning",
            "skill-size",
            f"SKILL.md has {skill_lines} lines; inspect progressive disclosure.",
            skill_file,
        )
    if PLACEHOLDER_RE.search(skill_text):
        add(findings, "error", "placeholder", "Unresolved placeholder found.", skill_file)

    headings = [value.strip().lower() for value in HEADING_RE.findall(skill_text)]
    duplicate_headings = [key for key, count in Counter(headings).items() if count > 1]
    for heading in duplicate_headings:
        add(
            findings,
            "warning",
            "duplicate-heading",
            f"Duplicate heading: {heading}",
            skill_file,
        )

    paragraphs = normalized_paragraphs(skill_text)
    duplicate_paragraphs = [
        key for key, count in Counter(paragraphs).items() if count > 1
    ]
    if duplicate_paragraphs:
        add(
            findings,
            "warning",
            "duplicate-paragraph",
            f"Found {len(duplicate_paragraphs)} duplicated long paragraph(s).",
            skill_file,
        )

    broken_links = 0
    markdown_files = [path for path in files if path.suffix.lower() == ".md"]
    all_markdown = "\n".join(
        path.read_text(encoding="utf-8", errors="replace") for path in markdown_files
    )
    for source in markdown_files:
        text = source.read_text(encoding="utf-8", errors="replace")
        if source != skill_file and source.parent.name in {"references", "prompts"}:
            if PLACEHOLDER_RE.search(text):
                add(findings, "error", "placeholder", "Unresolved placeholder found.", source)
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
                broken_links += 1
                add(
                    findings,
                    "error",
                    "broken-link",
                    f"Linked resource does not exist: {raw_target}",
                    source,
                )

    for path in files:
        relative = path.relative_to(root).as_posix()
        if path.stat().st_size == 0:
            add(findings, "error", "empty-file", "File is empty.", path)
        if path.name == ".DS_Store" or path.suffix in {".pyc", ".pyo"}:
            add(findings, "warning", "junk-file", "Generated junk file found.", path)
        if path.suffix == ".py":
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except (SyntaxError, UnicodeDecodeError) as exc:
                add(findings, "error", "python-syntax", f"Invalid Python: {exc}", path)
        if path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                add(findings, "error", "json-syntax", f"Invalid JSON: {exc}", path)
        if path.parent.name in {"references", "scripts", "assets", "prompts", "evals"}:
            if relative not in skill_text and path.name not in all_markdown:
                add(
                    findings,
                    "info",
                    "resource-routing",
                    f"Resource is not named in SKILL.md or another Markdown file: {relative}",
                    path,
                )

    openai_yaml = root / "agents" / "openai.yaml"
    if openai_yaml.exists():
        yaml_text = openai_yaml.read_text(encoding="utf-8", errors="replace")
        if name and f"${name}" not in yaml_text:
            add(
                findings,
                "warning",
                "default-prompt",
                f"agents/openai.yaml may not mention ${name} in default_prompt.",
                openai_yaml,
            )
    else:
        add(
            findings,
            "info",
            "openai-yaml",
            "agents/openai.yaml is absent; confirm whether the host needs UI metadata.",
            openai_yaml,
        )

    metrics.update(
        {
            "total_files": len(files),
            "total_bytes": sum(path.stat().st_size for path in files),
            "skill_lines": skill_lines,
            "skill_chars": len(skill_text),
            "skill_words": len(re.findall(r"\S+", skill_text)),
            "description_chars": len(description),
            "markdown_files": len(markdown_files),
            "script_files": resource_count(files, root, "scripts"),
            "reference_files": resource_count(files, root, "references"),
            "asset_files": resource_count(files, root, "assets"),
            "prompt_files": resource_count(files, root, "prompts"),
            "eval_files": resource_count(files, root, "evals"),
            "headings": len(headings),
            "absolute_terms": len(ABSOLUTE_RE.findall(skill_text)),
            "duplicate_headings": len(duplicate_headings),
            "duplicate_paragraphs": len(duplicate_paragraphs),
            "broken_links": broken_links,
        }
    )
    return build_report(root, metrics, findings)


def build_report(
    root: Path, metrics: dict[str, int], findings: list[Finding]
) -> dict[str, object]:
    counts = {
        severity: sum(item.severity == severity for item in findings)
        for severity in ("error", "warning", "info")
    }
    return {
        "skill": str(root.resolve()),
        "metrics": metrics,
        "counts": counts,
        "findings": [asdict(item) for item in findings],
    }


def render_text(report: dict[str, object]) -> str:
    lines = [f"Skill: {report['skill']}"]
    counts = report["counts"]
    assert isinstance(counts, dict)
    lines.append(
        f"Findings: {counts['error']} errors, {counts['warning']} warnings, {counts['info']} info"
    )
    metrics = report["metrics"]
    assert isinstance(metrics, dict)
    if metrics:
        lines.append("Metrics:")
        lines.extend(f"  {key}: {value}" for key, value in sorted(metrics.items()))
    for item in report["findings"]:
        assert isinstance(item, dict)
        location = f" ({item['path']})" if item.get("path") else ""
        lines.append(
            f"[{str(item['severity']).upper()}] {item['code']}: {item['message']}{location}"
        )
    if not report["findings"]:
        lines.append("No static findings.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_path", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--fail-on", choices=("none", "error", "warning"), default="none"
    )
    args = parser.parse_args()

    report = analyze(args.skill_path.expanduser().resolve())
    rendered = (
        json.dumps(report, ensure_ascii=False, indent=2)
        if args.format == "json"
        else render_text(report)
    )
    if args.output:
        output = args.output.expanduser().resolve()
        if not output.parent.is_dir():
            print(f"Output directory does not exist: {output.parent}", file=sys.stderr)
            return 2
        output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Report written to {output}", file=sys.stderr)
    else:
        print(rendered)

    counts = report["counts"]
    assert isinstance(counts, dict)
    if args.fail_on == "warning" and (counts["error"] or counts["warning"]):
        return 1
    if args.fail_on == "error" and counts["error"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

