# agent-os-architect

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Designs the minimum justified Agentic OS across experience, control, execution, knowledge, assurance and operations planes, including desired versus observed state, identities, schemas, policy points, protocols, SLOs, threat and failure models, deployment topology and staged evolution.
- **Версия:** `1.0.1`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `agent-os`, `architecture`.

## Когда использовать

A team runtime is no longer sufficient and a user needs a platform architecture, build/extend/buy comparison, bounded walking skeleton or Agentic OS ADR. Design only; do not bootstrap infrastructure, operate runs, change registries or policies, or issue release verdicts.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Варианты использования

### design

- **Пример запроса:** “Design a minimal Agentic OS for multiple durable release runs.”
- **Ожидаемый маршрут:** `design`.

### buy

- **Пример запроса:** “Compare build, extend and buy for our agent control plane.”
- **Ожидаемый маршрут:** `compare`.


## Ожидаемые результаты

### reject-platform

Для запроса “Create Agentic OS for one short task.” результат должен:

- returns simpler workflow unless platform evidence exists.

### threats

Для запроса “Architect a multi-tenant runtime.” результат должен:

- defines six planes, trust zones, policy points, SLOs and recovery.


## Как проходит выполнение

1. **Inventory and compare.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Design the vertical slice.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Design two agents for one code review.” → `agent-team-architect`.

Критические анти-результаты:

- adds infrastructure by default;
- treats LLM output as enforcement.

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
- Для детерминированной проверки используйте [`scripts/validate_architecture.py`](scripts/validate_architecture.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
