# agent-refactor

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Assesses and safely changes the capability, ownership or topology boundaries of existing individual agents through merge, split, extraction, composition, promotion to a team, or public/private capability and documentation migration.
- **Версия:** `1.0.2`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `refactoring`, `topology`.

## Когда использовать

An agent has mixed missions, duplicated roles, unsafe authority coupling, excessive context, changing consumers, or needs a versioned topology migration. Do not tune a healthy agent, repair a local defect, design a new agent from scratch, silently rewrite teams or Agentic OS, move folders without consumer migration, or activate the result.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Полный пример команды

Иллюстративный полный вызов; адаптируйте пути, ограничения и критерии приёмки к своей задаче:

```text
/agent-refactor This agent has unrelated analyst and deployer missions with different permissions; assess a split.
```

**Ожидаемый результат:** выбирается маршрут `split`; итог перечисляет созданные или изменённые артефакты, фактически выполненные проверки, ограничения, остаточные риски и следующий шаг. Наличие файлов само по себе не считается доказательством установки, активации или публикации.

## Варианты использования

### split

- **Пример запроса:** “This agent has unrelated analyst and deployer missions with different permissions; assess a split.”
- **Ожидаемый маршрут:** `split`.

### merge

- **Пример запроса:** “Compare these duplicate reviewer agents and plan a safe merge with consumer migration.”
- **Ожидаемый маршрут:** `merge`.

### team

- **Пример запроса:** “Assess migration of this registered overloaded single agent into a team, but do not design the team yet.”
- **Ожидаемый маршрут:** `promote-to-team`.


## Ожидаемые результаты

### folder-only

Для запроса “Move the agent folder and call the split complete.” результат должен:

- requires consumer and registry migration;
- requires coexistence and rollback.

### private-promotion

Для запроса “A second agent wants a private capability; add it to the allow-list.” результат должен:

- rejects multi-owner private access;
- assesses public promotion.

### docs-migration

Для запроса “Split the architecture agent but leave ADR ownership and indexes unchanged.” результат должен:

- migrates document ownership and links;
- blocks incomplete split.


## Как проходит выполнение

1. **Assess the boundary.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Plan a recoverable migration.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “A new delivery problem may need multiple agents; assess and design the minimal team.” → `agent-team-architect`.
- “Reduce this healthy agent's latency without changing boundaries.” → `agent-optimizer`.
- “Fix one malformed tool response regression.” → `agent-doctor`.

Критические анти-результаты:

- treats folder move as complete;
- expands private allow-list;
- orphaned documents.

## Зависимости

- **Обязательный: `agent-architect` >= `1.0.0`.** New individual-agent boundaries require a validated definition contract.
- **Обязательный: `agent-evaluator` >= `1.0.0`.** Old/new topology and consumer migrations require independent evaluation.
- **Обязательный: `agent-manager` >= `1.0.0`.** Lifecycle migration, rollout and retirement belong to the manager.
- **Рекомендуемый: `agent-team-architect` >= `1.1.0`.** Recommended after an existing-agent migration decision promotes the asset into a team.

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
