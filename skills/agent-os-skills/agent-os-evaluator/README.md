# agent-os-evaluator

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Independently evaluates frozen Agentic OS architecture, implementations and release evidence across plane boundaries, schemas, registry reconciliation, policy enforcement, durable execution, knowledge provenance, observability, operator readiness, security, failure recovery, lifecycle and end-to-end outcomes.
- **Версия:** `1.0.2`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `agent-os`, `evaluation`.

## Когда использовать

Evaluation plans, conformance, chaos/security/load tests, release gates, comparisons or migration evidence. Do not repair the candidate during a frozen run, reveal holdouts, average away blockers, or authorize deployment.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Полный пример команды

Иллюстративный полный вызов; адаптируйте пути, ограничения и критерии приёмки к своей задаче:

```text
/agent-os-evaluator Independently evaluate this frozen Agentic OS release candidate.
```

**Ожидаемый результат:** выбирается маршрут `release-gate`; итог перечисляет созданные или изменённые артефакты, фактически выполненные проверки, ограничения, остаточные риски и следующий шаг. Наличие файлов само по себе не считается доказательством установки, активации или публикации.

## Варианты использования

### release

- **Пример запроса:** “Independently evaluate this frozen Agentic OS release candidate.”
- **Ожидаемый маршрут:** `release-gate`.

### chaos

- **Пример запроса:** “Run the failure and recovery evaluation suite.”
- **Ожидаемый маршрут:** `chaos`.


## Ожидаемые результаты

### blocker

Для запроса “Security fails but aggregate score is high.” результат должен:

- blocks release and cites raw evidence.

### holdout

Для запроса “Builder asks for hidden expected answers.” результат должен:

- protects holdout and frozen contract.


## Как проходит выполнение

1. Проверяется применимость навыка и полнота входных данных.
2. Выбирается самый узкий безопасный маршрут.
3. Создаются или проверяются требуемые артефакты.
4. Результат сверяется с контрактом и передаётся вместе с рисками и следующим шагом.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Fix every failure you find during evaluation.” → `doctor`.

Критические анти-результаты:

- averages away blocker;
- reveals answers or patches candidate.

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
- Для детерминированной проверки используйте [`scripts/validate_release_evidence.py`](scripts/validate_release_evidence.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
