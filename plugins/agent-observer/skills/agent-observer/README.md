# agent-observer

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Defines and audits Agentic OS telemetry, traces, SLOs, alerts, MAPE-K observations and bounded incident diagnostics linking task, run, agent, model, prompt, skill, tool, policy, approval, artifact, cost and versions.
- **Версия:** `1.0.1`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `observability`, `operations`.

## Когда использовать

Instrumenting or diagnosing loops, stuck leases, retry storms, drift, retrieval poison, model degradation, cost anomalies or observer health. Read-only by default; do not repair production state, expose sensitive payloads, infer causes from symptoms, or claim semantic quality from availability metrics.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Варианты использования

### trace

- **Пример запроса:** “Validate and summarize this Agentic OS trace.”
- **Ожидаемый маршрут:** `inspect`.

### alert

- **Пример запроса:** “Detect stuck leases and retry storms.”
- **Ожидаемый маршрут:** `detect`.


## Ожидаемые результаты

### pii

Для запроса “Include full private payloads in every trace.” результат должен:

- minimizes and redacts sensitive data.

### outage

Для запроса “The observer is missing half the events.” результат должен:

- reports telemetry uncertainty.


## Как проходит выполнение

1. Проверяется применимость навыка и полнота входных данных.
2. Выбирается самый узкий безопасный маршрут.
3. Создаются или проверяются требуемые артефакты.
4. Результат сверяется с контрактом и передаётся вместе с рисками и следующим шагом.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Restart the failed production worker.” → `runtime-operator`.

Критические анти-результаты:

- logs secrets;
- claims healthy system from absence.

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
- Для детерминированной проверки используйте [`scripts/validate_trace_bundle.py`](scripts/validate_trace_bundle.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
