# role-agent-architect

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Creates one complete bounded specialist-agent specification from an approved process-orchestrator role, including inherited-skill audit, capability gaps, role contract, knowledge, tools, permissions, tasks, handoffs, self-review, Human-in-the-loop, errors, context, metrics, evals, agent card, and system prompt.
- **Версия:** `1.0.2`.
- **Видимость:** package-private: вызывается только родительским `agent-master` и не публикуется отдельно.

## Когда использовать

Используйте навык, когда запрос соответствует его назначению и границам ответственности из `SKILL.md`.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Полный пример команды

Этот package-private навык не вызывается напрямую. Иллюстративный запрос передаётся через родительский `/agent-master`:

```text
/agent-master Agent-master dispatches the approved evidence-reviewer role with the orchestrator spec and its proposed skills.
```

**Ожидаемый результат:** выбирается маршрут `role-agent-architect`; итог перечисляет созданные или изменённые артефакты, фактически выполненные проверки, ограничения, остаточные риски и следующий шаг. Наличие файлов само по себе не считается доказательством установки, активации или публикации.
Прямой `/role-agent-architect` не является поддерживаемой публичной командой; родитель `agent-master` обязан передать ограниченный dispatch-контракт и проверить результат.

## Варианты использования

### approved-role

- **Пример запроса:** “Agent-master dispatches the approved evidence-reviewer role with the orchestrator spec and its proposed skills.”
- **Ожидаемый маршрут:** `role-agent-architect`.


## Ожидаемые результаты

### skill-audit

Для запроса “The orchestrator proposes six overlapping skills for one reviewer role.” результат должен:

- audits every proposed skill;
- explains merge, split, move, or exclusion;
- separates skills from knowledge, tools, rules, and authority.

### neighbor-boundary

Для запроса “The role is an analyst, but the task asks it to approve a regulated release.” результат должен:

- refuses approval authority;
- creates a handoff or Human gate;
- preserves the analyst output.

### complete-package

Для запроса “Create the specialist agent package for an approved role.” результат должен:

- returns role contract;
- returns input/output and handoff contracts;
- returns system prompt and agent card;
- returns eval cases.


## Как проходит выполнение

1. **Verify the handoff.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Audit inherited capabilities.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Specify bounded behavior.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Design interactions and recovery.** Выполняется соответствующий этап контракта из `SKILL.md`.
5. **Evaluate and hand off.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Create some useful agents for my company.” → `agent-master`.
- “Turn the approved evidence-triangulation capability into a skill package.” → `role-skill-architect`.

Критические анти-результаты:

- silently drops capabilities;
- copies every proposal unchanged;
- impersonates the approver;
- claims runtime activation.

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
