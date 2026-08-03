# agent-team-orchestrator

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Executes an approved, active agent-team definition through a bounded task graph with typed envelopes, minimal context capsules, leases, budgets, checkpoints, cancellation, recovery and independent verification.
- **Версия:** `1.0.2`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `runtime`, `orchestration`.

## Когда использовать

Launching, resuming, monitoring, cancelling or recovering a concrete team run. It may choose only among declared workflows and cannot redesign teams, edit agents or skills, broaden authority, create worktrees directly, publish outputs by implication, or replace the lifecycle control plane owned by agent-team-manager.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Полный пример команды

Иллюстративный полный вызов; адаптируйте пути, ограничения и критерии приёмки к своей задаче:

```text
/agent-team-orchestrator Plan an approved team run for this task envelope.
```

**Ожидаемый результат:** выбирается маршрут `plan`; итог перечисляет созданные или изменённые артефакты, фактически выполненные проверки, ограничения, остаточные риски и следующий шаг. Наличие файлов само по себе не считается доказательством установки, активации или публикации.

## Варианты использования

### plan

- **Пример запроса:** “Plan an approved team run for this task envelope.”
- **Ожидаемый маршрут:** `plan`.

### run

- **Пример запроса:** “Execute this task with active team review@1.0.0.”
- **Ожидаемый маршрут:** `run`.

### monitor

- **Пример запроса:** “Show leases, budget and blockers for run 42.”
- **Ожидаемый маршрут:** `monitor`.

### resume

- **Пример запроса:** “Resume run 42 from its verified checkpoint.”
- **Ожидаемый маршрут:** `resume`.

### cancel

- **Пример запроса:** “Cancel run 42 and preserve partial evidence.”
- **Ожидаемый маршрут:** `cancel`.

### recover

- **Пример запроса:** “Recover the team run after one worker failed.”
- **Ожидаемый маршрут:** `recover`.


## Ожидаемые результаты

### sequential

Для запроса “Run two dependent stages.” результат должен:

- dispatches in dependency order;
- checks each exit gate.

### fork-join

Для запроса “Run two independent reviews then integrate.” результат должен:

- uses disjoint write-sets;
- names integration owner;
- independently verifies result.

### worker-failure

Для запроса “One fork fails deterministically.” результат должен:

- classifies failure;
- does not retry deterministic failure indefinitely;
- uses approved recovery.

### conflict

Для запроса “Two workers produce conflicting outputs.” результат должен:

- routes conflict to integration policy and verifier.

### budget

Для запроса “The run exhausts its step budget.” результат должен:

- stops new dispatch;
- returns resumable blocked evidence.

### cancel

Для запроса “Cancel then resume the run.” результат должен:

- makes cancellation durable and idempotent;
- revalidates checkpoint and external state.

### duplicate

Для запроса “The same task delivery arrives twice.” результат должен:

- uses idempotency key;
- avoids duplicate side effects.

### stale

Для запроса “The agent version changed after plan approval.” результат должен:

- blocks dispatch and returns to assessment.


## Как проходит выполнение

1. **Gate and plan the run.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Dispatch bounded context.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Observe, recover and cancel.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Integrate and verify.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Add a verifier role to this team.” → `agent-team-architect`.
- “Retire this entire agent team.” → `agent-team-manager`.

Критические анти-результаты:

- parallelizes shared writes;
- lets workers self-merge without protocol;
- claims full completion;
- chooses silently;
- raises budget itself;
- continues stale leases;
- creates a second independent run;
- runs stale definition.

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
- Для детерминированной проверки используйте [`scripts/validate_run_plan.py`](scripts/validate_run_plan.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
