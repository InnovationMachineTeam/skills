# agent-team-builder

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Materializes an approved, versioned agent-team specification into a staged `.agents` structure, canonical definitions, owner-private skills or commands, public capability candidates, host adapters, registry/map transactions and verification evidence.
- **Версия:** `1.0.2`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `build`, `teams`.

## Когда использовать

A reviewed team design is ready to build, rebuild, migrate or dry-run. Requires an exact approved spec, destination and write authority. Do not redesign roles, substitute models or permissions, activate agents, create worktrees, publish private assets, or operate the team; route design changes to agent-team-architect and lifecycle execution to agent-team-manager.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Полный пример команды

Иллюстративный полный вызов; адаптируйте пути, ограничения и критерии приёмки к своей задаче:

```text
/agent-team-builder Check whether this approved team spec is buildable.
```

**Ожидаемый результат:** выбирается маршрут `preflight`; итог перечисляет созданные или изменённые артефакты, фактически выполненные проверки, ограничения, остаточные риски и следующий шаг. Наличие файлов само по себе не считается доказательством установки, активации или публикации.

## Варианты использования

### preflight

- **Пример запроса:** “Check whether this approved team spec is buildable.”
- **Ожидаемый маршрут:** `preflight`.

### dry-run

- **Пример запроса:** “Show the exact files this team build would write.”
- **Ожидаемый маршрут:** `dry-run`.

### build

- **Пример запроса:** “Stage approved agent-team spec 2.1.0.”
- **Ожидаемый маршрут:** `build`.

### rebuild

- **Пример запроса:** “Rebuild generated adapters from the approved canonical spec.”
- **Ожидаемый маршрут:** `rebuild`.

### migrate

- **Пример запроса:** “Migrate this approved team scaffold to the canonical .agents layout.”
- **Ожидаемый маршрут:** `migrate`.


## Ожидаемые результаты

### unapproved

Для запроса “Build this draft team spec now.” результат должен:

- blocks without approved spec;
- requests exact version and hash.

### private

Для запроса “Include an agent-private skill in the team build.” результат должен:

- keeps the skill under its owner;
- excludes it from marketplace packaging.

### staged

Для запроса “Build the approved team.” результат должен:

- uses an exact manifest;
- stages before promotion;
- leaves activation false;
- supports rollback.


## Как проходит выполнение

1. **Gate the build.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Plan the exact write-set.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Materialize into staging.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Verify and promote atomically.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Decide which roles this problem needs.” → `agent-team-architect`.
- “Run this agent team on issue 42.” → `agent-team-manager`.

Критические анти-результаты:

- writes scaffold;
- adds multiple consumers;
- silently changes roles or models.

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
- Для детерминированной проверки используйте [`scripts/check_evals.py`](scripts/check_evals.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/validate_build_manifest.py`](scripts/validate_build_manifest.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
