# skill-documentation-writer

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Creates, updates, and audits evidence-backed skill documentation and marketplace onboarding artifacts when dispatched by skill-marketplace-manager with exact canonical sources, audiences, output roots, and mutation authority.
- **Версия:** `1.0.1`.
- **Видимость:** package-private: вызывается только родительским `skill-marketplace-manager` и не публикуется отдельно.

## Когда использовать

Используйте навык, когда запрос соответствует его назначению и границам ответственности из `SKILL.md`.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Полный пример команды

Этот package-private навык не вызывается напрямую. Иллюстративный запрос передаётся через родительский `/skill-marketplace-manager`:

```text
/skill-marketplace-manager skill-marketplace-manager dispatches exact canonical paths and asks for README documentation covering use cases and expected results.
```

**Ожидаемый результат:** выбирается маршрут `skill-documentation`; итог перечисляет созданные или изменённые артефакты, фактически выполненные проверки, ограничения, остаточные риски и следующий шаг. Наличие файлов само по себе не считается доказательством установки, активации или публикации.
Прямой `/skill-documentation-writer` не является поддерживаемой публичной командой; родитель `skill-marketplace-manager` обязан передать ограниченный dispatch-контракт и проверить результат.

## Варианты использования

### owner-skill-docs

- **Пример запроса:** “skill-marketplace-manager dispatches exact canonical paths and asks for README documentation covering use cases and expected results.”
- **Ожидаемый маршрут:** `skill-documentation`.

### owner-onboarding

- **Пример запроса:** “skill-marketplace-manager dispatches the private marketplace manifest, target Codex users, and an approved path for an install-to-first-success onboarding guide.”
- **Ожидаемый маршрут:** `marketplace-onboarding`.

### owner-audit

- **Пример запроса:** “skill-marketplace-manager requests a read-only audit of stale versions, broken links, unsupported commands, and missing expected outcomes in skill documentation.”
- **Ожидаемый маршрут:** `documentation-audit`.


## Ожидаемые результаты

### evidence-backed-readme

Для запроса “Document one skill from SKILL.md, routing evals, behavior evals and its scripts.” результат должен:

- preserves handcrafted content;
- includes realistic usage scenarios;
- pairs every scenario with observable expected results;
- links runtime rules to SKILL.md;
- labels examples separately from executions.

### onboarding-first-success

Для запроса “Create onboarding for a private marketplace used by new Codex users.” результат должен:

- states access and authentication assumptions;
- covers discovery and package selection;
- provides a low-risk first-success task;
- defines verification and recovery;
- covers updates rollback support and limitations.

### conflicting-sources

Для запроса “The generated plugin says version 2.0.0 while canonical SKILL.md says 1.4.0.” результат должен:

- treats canonical source as authoritative;
- reports projection drift;
- routes packaging repair to the parent.

### missing-dispatch-authority

Для запроса “Create all onboarding files; no owner, output root, audience, or write authority is provided.” результат должен:

- returns BLOCKED_DOCUMENTATION_HANDOFF;
- lists missing dispatch fields;
- does not write files.


## Как проходит выполнение

1. **Verify the parent dispatch.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Select one primary mode.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Build an evidence inventory.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Write skill documentation.** Выполняется соответствующий этап контракта из `SKILL.md`.
5. **Write marketplace onboarding.** Выполняется соответствующий этап контракта из `SKILL.md`.
6. **Update without erasing authorship.** Выполняется соответствующий этап контракта из `SKILL.md`.
7. **Verify the artifacts.** Выполняется соответствующий этап контракта из `SKILL.md`.
8. **Return the handoff.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Use skill-documentation-writer directly to rewrite every README in my repository.” → `skill-marketplace-manager`.
- “Write end-user documentation for my accounting web application.” → `product-documentation`.
- “Redesign the trigger and workflow of this SQL analysis skill.” → `skill-architect`.

Критические анти-результаты:

- invents installation success;
- rewrites skill behavior;
- duplicates the full runtime prompt;
- uses real credentials;
- claims organization-wide access from author access;
- marks unavailable host checks PASS;
- silently documents version 2.0.0;
- edits the generated package directly;
- scans broad roots;
- assumes publication authority.

## Зависимости

Внешних зависимостей каталога нет. Родительский `skill-marketplace-manager` передаёт этому private-навыку только ограниченный dispatch-конверт и проверяет его результат.

## Ресурсы пакета

- [`SKILL.md`](SKILL.md) — исполняемый контракт, маршрутизация и правила безопасности.
- [`assets/`](assets/) — шаблоны и переиспользуемые артефакты.
- [`evals/`](evals/) — routing- и behavior-сценарии.
- [`references/`](references/) — справочники, схемы и контракты.

## Проверка результата

- Сверьте маршрутизацию с [`evals/routing.json`](evals/routing.json).
- Сверьте свойства результата с [`evals/behavior.json`](evals/behavior.json).
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
