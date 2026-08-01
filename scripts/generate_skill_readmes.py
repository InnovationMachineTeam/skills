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
    return "Сценарий описан идентификатором и ожидаемым маршрутом в eval-корпусе."


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
    return "основной маршрут навыка"


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
        "agents": "UI-метаданные и host-конфигурация",
        "assets": "шаблоны и переиспользуемые артефакты",
        "evals": "routing- и behavior-сценарии",
        "prompts": "маршрутные и специализированные промпты",
        "references": "справочники, схемы и контракты",
        "scripts": "детерминированные проверки и автоматизация",
        "private-skills": "внутренние навыки, доступные только владельцу",
        "vendor": "зафиксированный снимок зависимых компонентов",
    }
    result = []
    for child in sorted(skill_dir.iterdir(), key=lambda path: path.name):
        if child.is_dir() and child.name in descriptions:
            result.append((child.name, descriptions[child.name]))
    return result


def dependency_lines(name: str, graph: dict[str, Any]) -> list[str]:
    declaration = graph.get(name, {})
    lines = []
    for kind, label in (("required", "Обязательный"), ("recommended", "Рекомендуемый")):
        for item in declaration.get(kind, []):
            reason = item.get("reason", "")
            lines.append(
                f"- **{label}: `{item['name']}` >= `{item['minimum_version']}`.** {reason}"
            )
    return lines


def visibility(skill_dir: Path, root: Path) -> str:
    if "private-skills" in skill_dir.relative_to(root).parts:
        return "package-private: вызывается только родительским `agent-master` и не публикуется отдельно"
    return "public: канонический навык каталога; фактическая активация зависит от целевого host"


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
        "## Паспорт навыка",
        "",
        f"- **Назначение:** {short_purpose(description)}",
        f"- **Версия:** `{version}`.",
        f"- **Видимость:** {visibility(skill_dir, root)}.",
    ]
    if tags:
        lines.append(f"- **Теги каталога:** {', '.join(f'`{tag}`' for tag in tags)}.")

    lines.extend(["", "## Когда использовать", ""])
    if use:
        lines.append(use)
    else:
        lines.append("Используйте навык, когда запрос соответствует его назначению и границам ответственности из `SKILL.md`.")
    lines.append("")
    lines.append("Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.")

    lines.extend(["", "## Варианты использования", ""])
    if routes:
        for case in routes:
            lines.append(f"### {case.get('id', route_label(case))}")
            lines.append("")
            lines.append(f"- **Пример запроса:** “{case_request(case)}”")
            lines.append(f"- **Ожидаемый маршрут:** `{route_label(case)}`.")
            action = case.get("expected_action")
            if action and action != route_label(case):
                lines.append(f"- **Ожидаемое действие:** `{action}`.")
            lines.append("")
    else:
        lines.extend([
            "- Явный вызов навыка для выполнения основного контракта из `SKILL.md`.",
            "- Аудит или планирование без изменения файлов, если полномочия на запись не заданы.",
            "- Применение разрешённых изменений с последующей проверкой результата и описанием отката.",
        ])

    lines.extend(["", "## Ожидаемые результаты", ""])
    if behaviors:
        for case in behaviors:
            expected = case.get("expected_properties", [])
            if isinstance(expected, str):
                expected = [expected]
            if not expected:
                expected = [case.get("expected_output") or case.get("expected_result")]
            expected = [str(item) for item in expected if item]
            lines.append(f"### {case.get('id', 'сценарий')}")
            lines.append("")
            request = case_request(case)
            if request:
                lines.append(f"Для запроса “{request}” результат должен:")
                lines.append("")
            lines.extend(f"- {item};" for item in expected)
            if expected:
                lines[-1] = lines[-1].rstrip(";") + "."
            lines.append("")
    else:
        lines.extend([
            "- результат соответствует заявленному контракту и явно отделяет факты от предположений;",
            "- изменённые артефакты перечислены, а выполненные проверки названы без выдуманных PASS-результатов;",
            "- ограничения, остаточные риски, состояние отката и следующий шаг указаны явно.",
        ])

    lines.extend(["", "## Как проходит выполнение", ""])
    if workflow:
        for index, title in enumerate(workflow, 1):
            lines.append(f"{index}. **{title}.** Выполняется соответствующий этап контракта из `SKILL.md`.")
    else:
        lines.extend([
            "1. Проверяется применимость навыка и полнота входных данных.",
            "2. Выбирается самый узкий безопасный маршрут.",
            "3. Создаются или проверяются требуемые артефакты.",
            "4. Результат сверяется с контрактом и передаётся вместе с рисками и следующим шагом.",
        ])

    lines.extend(["", "## Границы и неподходящие запросы", ""])
    if avoid:
        lines.append(avoid)
        lines.append("")
    if negatives:
        lines.append("Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:")
        lines.append("")
        for case in negatives:
            destination = case.get("expected_specialist") or route_label(case)
            lines.append(f"- “{case_request(case)}” → `{destination}`.")
    else:
        lines.append("Навык не должен расширять полученные полномочия, скрывать пропущенные проверки, выполнять необратимые или внешние действия без явного разрешения либо заявлять состояние host только по наличию файлов.")

    forbidden = []
    for case in behavior.get("cases", []):
        forbidden.extend(case.get("forbidden_properties", []))
    if forbidden:
        lines.extend(["", "Критические анти-результаты:", ""])
        for item in list(dict.fromkeys(map(str, forbidden)))[:10]:
            lines.append(f"- {item};")
        lines[-1] = lines[-1].rstrip(";") + "."

    lines.extend(["", "## Зависимости", ""])
    if deps:
        lines.extend(deps)
        lines.append("")
        lines.append("Отсутствующая обязательная зависимость блокирует только принадлежащий ей маршрут. Рекомендуемые зависимости повышают качество доказательств, но не должны имитироваться самим навыком.")
    elif "private-skills" in skill_dir.relative_to(root).parts:
        lines.append("Внешних зависимостей каталога нет. Родительский `agent-master` передаёт этому private-навыку только ограниченный dispatch-конверт и проверяет его результат.")
    else:
        lines.append("Обязательные companion-навыки в каноническом dependency-графе не объявлены. Проверяйте доступность host-инструментов и ресурсов, на которые ссылается `SKILL.md`.")

    lines.extend(["", "## Ресурсы пакета", ""])
    lines.append("- [`SKILL.md`](SKILL.md) — исполняемый контракт, маршрутизация и правила безопасности.")
    for folder, meaning in resources:
        lines.append(f"- [`{folder}/`]({folder}/) — {meaning}.")

    lines.extend(["", "## Проверка результата", ""])
    if (skill_dir / "evals" / "routing.json").is_file():
        lines.append("- Сверьте маршрутизацию с [`evals/routing.json`](evals/routing.json).")
    if (skill_dir / "evals" / "behavior.json").is_file():
        lines.append("- Сверьте свойства результата с [`evals/behavior.json`](evals/behavior.json).")
    scripts = sorted((skill_dir / "scripts").glob("*.py")) if (skill_dir / "scripts").is_dir() else []
    for script in scripts[:5]:
        lines.append(f"- Для детерминированной проверки используйте [`scripts/{script.name}`](scripts/{script.name}) согласно его `--help` и контракту навыка.")
    lines.append("- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.")

    lines.extend(["", "## Формат завершения", ""])
    lines.append("Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.")
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
