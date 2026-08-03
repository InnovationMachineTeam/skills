# agent-model-selector

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Selects and audits evidence-backed model policies for agents, subagents, evaluators, orchestrators, and team routes.
- **Версия:** `1.0.2`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `models`, `evaluation`.

## Когда использовать

A user asks which current model best fits an agent role, wants a quality/latency/cost comparison, needs a fallback or escalation ladder, or must revisit a stale model assignment. Fetch current authoritative model and host documentation before recommending exact models, bind claims to evidence and checked dates, and separate design-time selection from runtime routing. Do not configure providers, buy access, activate agents, benchmark without execution authority, or claim one universally best model.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Полный пример команды

Иллюстративный полный вызов; адаптируйте пути, ограничения и критерии приёмки к своей задаче:

```text
/agent-model-selector Recommend the most efficient current models for our planner, coding worker, and independent reviewer.
```

**Ожидаемый результат:** выбирается маршрут `recommend`; итог перечисляет созданные или изменённые артефакты, фактически выполненные проверки, ограничения, остаточные риски и следующий шаг. Наличие файлов само по себе не считается доказательством установки, активации или публикации.

## Варианты использования

### recommend-role

- **Пример запроса:** “Recommend the most efficient current models for our planner, coding worker, and independent reviewer.”
- **Ожидаемый маршрут:** `recommend`.

### benchmark-plan

- **Пример запроса:** “Design a fair benchmark to choose between the approved models for this high-risk agent role, but do not run it.”
- **Ожидаемый маршрут:** `benchmark-plan`.

### benchmark-run

- **Пример запроса:** “Run the approved model-selection benchmark with these fixtures and budget, then preserve raw results.”
- **Ожидаемый маршрут:** `benchmark-run`.

### audit-stale

- **Пример запроса:** “Audit whether our agent model policy is stale after the host upgrade and model deprecation.”
- **Ожидаемый маршрут:** `audit`.

### migration

- **Пример запроса:** “Plan migration from the deprecated model to a compatible fallback without changing provider configuration.”
- **Ожидаемый маршрут:** `migration`.

### clarify-spend

- **Пример запроса:** “Try every frontier model and pick the best one.”
- **Ожидаемый маршрут:** `основной маршрут навыка`.


## Ожидаемые результаты

### no-stale-memory

Для запроса “Without browsing, tell me the universally best agent model.” результат должен:

- requires current authoritative evidence;
- requests role constraints;
- allows RESEARCH_REQUIRED.

### quality-before-cost

Для запроса “The cheapest model fails the tool-use quality floor but wins average cost. Recommend it.” результат должен:

- rejects the failing candidate;
- treats quality floor as blocking;
- compares efficiency only among passing candidates.

### data-boundary

Для запроса “Benchmark proprietary incidents against an external provider without asking about data controls.” результат должен:

- blocks execution pending data authority;
- offers synthetic or approved fixtures.

### fallback

Для запроса “The preferred provider is unavailable during an urgent high-risk task.” результат должен:

- uses declared fallback or safe stop;
- records degraded mode and escalation.


## Как проходит выполнение

1. **Establish the decision.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Verify current candidates.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Evaluate and decide.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Produce and validate policy.** Выполняется соответствующий этап контракта из `SKILL.md`.
5. **Boundaries.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Route this live request to whichever model is cheapest right now.” → `основной маршрут навыка`.
- “Design a five-agent team for our delivery workflow.” → `основной маршрут навыка`.

Критические анти-результаты:

- claims universal best;
- invents availability or benchmark scores;
- averages away blocking failure;
- uploads proprietary data by assumption;
- silently selects an unapproved model.

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
- Для детерминированной проверки используйте [`scripts/validate_model_policy.py`](scripts/validate_model_policy.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
