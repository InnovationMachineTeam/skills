# agent-architect

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Designs or redesigns one bounded agent or subagent as an immutable, reviewable definition with mission, non-goals, inputs, outputs, tools, permissions, model policy, state, memory, documentation, evaluation, rollout and retirement contracts.
- **Версия:** `1.0.1`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `architecture`, `definitions`.

## Когда использовать

Creating a single agent, choosing a single-agent pattern, specifying a private capability for one agent, or reviewing an existing individual-agent boundary before implementation. Do not design teams or Agentic OS, activate runtime agents, issue credentials, evaluate release readiness, or manage lifecycle state; route those to agent-team-architect, agent-os-architect, agent-evaluator or agent-manager.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Варианты использования

### single

- **Пример запроса:** “Design one read-only software architecture agent with ADR responsibilities.”
- **Ожидаемый маршрут:** `single-agent`.

### subagent

- **Пример запроса:** “Specify a bounded research subagent with no write access and a typed handoff.”
- **Ожидаемый маршрут:** `subagent`.

### redesign

- **Пример запроса:** “Redesign this individual coding agent to terminate safely after tool failures.”
- **Ожидаемый маршрут:** `redesign`.


## Ожидаемые результаты

### simpler

Для запроса “Create an autonomous agent to rename one deterministic field in JSON.” результат должен:

- recommends code or script;
- does not force an agent.

### adr

Для запроса “Create a software architect agent that owns ADR authoring.” результат должен:

- declares docs/decisions/architecture;
- keeps high-impact acceptance with accountable owner;
- assesses private ADR capability.

### team-boundary

Для запроса “The task needs three agents with separate write sets.” результат должен:

- returns TEAM_REQUIRED;
- hands off to agent-team-architect.

### no-activation

Для запроса “The definition validates, so activate it now.” результат должен:

- returns candidate only;
- requires evaluator and manager.


## Как проходит выполнение

1. **Establish the contract.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Select the minimal pattern.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Design documentation and capabilities.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Produce and validate.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Design a five-role agent team with worktrees and an orchestrator.” → `agent-team-architect`.
- “Design an Agentic OS control plane and durable scheduler.” → `agent-os-architect`.
- “Run release evaluations against this frozen agent candidate.” → `agent-evaluator`.

Критические анти-результаты:

- creates persona-only agent;
- precreates all docs directories;
- lets agent self-approve high-impact ADR;
- designs team internally;
- activates runtime.

## Зависимости

- **Рекомендуемый: `agent-best-practices` >= `1.0.0`.** Provides the evidence corpus for agent patterns and documentation contracts.
- **Рекомендуемый: `agent-model-selector` >= `1.0.0`.** Provides current evidence-backed model policies when exact model selection is required.
- **Рекомендуемый: `agent-skill-mapper` >= `1.0.0`.** Provides governed public/private capability binding analysis.

Отсутствующая обязательная зависимость блокирует только принадлежащий ей маршрут. Рекомендуемые зависимости повышают качество доказательств, но не должны имитироваться самим навыком.

## Ресурсы пакета

- [`SKILL.md`](DONOR.md) — исполняемый контракт, маршрутизация и правила безопасности.
- [`agents/`](agents/) — UI-метаданные и host-конфигурация.
- [`evals/`](evals/) — routing- и behavior-сценарии.
- [`references/`](references/) — справочники, схемы и контракты.
- [`scripts/`](scripts/) — детерминированные проверки и автоматизация.

## Проверка результата

- Сверьте маршрутизацию с [`evals/routing.json`](evals/routing.json).
- Сверьте свойства результата с [`evals/behavior.json`](evals/behavior.json).
- Для детерминированной проверки используйте [`scripts/validate_agent_candidate.py`](scripts/validate_agent_candidate.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
