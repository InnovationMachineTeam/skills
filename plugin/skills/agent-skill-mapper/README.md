# agent-skill-mapper

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Maps governed public and owner-private skills or commands to existing agents using mission fit, permissions, trust, context cost, evidence and capability budgets.
- **Версия:** `1.0.1`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `skills`, `mapping`.

## Когда использовать

Auditing agent capabilities, reconciling agent definitions with registries or skills-lock files, recommending versioned bindings, detecting gaps or excessive tool access, or preparing a controlled mapping update. Read only by default. Do not create agents or skills, promote private capabilities, silently edit agent definitions, or operate the team; route missing capability creation to the relevant architect and team design changes to agent-team-architect.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Варианты использования

### inventory

- **Пример запроса:** “Inventory all skills available to these registered agents.”
- **Ожидаемый маршрут:** `inventory`.

### recommend

- **Пример запроса:** “Which versioned skills should each agent receive?”
- **Ожидаемый маршрут:** `recommend`.

### audit

- **Пример запроса:** “Audit the current agent-to-skill map for excess permissions.”
- **Ожидаемый маршрут:** `audit`.

### apply

- **Пример запроса:** “Apply this approved mapping transaction and bump agent versions.”
- **Ожидаемый маршрут:** `apply`.

### promote

- **Пример запроса:** “Can this private agent skill be promoted for team use?”
- **Ожидаемый маршрут:** `private-promotion`.


## Ожидаемые результаты

### private-boundary

Для запроса “Map agent-a's private command to agent-b.” результат должен:

- rejects cross-owner mapping;
- offers explicit promotion workflow.

### read-only

Для запроса “Recommend capabilities for the team.” результат должен:

- does not mutate files;
- uses exact versions and evidence;
- enforces capability budgets.

### authorized-apply

Для запроса “Apply approved map revision 7.” результат должен:

- checks expected revisions;
- bumps changed agent versions;
- supports rollback.


## Как проходит выполнение

1. **Establish inventory and authority.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Score candidates through hard gates.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Decide and explain.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Apply only an authorized transaction.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Create a new PDF extraction skill.” → `skill-architect`.
- “Design the roles for a research agent team.” → `agent-team-architect`.

Критические анти-результаты:

- silently copies private content;
- activates mappings;
- overwrites concurrent changes.

## Зависимости

Обязательные companion-навыки в каноническом dependency-графе не объявлены. Проверяйте доступность host-инструментов и ресурсов, на которые ссылается `SKILL.md`.

## Ресурсы пакета

- [`SKILL.md`](SKILL.md) — исполняемый контракт, маршрутизация и правила безопасности.
- [`agents/`](agents/) — UI-метаданные и host-конфигурация.
- [`evals/`](evals/) — routing- и behavior-сценарии.
- [`references/`](references/) — справочники, схемы и контракты.
- [`scripts/`](scripts/) — детерминированные проверки и автоматизация.

## Проверка результата

- Сверьте маршрутизацию с [`evals/routing.json`](evals/routing.json).
- Сверьте свойства результата с [`evals/behavior.json`](evals/behavior.json).
- Для детерминированной проверки используйте [`scripts/check_evals.py`](scripts/check_evals.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/validate_mapping.py`](scripts/validate_mapping.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
