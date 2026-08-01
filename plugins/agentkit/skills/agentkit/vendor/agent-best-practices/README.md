# agent-best-practices

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Maintains and applies an evidence-linked corpus of best practices for individual agents, subagents, agent teams, orchestration, documentation, evaluation and Agentic OS.
- **Версия:** `1.0.1`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `research`, `governance`.

## Когда использовать

Querying agent design guidance, auditing an agent or agent-oriented skill against practices, checking source freshness, reconciling changed guidance, rebuilding the corpus, or preparing a bounded portfolio-change prompt. Do not treat platform examples as universal rules, perform open-ended research without scope, edit active agents, or activate changes.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Варианты использования

### query

- **Пример запроса:** “What documentation contract should a software-architecture agent have?”
- **Ожидаемый маршрут:** `query`.

### audit

- **Пример запроса:** “Audit this agent definition against current lifecycle and delegation practices.”
- **Ожидаемый маршрут:** `apply`.

### refresh

- **Пример запроса:** “Check whether the official agent sources changed and prepare a corpus rebuild candidate.”
- **Ожидаемый маршрут:** `refresh`.


## Ожидаемые результаты

### scope-platform-fact

Для запроса “A Cursor guide recommends a setting; make it mandatory for every host.” результат должен:

- keeps platform scope;
- requires evidence before universal rule.

### conflicting-sources

Для запроса “Two official sources conflict about delegation limits.” результат должен:

- records scope and revisions;
- blocks silent reconciliation.

### docs-taxonomy

Для запроса “Create every possible docs folder for a tiny advisory agent.” результат должен:

- requires owned consumers;
- creates directories on demand.


## Как проходит выполнение

1. **Select one route.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Preserve evidence integrity.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Apply documentation practices.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Validate and complete.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Create and activate a production coding agent now.” → `agent-builder`.
- “Evaluate the routing description of this PDF skill.” → `skill-evaluator`.

Критические анти-результаты:

- promotes platform fact to universal MUST;
- silently chooses one;
- creates empty taxonomy.

## Зависимости

Обязательные companion-навыки в каноническом dependency-графе не объявлены. Проверяйте доступность host-инструментов и ресурсов, на которые ссылается `SKILL.md`.

## Ресурсы пакета

- [`SKILL.md`](DONOR.md) — исполняемый контракт, маршрутизация и правила безопасности.
- [`agents/`](agents/) — UI-метаданные и host-конфигурация.
- [`evals/`](evals/) — routing- и behavior-сценарии.
- [`scripts/`](scripts/) — детерминированные проверки и автоматизация.

## Проверка результата

- Сверьте маршрутизацию с [`evals/routing.json`](evals/routing.json).
- Сверьте свойства результата с [`evals/behavior.json`](evals/behavior.json).
- Для детерминированной проверки используйте [`scripts/validate_corpus.py`](scripts/validate_corpus.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
