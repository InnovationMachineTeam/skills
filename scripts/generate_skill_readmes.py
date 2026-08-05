#!/usr/bin/env python3
"""Generate evidence-backed usage sections for every canonical skill README."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


START = "<!-- generated-skill-readme:start -->"
END = "<!-- generated-skill-readme:end -->"
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def load_json(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def scalar(block: str, key: str) -> str:
    match = re.search(rf"^\s*{re.escape(key)}:\s*[\"']?([^\"'\n]+)", block, re.MULTILINE)
    return match.group(1).strip() if match else ""


def metadata(skill_file: Path) -> tuple[str, str, str, str]:
    text = skill_file.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        raise ValueError(f"missing frontmatter: {skill_file}")
    frontmatter = match.group(1)
    name = scalar(frontmatter, "name")
    description = scalar(frontmatter, "description")
    version = scalar(frontmatter, "version")
    if not name or not description or not version:
        raise ValueError(f"incomplete metadata: {skill_file}")
    return name, description, version, text[match.end():]


def sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]


def short_purpose(description: str) -> str:
    return sentences(description)[0].rstrip(".") + "."


def use_guidance(description: str) -> tuple[str, str]:
    use = ""
    avoid = ""
    use_match = re.search(r"\bUse (?:when|for) (.*?)(?=\s+(?:Do not use|Route |Ask |Default )|$)", description)
    avoid_match = re.search(r"\bDo not use (?:when|for) (.*?)(?=\s+(?:Route |Ask |Default )|$)", description)
    if use_match:
        use = use_match.group(1).strip().rstrip(".") + "."
        use = use[:1].upper() + use[1:]
    if avoid_match:
        avoid = avoid_match.group(1).strip().rstrip(".") + "."
        avoid = avoid[:1].upper() + avoid[1:]
    return use, avoid


def case_request(case: dict[str, Any]) -> str:
    for key in ("input", "prompt", "query", "request"):
        value = case.get(key)
        if value:
            return str(value)
    command = case.get("command")
    if isinstance(command, list):
        return " ".join(map(str, command))
    if command:
        return str(command)
    return "The scenario is described by its identifier and expected route in the eval corpus."


def positive_routes(data: dict[str, Any]) -> list[dict[str, Any]]:
    result = []
    for case in data.get("cases", []):
        if case.get("expected_trigger") is False:
            continue
        result.append(case)
    return result[:8]


def negative_routes(data: dict[str, Any]) -> list[dict[str, Any]]:
    return [case for case in data.get("cases", []) if case.get("expected_trigger") is False][:6]


def route_label(case: dict[str, Any]) -> str:
    for key in ("expected_route", "expected_primary_route", "expected_action", "expected_mode"):
        value = case.get(key)
        if value:
            return str(value)
    return "the skill's primary route"


def behavior_cases(data: dict[str, Any]) -> list[dict[str, Any]]:
    cases = []
    for case in data.get("cases", []):
        if case.get("expected_properties") or case.get("expected_output") or case.get("expected_result"):
            cases.append(case)
    return cases[:8]


def headings(body: str) -> list[str]:
    ignored = {"deliver", "complete", "completion", "output", "report", "role"}
    result = []
    for title in re.findall(r"^##\s+(.+?)\s*$", body, re.MULTILINE):
        normalized = re.sub(r"[`*_]", "", title).strip()
        if normalized.lower() in ignored:
            continue
        result.append(normalized)
    return result[:10]


def resource_rows(skill_dir: Path) -> list[tuple[str, str]]:
    descriptions = {
        "agents": "UI metadata and host configuration",
        "assets": "templates and reusable artifacts",
        "evals": "routing and behavior scenarios",
        "prompts": "routing and specialist prompts",
        "references": "reference guides, schemas, and contracts",
        "scripts": "deterministic checks and automation",
        "private-skills": "internal skills available only to the owner",
        "vendor": "pinned snapshot of dependent components",
    }
    result = []
    for child in sorted(skill_dir.iterdir(), key=lambda path: path.name):
        if child.is_dir() and child.name in descriptions:
            result.append((child.name, descriptions[child.name]))
    return result


def dependency_lines(name: str, graph: dict[str, Any]) -> list[str]:
    declaration = graph.get(name, {})
    lines = []
    for kind, label in (("required", "Required"), ("recommended", "Recommended")):
        for item in declaration.get(kind, []):
            reason = item.get("reason", "")
            lines.append(
                f"- **{label}: `{item['name']}` >= `{item['minimum_version']}`.** {reason}"
            )
    return lines


def private_owner(skill_dir: Path, root: Path) -> str | None:
    parts = skill_dir.relative_to(root).parts
    if "private-skills" not in parts:
        return None
    index = parts.index("private-skills")
    return parts[index - 1] if index > 0 else None


def visibility(skill_dir: Path, root: Path) -> str:
    owner = private_owner(skill_dir, root)
    if owner:
        return f"package-private: invoked only by its parent `{owner}` and not published separately"
    return "public: canonical catalog skill; actual activation depends on the target host"


def slash_invocation(command: str, request: str) -> str:
    request = request.strip().strip("“”\"")
    if request.startswith(f"/{command}"):
        return request
    return f"/{command} {request}"


def generated_block(
    root: Path,
    skill_dir: Path,
    name: str,
    description: str,
    version: str,
    body: str,
    tags: list[str],
    graph: dict[str, Any],
) -> str:
    routing = load_json(skill_dir / "evals" / "routing.json", {})
    behavior = load_json(skill_dir / "evals" / "behavior.json", {})
    use, avoid = use_guidance(description)
    routes = positive_routes(routing)
    negatives = negative_routes(routing)
    behaviors = behavior_cases(behavior)
    workflow = headings(body)
    resources = resource_rows(skill_dir)
    deps = dependency_lines(name, graph)

    lines = [
        START,
        "",
        "## Skill Profile",
        "",
        f"- **Purpose:** {short_purpose(description)}",
        f"- **Version:** `{version}`.",
        f"- **Visibility:** {visibility(skill_dir, root)}.",
    ]
    if tags:
        lines.append(f"- **Catalog tags:** {', '.join(f'`{tag}`' for tag in tags)}.")

    lines.extend(["", "## When To Use", ""])
    if use:
        lines.append(use)
    else:
        lines.append("Use the skill when the request matches its purpose and responsibility boundaries in `SKILL.md`.")
    lines.append("")
    lines.append("Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.")

    example_case = routes[0] if routes else {}
    example_request = case_request(example_case)
    expected_route = route_label(example_case)
    owner = private_owner(skill_dir, root)
    command_name = owner or name
    lines.extend(["", "## Full Command Example", ""])
    if owner:
        lines.append(f"This package-private skill is not invoked directly. The illustrative request is passed through its parent `/{owner}`:")
    else:
        lines.append("Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:")
    lines.extend([
        "",
        "```text",
        slash_invocation(command_name, example_request),
        "```",
        "",
        f"**Expected result:** route `{expected_route}` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.",
    ])
    if owner:
        lines.append(f"Direct `/{name}` is not a supported public command; parent `{owner}` must pass a bounded dispatch contract and verify the result.")

    lines.extend(["", "## Usage Variants", ""])
    if routes:
        for case in routes:
            lines.append(f"### {case.get('id', route_label(case))}")
            lines.append("")
            lines.append(f"- **Example request:** “{case_request(case)}”")
            lines.append(f"- **Expected route:** `{route_label(case)}`.")
            action = case.get("expected_action")
            if action and action != route_label(case):
                lines.append(f"- **Expected action:** `{action}`.")
            lines.append("")
    else:
        lines.extend([
            "- Explicitly invoke the skill to execute the primary contract from `SKILL.md`.",
            "- Audit or planning without changing files when write authority is not granted.",
            "- Apply allowed changes followed by result verification and rollback description.",
        ])

    lines.extend(["", "## Expected Results", ""])
    if behaviors:
        for case in behaviors:
            expected = case.get("expected_properties", [])
            if isinstance(expected, str):
                expected = [expected]
            if not expected:
                expected = [case.get("expected_output") or case.get("expected_result")]
            expected = [str(item) for item in expected if item]
            lines.append(f"### {case.get('id', 'scenario')}")
            lines.append("")
            request = case_request(case)
            if request:
                lines.append(f"For request “{request}”, the result must:")
                lines.append("")
            lines.extend(f"- {item};" for item in expected)
            if expected:
                lines[-1] = lines[-1].rstrip(";") + "."
            lines.append("")
    else:
        lines.extend([
            "- the result matches the stated contract and clearly separates facts from assumptions;",
            "- modified artifacts are listed, and completed checks are named without invented PASS results;",
            "- constraints, residual risks, rollback status, and the next step are stated explicitly.",
        ])

    lines.extend(["", "## Execution Flow", ""])
    if workflow:
        for index, title in enumerate(workflow, 1):
            lines.append(f"{index}. **{title}.** Execute the corresponding contract step from `SKILL.md`.")
    else:
        lines.extend([
            "1. Check that the skill applies and that the inputs are complete.",
            "2. Choose the narrowest safe route.",
            "3. Create or verify the required artifacts.",
            "4. Compare the result against the contract and deliver it with risks and the next step.",
        ])

    lines.extend(["", "## Boundaries And Unsuitable Requests", ""])
    if avoid:
        lines.append(avoid)
        lines.append("")
    if negatives:
        lines.append("The following examples should route to another skill or should not trigger this skill:")
        lines.append("")
        for case in negatives:
            destination = case.get("expected_specialist") or route_label(case)
            lines.append(f"- “{case_request(case)}” → `{destination}`.")
    else:
        lines.append("The skill must not expand the authority it received, hide skipped checks, perform irreversible or external actions without explicit permission, or claim host state solely from the presence of files.")

    forbidden = []
    for case in behavior.get("cases", []):
        forbidden.extend(case.get("forbidden_properties", []))
    if forbidden:
        lines.extend(["", "Critical anti-results:", ""])
        for item in list(dict.fromkeys(map(str, forbidden)))[:10]:
            lines.append(f"- {item};")
        lines[-1] = lines[-1].rstrip(";") + "."

    lines.extend(["", "## Dependencies", ""])
    if deps:
        lines.extend(deps)
        lines.append("")
        lines.append("A missing required dependency blocks only the route that depends on it. Recommended dependencies improve evidence quality but must not be imitated by the skill itself.")
    elif owner:
        lines.append(f"There are no external catalog dependencies. Parent `{owner}` passes only a bounded dispatch envelope to this private skill and verifies its result.")
    else:
        lines.append("No required companion skills are declared in the canonical dependency graph. Check the availability of host tools and resources referenced by `SKILL.md`.")

    lines.extend(["", "## Package Resources", ""])
    lines.append("- [`SKILL.md`](SKILL.md) — executable contract, routing, and safety rules.")
    for folder, meaning in resources:
        lines.append(f"- [`{folder}/`]({folder}/) — {meaning}.")

    lines.extend(["", "## Result Verification", ""])
    if (skill_dir / "evals" / "routing.json").is_file():
        lines.append("- Compare routing against [`evals/routing.json`](evals/routing.json).")
    if (skill_dir / "evals" / "behavior.json").is_file():
        lines.append("- Compare result properties against [`evals/behavior.json`](evals/behavior.json).")
    scripts = sorted((skill_dir / "scripts").glob("*.py")) if (skill_dir / "scripts").is_dir() else []
    for script in scripts[:5]:
        lines.append(f"- For deterministic verification, use [`scripts/{script.name}`](scripts/{script.name}) according to its `--help` output and the skill contract.")
    lines.append("- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.")

    lines.extend(["", "## Completion Format", ""])
    lines.append("The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.")
    lines.extend(["", END, ""])
    return "\n".join(lines)


def render(root: Path, check: bool) -> int:
    entries_data = load_json(root / "catalog" / "entries.json", {"entries": []})
    entries = {item["name"]: item for item in entries_data.get("entries", [])}
    dependencies = load_json(root / "catalog" / "dependencies.json", {"skills": {}}).get("skills", {})
    changed = []

    for skill_file in sorted((root / "skills").rglob("SKILL.md")):
        skill_dir = skill_file.parent
        name, description, version, body = metadata(skill_file)
        entry = entries.get(name, {})
        block = generated_block(root, skill_dir, name, description, version, body, entry.get("tags", []), dependencies)
        readme = skill_dir / "README.md"
        current = readme.read_text(encoding="utf-8") if readme.is_file() else ""
        if readme.is_file():
            if START in current and END in current:
                prefix = current.split(START, 1)[0].rstrip()
                suffix = current.split(END, 1)[1].strip()
                target = prefix + "\n\n" + block
                if suffix:
                    target += "\n" + suffix + "\n"
            else:
                target = current.rstrip() + "\n\n" + block
        else:
            target = f"# {name}\n\n" + block
        if current != target:
            changed.append(readme)
            if not check:
                readme.write_text(target, encoding="utf-8")

    if changed:
        verb = "Would update" if check else "Updated"
        print(f"{verb} {len(changed)} skill README files")
        for path in changed:
            print(path.relative_to(root))
        return 1 if check else 0
    print("All skill README files are up to date")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return render(args.root.resolve(), args.check)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        sys.exit(1)
