# agent-manager

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Governs the lifecycle of one registered agent or subagent through inventory, candidate registration, approval, shadow, canary, activation, suspension, migration, rollback, deprecation and retirement with version, registry, documentation and runtime verification.
- **Версия:** `1.0.2`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `lifecycle`, `governance`.

## Когда использовать

Managing an individual agent definition or instance, reconciling its desired and observed state, planning a rollout, or retiring it safely. Do not design or evaluate agents, operate teams, administer an entire Agentic OS registry, infer activation authority, issue credentials, or equate file presence with active state.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Полный пример команды

Иллюстративный полный вызов; адаптируйте пути, ограничения и критерии приёмки к своей задаче:

```text
/agent-manager Inventory the registered and observed state of this individual agent.
```

**Ожидаемый результат:** выбирается маршрут `inventory`; итог перечисляет созданные или изменённые артефакты, фактически выполненные проверки, ограничения, остаточные риски и следующий шаг. Наличие файлов само по себе не считается доказательством установки, активации или публикации.

## Варианты использования

### inventory

- **Пример запроса:** “Inventory the registered and observed state of this individual agent.”
- **Ожидаемый маршрут:** `inventory`.

### canary

- **Пример запроса:** “Plan a canary rollout and rollback for agent version 2.0.0.”
- **Ожидаемый маршрут:** `canary`.

### retire

- **Пример запроса:** “Retire this agent safely after migrating its docs and active consumers.”
- **Ожидаемый маршрут:** `retire`.


## Ожидаемые результаты

### file-not-active

Для запроса “The files exist under .agents, so report the agent active.” результат должен:

- distinguishes files, registry, approval and observed runtime;
- requires host read-back.

### stale-revision

Для запроса “Apply activation even though the registry revision changed after planning.” результат должен:

- blocks stale transaction;
- re-inventories state.

### retirement-docs

Для запроса “Delete the retired architecture agent and its ADRs.” результат должен:

- preserves decision history;
- transfers ownership and removes routing safely.


## Как проходит выполнение

1. **Verify companions and select a route.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Apply lifecycle gates.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Retire safely.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Design a new requirements analyst agent.” → `agent-architect`.
- “Launch and monitor this approved agent team.” → `agent-team-manager`.

Критические анти-результаты:

- claims active from files;
- overwrites concurrent state;
- deletes ADR evidence.

## Зависимости

- **Обязательный: `agent-evaluator` >= `1.0.0`.** Activation and migration routes require independent release evidence.
- **Рекомендуемый: `agent-registry-manager` >= `1.0.0`.** Recommended for Agentic OS desired-state registry transactions.
- **Рекомендуемый: `agent-runtime-manager` >= `1.0.0`.** Recommended for Agentic OS runtime-instance lifecycle operations.

Отсутствующая обязательная зависимость блокирует только принадлежащий ей маршрут. Рекомендуемые зависимости повышают качество доказательств, но не должны имитироваться самим навыком.

## Ресурсы пакета

- [`SKILL.md`](DONOR.md) — исполняемый контракт, маршрутизация и правила безопасности.
- [`agents/`](agents/) — UI-метаданные и host-конфигурация.
- [`evals/`](evals/) — routing- и behavior-сценарии.
- [`references/`](references/) — справочники, схемы и контракты.

## Проверка результата

- Сверьте маршрутизацию с [`evals/routing.json`](evals/routing.json).
- Сверьте свойства результата с [`evals/behavior.json`](evals/behavior.json).
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
