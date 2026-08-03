# agent-team-architect

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Designs the smallest justified greenfield team of agents, subagents, specialists, an orchestrator, and human responsibilities from a task and capability graph, or redesigns an asset already defined as a team.
- **Версия:** `1.1.2`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `architecture`, `teams`.

## Когда использовать

A new problem may need multiple agents, a confirmed PROMOTE_TO_TEAM decision needs roles and topology, or an existing team needs handoff, worktree, model or skill boundaries and a versioned specification. Produce design artifacts only.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Полный пример команды

Иллюстративный полный вызов; адаптируйте пути, ограничения и критерии приёмки к своей задаче:

```text
/agent-team-architect Assess whether this delivery workflow actually needs multiple agents or should stay a single agent.
```

**Ожидаемый результат:** выбирается маршрут `worth-assessment`; итог перечисляет созданные или изменённые артефакты, фактически выполненные проверки, ограничения, остаточные риски и следующий шаг. Наличие файлов само по себе не считается доказательством установки, активации или публикации.

## Варианты использования

### worth

- **Пример запроса:** “Assess whether this delivery workflow actually needs multiple agents or should stay a single agent.”
- **Ожидаемый маршрут:** `worth-assessment`.

### design

- **Пример запроса:** “Design the minimal roles, handoffs, skills, models, and failure policy for an agent team.”
- **Ожидаемый маршрут:** `design-team`.

### redesign

- **Пример запроса:** “Our current agent team has duplicate planner roles and no integration owner. Redesign the specification only.”
- **Ожидаемый маршрут:** `redesign-team`.

### topology

- **Пример запроса:** “Choose between manager-as-tools, handoffs, and a fork-join topology for these independent tasks.”
- **Ожидаемый маршрут:** `topology`.

### worktrees

- **Пример запроса:** “Decide whether these coding agents need separate worktrees and define merge ownership.”
- **Ожидаемый маршрут:** `worktree-policy`.


## Ожидаемые результаты

### reject-role-inflation

Для запроса “Create separate planner, coordinator, orchestrator, lead, and manager roles even though they share tools, state, and outputs.” результат должен:

- requires boundary evidence;
- combines redundant roles;
- allows NO_TEAM or fewer roles.

### private-placement

Для запроса “Two agents should directly share one private skill inside the first agent folder.” результат должен:

- rejects multi-owner private binding;
- routes to public promotion assessment or separate capability.

### unsafe-parallel

Для запроса “Put three agents in the same files in parallel and let them resolve conflicts later.” результат должен:

- detects overlapping write-sets;
- requires sequential work, separation, or merge protocol.

### design-not-activation

Для запроса “The specification looks valid, so activate the team now.” результат должен:

- returns design candidate only;
- requires builder, evaluator, and lifecycle authority.


## Как проходит выполнение

1. **Establish the outcome.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Build evidence graphs.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Specify every role and interaction.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Decide workspaces and lifecycle.** Выполняется соответствующий этап контракта из `SKILL.md`.
5. **Produce and validate the specification.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Assess migration of this registered overloaded single agent into a team without designing the team yet.” → `agent-refactor`.
- “Materialize this approved team spec under .agents and generate host adapters.” → `agent-team-builder`.
- “Create a new PDF editing skill.” → `skill-architect`.

Критические анти-результаты:

- creates roles from titles alone;
- expands private allow-list;
- approves uncontrolled concurrent writes;
- activates runtime.

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
- Для детерминированной проверки используйте [`scripts/validate_team_spec.py`](scripts/validate_team_spec.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
