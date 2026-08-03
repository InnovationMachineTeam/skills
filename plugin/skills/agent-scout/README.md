# agent-scout

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Identifies and prioritizes justified opportunities for one agent or subagent from tasks, sessions, code, documents, incidents and recurring work, then checks whether code, a model call, workflow, existing agent, team or Agentic OS already fits.
- **Версия:** `1.0.2`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `discovery`, `planning`.

## Когда использовать

Deciding whether to create or extend an agent, finding duplicate or missing agent capabilities, or producing an evidence-backed agent opportunity manifest. Read only by default. Do not design, build, install or activate agents, treat frequency or persona names as proof, or recommend a new agent without coverage, maintenance, authority and evaluation analysis.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Полный пример команды

Иллюстративный полный вызов; адаптируйте пути, ограничения и критерии приёмки к своей задаче:

```text
/agent-scout Review these recurring tasks and tell me which ones justify an agent.
```

**Ожидаемый результат:** выбирается маршрут `portfolio`; итог перечисляет созданные или изменённые артефакты, фактически выполненные проверки, ограничения, остаточные риски и следующий шаг. Наличие файлов само по себе не считается доказательством установки, активации или публикации.

## Варианты использования

### discover

- **Пример запроса:** “Review these recurring tasks and tell me which ones justify an agent.”
- **Ожидаемый маршрут:** `portfolio`.

### duplicate

- **Пример запроса:** “Check whether this proposed reviewer duplicates an installed agent.”
- **Ожидаемый маршрут:** `coverage`.

### session

- **Пример запроса:** “Find potential agent opportunities in these session notes without creating them.”
- **Ожидаемый маршрут:** `discover`.


## Ожидаемые результаты

### deterministic

Для запроса “Create an agent to sort a fixed JSON array.” результат должен:

- selects code or script;
- rejects unnecessary autonomy.

### unknown

Для запроса “Public search failed because network is unavailable; label coverage none.” результат должен:

- labels coverage unknown;
- records search failure.

### docs

Для запроса “The proposed architect agent needs ADRs; create every docs folder now.” результат должен:

- records documentation needs only;
- defers structure to architect.


## Как проходит выполнение

1. **Inventory and compare.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Apply the worth gate.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Find reusable skill opportunities in this article.” → `skill-scout`.
- “Design the exact definition for this approved agent.” → `agent-architect`.

Критические анти-результаты:

- rewards agent novelty;
- claims none;
- creates directories.

## Зависимости

- **Рекомендуемый: `agent-best-practices` >= `1.0.0`.** Provides selection, lifecycle and maintenance criteria.
- **Рекомендуемый: `agent-context` >= `1.0.0`.** Recommended when the opportunity decision needs additional evidence.

Отсутствующая обязательная зависимость блокирует только принадлежащий ей маршрут. Рекомендуемые зависимости повышают качество доказательств, но не должны имитироваться самим навыком.

## Ресурсы пакета

- [`SKILL.md`](SKILL.md) — исполняемый контракт, маршрутизация и правила безопасности.
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
