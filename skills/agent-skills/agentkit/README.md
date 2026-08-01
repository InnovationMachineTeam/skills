# agentkit

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Explicit composite toolkit for the version-locked individual-agent lifecycle skills.
- **Версия:** `1.0.1`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `orchestration`, `composite`, `lifecycle`.

## Когда использовать

Используйте навык, когда запрос соответствует его назначению и границам ответственности из `SKILL.md`.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Варианты использования

### route-explicit-e2e

- **Пример запроса:** “agentkit e2e all для проверки всех команд”
- **Ожидаемый маршрут:** `e2e`.

### route-explicit-architect

- **Пример запроса:** “$agentkit architect создай контракт агента архитектора”
- **Ожидаемый маршрут:** `architect`.


## Ожидаемые результаты

### behavior-load-one-donor

Для запроса “agentkit evaluate ./agent.json” результат должен:

- Selects agent-evaluator only;
- Reports locked donor version and hash;
- Preserves the supplied authority.

### behavior-e2e-donor-approval

Для запроса “agentkit e2e all; один тест показал улучшение для agent-optimizer” результат должен:

- Classifies ownership from evidence;
- Shows exact donor and proposed staged process;
- Asks before creating the prompt or launching donor work.

### behavior-run-choice

Для запроса “agentkit run создать и проверить нового агента” результат должен:

- Presents two to four workflows;
- Names gates and mutations;
- Waits for workflow selection.

### behavior-drift-fails-closed

Для запроса “agentkit upgrade при отсутствующем agent-doctor” результат должен:

- Reports missing donor;
- Blocks automatic upgrade;
- Preserves the current stable pack.


## Как проходит выполнение

1. **Parse the command.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Dispatch a donor.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Run a workflow.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Execute E2E evaluation.** Выполняется соответствующий этап контракта из `SKILL.md`.
5. **Check status and upgrade.** Выполняется соответствующий этап контракта из `SKILL.md`.
6. **Complete safely.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Создай одного агента для ревью архитектуры” → `agent-architect`.
- “Спроектируй команду агентов и их взаимодействие” → `agent-team-architect`.
- “Запусти metaskillpack doctor для skill-optimizer” → `metaskillpack`.

Критические анти-результаты:

- Loads all donor bodies;
- Invokes agentkit recursively;
- Edits the donor;
- Silently edits agent-optimizer;
- Treats a synthetic case as a real workflow;
- Publishes a donor candidate;
- Starts a mutating workflow immediately;
- Reimplements agent-builder;
- Fetches a replacement automatically;
- Deletes the rollback version.

## Зависимости

Обязательные companion-навыки в каноническом dependency-графе не объявлены. Проверяйте доступность host-инструментов и ресурсов, на которые ссылается `SKILL.md`.

## Ресурсы пакета

- [`SKILL.md`](SKILL.md) — исполняемый контракт, маршрутизация и правила безопасности.
- [`agents/`](agents/) — UI-метаданные и host-конфигурация.
- [`evals/`](evals/) — routing- и behavior-сценарии.
- [`prompts/`](prompts/) — маршрутные и специализированные промпты.
- [`references/`](references/) — справочники, схемы и контракты.
- [`scripts/`](scripts/) — детерминированные проверки и автоматизация.
- [`vendor/`](vendor/) — зафиксированный снимок зависимых компонентов.

## Проверка результата

- Сверьте маршрутизацию с [`evals/routing.json`](evals/routing.json).
- Сверьте свойства результата с [`evals/behavior.json`](evals/behavior.json).
- Для детерминированной проверки используйте [`scripts/build_rollback_plan.py`](scripts/build_rollback_plan.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/build_vendor_snapshot.py`](scripts/build_vendor_snapshot.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/check_donors.py`](scripts/check_donors.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/classify_e2e_findings.py`](scripts/classify_e2e_findings.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/record_real_workflow.py`](scripts/record_real_workflow.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
