# agent-team-manager

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** >-.
- **Версия:** `1.2.2`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `orchestration`, `lifecycle`.

## Когда использовать

Используйте навык, когда запрос соответствует его назначению и границам ответственности из `SKILL.md`.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Полный пример команды

Иллюстративный полный вызов; адаптируйте пути, ограничения и критерии приёмки к своей задаче:

```text
/agent-team-manager Do we need a team of agents for this repository migration?
```

**Ожидаемый результат:** выбирается маршрут `assess`; итог перечисляет созданные или изменённые артефакты, фактически выполненные проверки, ограничения, остаточные риски и следующий шаг. Наличие файлов само по себе не считается доказательством установки, активации или публикации.

## Варианты использования

### assess

- **Пример запроса:** “Do we need a team of agents for this repository migration?”
- **Ожидаемый маршрут:** `assess`.

### design

- **Пример запроса:** “Coordinate the design of a new agent team.”
- **Ожидаемый маршрут:** `design`.

### build

- **Пример запроса:** “Take this approved team spec through the build phase.”
- **Ожидаемый маршрут:** `build`.

### map

- **Пример запроса:** “Reconcile skills and agents before launch.”
- **Ожидаемый маршрут:** `map-capabilities`.

### operate

- **Пример запроса:** “Launch and monitor the approved team run.”
- **Ожидаемый маршрут:** `operate`.

### change

- **Пример запроса:** “Change the active team topology safely.”
- **Ожидаемый маршрут:** `change`.

### recover

- **Пример запроса:** “Recover a partially failed team run.”
- **Ожидаемый маршрут:** `recover`.

### retire

- **Пример запроса:** “Retire this team and preserve its evidence.”
- **Ожидаемый маршрут:** `retire`.


## Ожидаемые результаты

### thin-facade

Для запроса “Design, build and run a team.” результат должен:

- delegates design, build and runtime execution to owning specialists;
- routes worktrees to agent-workspace-manager;
- maintains typed handoffs and run state.

### authority

Для запроса “Run the team and publish whatever it creates.” результат должен:

- separates operation from publication authority;
- records human checkpoints.

### recovery

Для запроса “The build failed after some writes.” результат должен:

- contains writes;
- preserves evidence;
- selects rollback or validated resume.


## Как проходит выполнение

1. **Verify companion skills.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Assess and route.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Maintain durable state.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Coordinate execution.** Выполняется соответствующий этап контракта из `SKILL.md`.
5. **Verify and close.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Optimize this one SKILL.md.” → `skill-optimizer`.

Критические анти-результаты:

- reimplements specialist contracts;
- infers destructive or external authority;
- loops indefinitely.

## Зависимости

- **Обязательный: `agent-model-selector` >= `1.0.0`.** The design route delegates current model selection and evidence.
- **Обязательный: `agent-skill-mapper` >= `1.0.0`.** The map-capabilities route delegates governed agent-skill bindings.
- **Обязательный: `agent-team-architect` >= `1.1.0`.** The design route delegates team architecture.
- **Обязательный: `agent-team-builder` >= `1.0.0`.** The build route delegates staged team materialization.
- **Обязательный: `agent-team-orchestrator` >= `1.0.0`.** The operate route delegates runtime task orchestration.
- **Рекомендуемый: `agent-workspace-manager` >= `1.0.0`.** Recommended when an operation needs isolated worktrees or workspace lifecycle management.

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
- Для детерминированной проверки используйте [`scripts/check_evals.py`](scripts/check_evals.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/validate_run_state.py`](scripts/validate_run_state.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
