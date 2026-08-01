# agent-registry-manager

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Governs typed desired-state registries and versioned bindings for Agentic OS agents, skills, commands, workflows, teams, tools, models and policies, and reconciles them with observed host/runtime state.
- **Версия:** `1.0.1`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `registry`, `governance`.

## Когда использовать

Inventory, candidate registration, optimistic transactions, drift detection, quarantine, deprecation, migration or retirement at platform scope. Do not equate registered with trusted or active, bypass ownership/private visibility, edit generated views as canonical data, or mutate on a stale revision.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Варианты использования

### inventory

- **Пример запроса:** “Inventory desired and observed Agentic OS assets.”
- **Ожидаемый маршрут:** `inventory`.

### reconcile

- **Пример запроса:** “Reconcile registry drift at revisions 4 and 2.”
- **Ожидаемый маршрут:** `reconcile`.


## Ожидаемые результаты

### stale

Для запроса “Apply a transaction based on a stale revision.” результат должен:

- rejects stale writer.

### private

Для запроса “Bind a private skill to a second agent.” результат должен:

- rejects private escape and records evidence.


## Как проходит выполнение

1. Проверяется применимость навыка и полнота входных данных.
2. Выбирается самый узкий безопасный маршрут.
3. Создаются или проверяются требуемые артефакты.
4. Результат сверяется с контрактом и передаётся вместе с рисками и следующим шагом.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Install this public skill in Codex.” → `skill-manager`.

Критические анти-результаты:

- partially mutates registry;
- expands allow-list.

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
- Для детерминированной проверки используйте [`scripts/validate_reconcile_plan.py`](scripts/validate_reconcile_plan.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
