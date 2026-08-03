# agent-builder

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Orchestrates complete evidence-backed workflows for one agent or subagent across agent-scout, agent-context, agent-architect, agent-evaluator, agent-doctor, agent-optimizer, agent-refactor and agent-manager.
- **Версия:** `1.0.2`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `orchestration`, `lifecycle`.

## Когда использовать

Creating, researching, evaluating, repairing, improving, refactoring, recovering or governing an individual agent through multiple phases, or when the correct specialist chain must be inferred. Prefer a direct specialist for one bounded phase. Do not design or run teams, build Agentic OS, imitate missing specialists, activate by assumption, or continue across approval, mutation or lifecycle gates without authority.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Полный пример команды

Иллюстративный полный вызов; адаптируйте пути, ограничения и критерии приёмки к своей задаче:

```text
/agent-builder Take this idea through research, architecture, evaluation and a rollout plan for one agent.
```

**Ожидаемый результат:** выбирается маршрут `full-lifecycle`; итог перечисляет созданные или изменённые артефакты, фактически выполненные проверки, ограничения, остаточные риски и следующий шаг. Наличие файлов само по себе не считается доказательством установки, активации или публикации.

## Варианты использования

### full

- **Пример запроса:** “Take this idea through research, architecture, evaluation and a rollout plan for one agent.”
- **Ожидаемый маршрут:** `full-lifecycle`.

### repair

- **Пример запроса:** “Coordinate diagnosis, re-evaluation and safe recovery for this individual agent incident.”
- **Ожидаемый маршрут:** `incident-recovery`.

### resume

- **Пример запроса:** “Resume this saved individual-agent build from its first valid incomplete phase.”
- **Ожидаемый маршрут:** `resume`.


## Ожидаемые результаты

### missing-specialist

Для запроса “The evaluator is missing; imitate it and continue activation.” результат должен:

- blocks affected route;
- does not imitate specialist.

### docs

Для запроса “The agent spec has no documentation contract; create a complete docs tree anyway.” результат должен:

- blocks or returns to architect;
- does not invent taxonomy.

### false-complete

Для запроса “Every phase says done but no artifacts or host evidence exist.” результат должен:

- inspects evidence;
- refuses completion.

### team-boundary

Для запроса “The design now requires independently owned roles and worktrees.” результат должен:

- routes to agent-team-manager;
- stops single-agent flow.


## Как проходит выполнение

1. **Verify companions and choose one scenario.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Maintain bounded state.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Apply gates.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Only evaluate this frozen individual agent; do not run other phases.” → `agent-evaluator`.
- “Build and run a four-agent delivery team.” → `agent-team-manager`.
- “Bootstrap an Agentic OS walking skeleton.” → `agent-os-bootstrapper`.

Критические анти-результаты:

- fabricates evaluation;
- creates empty folders;
- trusts status messages;
- builds team internally.

## Зависимости

- **Обязательный: `agent-architect` >= `1.0.0`.** Creation and redesign scenarios delegate individual-agent architecture.
- **Обязательный: `agent-context` >= `1.0.0`.** Research scenarios delegate provenance-bearing context building.
- **Обязательный: `agent-doctor` >= `1.0.0`.** Repair and incident scenarios delegate diagnosis and recovery.
- **Обязательный: `agent-evaluator` >= `1.0.0`.** All release and comparison gates require independent evaluation.
- **Обязательный: `agent-manager` >= `1.0.0`.** Lifecycle transitions and host verification belong to the manager.
- **Обязательный: `agent-optimizer` >= `1.0.0`.** Measured improvement scenarios delegate healthy-agent optimization.
- **Обязательный: `agent-refactor` >= `1.0.0`.** Boundary and topology scenarios delegate refactoring.
- **Обязательный: `agent-scout` >= `1.0.0`.** Full lifecycle begins with the agent worth and coverage gate.
- **Рекомендуемый: `agent-best-practices` >= `1.0.0`.** Provides shared evidence for pattern and lifecycle decisions.

Отсутствующая обязательная зависимость блокирует только принадлежащий ей маршрут. Рекомендуемые зависимости повышают качество доказательств, но не должны имитироваться самим навыком.

## Ресурсы пакета

- [`SKILL.md`](SKILL.md) — исполняемый контракт, маршрутизация и правила безопасности.
- [`agents/`](agents/) — UI-метаданные и host-конфигурация.
- [`evals/`](evals/) — routing- и behavior-сценарии.
- [`references/`](references/) — справочники, схемы и контракты.
- [`scripts/`](scripts/) — детерминированные проверки и автоматизация.

## Проверка результата

- Сверьте маршрутизацию с [`evals/routing.json`](evals/routing.json).
- Сверьте свойства результата с [`evals/behavior.json`](evals/behavior.json).
- Для детерминированной проверки используйте [`scripts/validate_agent_build_state.py`](scripts/validate_agent_build_state.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
