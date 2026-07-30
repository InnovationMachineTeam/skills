#!/usr/bin/env python3
"""Run read-only static health checks on a SKILL.md-based agent skill."""

from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|FIXME|TBD)\b|\[TODO[^\]]*\]", re.IGNORECASE)
SECRET_RE = re.compile(
    r"(?i)\b(?:api[_-]?key|access[_-]?token|secret|password)\b\s*[:=]\s*['\"]([^$<{\s][^'\"]{7,})['\"]"
)
HEALTH_ORDER = {"HEALTHY": 0, "DEGRADED": 1, "BROKEN": 2, "UNSAFE": 3}


@dataclass
class Finding:
    severity: str
    health_impact: str
    domain: str
    code: str
    message: str
    path: str | None = None


def add(
    findings: list[Finding],
    severity: str,
    health_impact: str,
    domain: str,
    code: str,
    message: str,
    path: Path | None = None,
) -> None:
    findings.append(
        Finding(
            severity,
            health_impact,
            domain,
            code,
            message,
            str(path) if path is not None else None,
        )
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
        if not key or not value:
            return {}, f"Empty frontmatter field on line {number}."
        if value[:1] == value[-1:] and value[:1] in {'"', "'"}:
            value = value[1:-1]
        values[key] = value
    return values, None


def files_under(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file())


def check_shell(path: Path, findings: list[Finding]) -> None:
    bash = shutil.which("bash")
    if bash is None:
        add(
            findings,
            "LOW",
            "DEGRADED",
            "scripts-dependencies",
            "bash-unavailable",
            "Shell syntax check was requested but bash is unavailable.",
            path,
        )
        return
    result = subprocess.run(
        [bash, "-n", str(path)], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "syntax error"
        add(
            findings,
            "HIGH",
            "BROKEN",
            "scripts-dependencies",
            "shell-syntax",
            f"Shell syntax check failed: {detail}",
            path,
        )


def diagnose(root: Path, check_shell_scripts: bool) -> dict[str, object]:
    findings: list[Finding] = []
    metrics: dict[str, int] = {}
    checks = ["filesystem", "frontmatter", "links", "python-syntax", "json-syntax"]
    if check_shell_scripts:
        checks.append("shell-syntax")

    if not root.is_dir():
        add(findings, "BLOCK", "BROKEN", "packaging-portability", "path", "Skill path is not a directory.", root)
        return report(root, metrics, checks, findings)
    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        add(findings, "BLOCK", "BROKEN", "metadata-discovery", "skill-file", "SKILL.md is missing.", skill_file)
        return report(root, metrics, checks, findings)

    files = files_under(root)
    skill_text = skill_file.read_text(encoding="utf-8", errors="replace")
    frontmatter, error = parse_frontmatter(skill_text)
    if error:
        add(findings, "BLOCK", "BROKEN", "metadata-discovery", "frontmatter", error, skill_file)

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if set(frontmatter) != {"name", "description"}:
        add(
            findings,
            "HIGH",
            "BROKEN",
            "metadata-discovery",
            "frontmatter-keys",
            "Frontmatter must contain exactly name and description.",
            skill_file,
        )
    if not NAME_RE.fullmatch(name) or len(name) > 63:
        add(findings, "HIGH", "BROKEN", "metadata-discovery", "name", "Skill name is invalid.", skill_file)
    if name and name != root.name:
        add(
            findings,
            "HIGH",
            "BROKEN",
            "packaging-portability",
            "folder-name",
            f"Folder '{root.name}' does not match skill name '{name}'.",
            root,
        )
    if not 20 <= len(description) <= 1024:
        add(
            findings,
            "MEDIUM",
            "DEGRADED",
            "metadata-discovery",
            "description-length",
            "Description should contain 20 to 1024 characters.",
            skill_file,
        )
    if PLACEHOLDER_RE.search(skill_text):
        add(findings, "HIGH", "BROKEN", "metadata-discovery", "placeholder", "Unresolved placeholder found in SKILL.md.", skill_file)
    skill_lines = len(skill_text.splitlines())
    if skill_lines > 500:
        add(
            findings,
            "LOW",
            "DEGRADED",
            "context-resources",
            "skill-size",
            f"SKILL.md has {skill_lines} lines; inspect progressive disclosure.",
            skill_file,
        )

    markdown_files = [path for path in files if path.suffix.lower() == ".md"]
    linked_targets: set[Path] = set()
    broken_links = 0
    for source in markdown_files:
        text = source.read_text(encoding="utf-8", errors="replace")
        if source != skill_file and source.parent.name in {"references", "prompts"} and PLACEHOLDER_RE.search(text):
            add(findings, "HIGH", "BROKEN", "context-resources", "placeholder", "Unresolved placeholder found.", source)
        for raw in LINK_RE.findall(text):
            target = raw.strip().strip("<>").split("#", 1)[0]
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
                continue
            resolved = (source.parent / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                add(
                    findings,
                    "LOW",
                    "DEGRADED",
                    "context-resources",
                    "external-relative-link",
                    f"Relative link leaves the skill folder: {raw}",
                    source,
                )
                continue
            linked_targets.add(resolved)
            if not resolved.exists():
                broken_links += 1
                add(
                    findings,
                    "HIGH",
                    "BROKEN",
                    "context-resources",
                    "broken-link",
                    f"Linked resource does not exist: {raw}",
                    source,
                )

    for path in files:
        if path.stat().st_size == 0:
            add(findings, "HIGH", "BROKEN", "packaging-portability", "empty-file", "File is empty.", path)
        if path.name == ".DS_Store" or path.suffix in {".pyc", ".pyo"}:
            add(findings, "LOW", "DEGRADED", "packaging-portability", "junk-file", "Generated junk file found.", path)
        if path.suffix == ".py":
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except (SyntaxError, UnicodeDecodeError) as exc:
                add(findings, "HIGH", "BROKEN", "scripts-dependencies", "python-syntax", f"Invalid Python: {exc}", path)
        if path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                add(findings, "HIGH", "BROKEN", "evals-regressions", "json-syntax", f"Invalid JSON: {exc}", path)
        if check_shell_scripts and path.suffix in {".sh", ".bash"}:
            check_shell(path, findings)
        if path.parent.name in {"scripts", "agents"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            if SECRET_RE.search(text):
                add(
                    findings,
                    "BLOCK",
                    "UNSAFE",
                    "security-authority",
                    "embedded-secret",
                    "Possible literal credential embedded in executable or host metadata.",
                    path,
                )

    openai_yaml = root / "agents" / "openai.yaml"
    if openai_yaml.is_file():
        yaml_text = openai_yaml.read_text(encoding="utf-8", errors="replace")
        if name and f"${name}" not in yaml_text:
            add(
                findings,
                "LOW",
                "DEGRADED",
                "metadata-discovery",
                "default-prompt",
                f"agents/openai.yaml may not mention ${name} in default_prompt.",
                openai_yaml,
            )

    for folder_name in ("scripts", "references", "assets", "prompts", "evals"):
        folder = root / folder_name
        if folder.is_dir() and not any(path.is_file() for path in folder.rglob("*")):
            add(
                findings,
                "LOW",
                "DEGRADED",
                "packaging-portability",
                "empty-resource-folder",
                f"Resource folder '{folder_name}' is empty.",
                folder,
            )

    metrics.update(
        {
            "total_files": len(files),
            "total_bytes": sum(path.stat().st_size for path in files),
            "skill_lines": skill_lines,
            "description_chars": len(description),
            "markdown_files": len(markdown_files),
            "script_files": sum((root / "scripts") in path.parents for path in files),
            "reference_files": sum((root / "references") in path.parents for path in files),
            "prompt_files": sum((root / "prompts") in path.parents for path in files),
            "eval_files": sum((root / "evals") in path.parents for path in files),
            "broken_links": broken_links,
        }
    )
    return report(root, metrics, checks, findings)


def report(
    root: Path,
    metrics: dict[str, int],
    checks: list[str],
    findings: list[Finding],
) -> dict[str, object]:
    health = "HEALTHY"
    for item in findings:
        if HEALTH_ORDER[item.health_impact] > HEALTH_ORDER[health]:
            health = item.health_impact
    severities = ("BLOCK", "HIGH", "MEDIUM", "LOW")
    counts = {severity: sum(item.severity == severity for item in findings) for severity in severities}
    return {
        "skill": str(root.resolve()),
        "health": health,
        "checks_run": checks,
        "metrics": metrics,
        "counts": counts,
        "findings": [asdict(item) for item in findings],
        "scope_note": "Static health is scoped to checks_run and does not prove functional recovery.",
    }


def render_text(payload: dict[str, object]) -> str:
    lines = [f"Skill: {payload['skill']}", f"Health: {payload['health']}"]
    counts = payload["counts"]
    assert isinstance(counts, dict)
    lines.append(
        "Findings: " + ", ".join(f"{key}={value}" for key, value in counts.items())
    )
    metrics = payload["metrics"]
    assert isinstance(metrics, dict)
    if metrics:
        lines.append("Metrics:")
        lines.extend(f"  {key}: {value}" for key, value in sorted(metrics.items()))
    for item in payload["findings"]:
        assert isinstance(item, dict)
        location = f" ({item['path']})" if item.get("path") else ""
        lines.append(
            f"[{item['severity']}] {item['domain']}/{item['code']}: {item['message']}{location}"
        )
    lines.append(str(payload["scope_note"]))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_path", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-shell-syntax", action="store_true")
    parser.add_argument(
        "--fail-on", choices=("none", "degraded", "broken", "unsafe"), default="none"
    )
    args = parser.parse_args()

    payload = diagnose(args.skill_path.expanduser().resolve(), args.check_shell_syntax)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_text(payload)
    if args.output:
        output = args.output.expanduser().resolve()
        if not output.parent.is_dir():
            print(f"Output directory does not exist: {output.parent}", file=sys.stderr)
            return 2
        output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Report written to {output}", file=sys.stderr)
    else:
        print(rendered)

    threshold = {"none": 4, "degraded": 1, "broken": 2, "unsafe": 3}[args.fail_on]
    return 1 if HEALTH_ORDER[str(payload["health"])] >= threshold else 0


if __name__ == "__main__":
    sys.exit(main())

