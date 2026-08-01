# role-skill-architect

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Turns one approved role-agent capability into a researched, bounded, host-native skill package with triggers, method, knowledge provenance, contracts, examples, tests, evals, security, maintenance, and a justified implementation proposal.
- **Версия:** `1.0.1`.
- **Видимость:** package-private: вызывается только родительским `agent-master` и не публикуется отдельно.

## Когда использовать

Используйте навык, когда запрос соответствует его назначению и границам ответственности из `SKILL.md`.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Варианты использования

### approved-capability

- **Пример запроса:** “Agent-master dispatches one approved evidence-triangulation capability from a designed reviewer role.”
- **Ожидаемый маршрут:** `role-skill-architect`.


## Ожидаемые результаты

### classification-gate

Для запроса “The proposal is only a stable one-line prohibition for one agent.” результат должен:

- rejects a full skill;
- recommends an inline rule or private command;
- explains maintenance tradeoff.

### research-provenance

Для запроса “Build a role skill that depends on current professional standards.” результат должен:

- researches authoritative current sources;
- records provenance and limitations;
- preserves conflicts.

### repo-native-package

Для запроса “Create the skill in this repository from the supplied complete capability contract.” результат должен:

- uses repository-native SKILL.md structure;
- adds only necessary resources;
- creates routing and behavior evals.


## Как проходит выполнение

1. **Verify and classify the proposal.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Research the method.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Build the host-native package.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Evaluate and hand off.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Create the entire specialist reviewer agent first.” → `role-agent-architect`.
- “Implement the already approved deterministic schema validator proposed by this skill.” → `skill-implementation-engineer`.

Критические анти-результаты:

- scaffolds a large package;
- treats an exemplar repository as a standard;
- forces skill.yaml;
- adds empty directories;
- claims installation.

## Зависимости

Внешних зависимостей каталога нет. Родительский `agent-master` передаёт этому private-навыку только ограниченный dispatch-конверт и проверяет его результат.

## Ресурсы пакета

- [`SKILL.md`](SKILL.md) — исполняемый контракт, маршрутизация и правила безопасности.
- [`evals/`](evals/) — routing- и behavior-сценарии.
- [`references/`](references/) — справочники, схемы и контракты.

## Проверка результата

- Сверьте маршрутизацию с [`evals/routing.json`](evals/routing.json).
- Сверьте свойства результата с [`evals/behavior.json`](evals/behavior.json).
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
