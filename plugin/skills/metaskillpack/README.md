# metaskillpack

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Provides a self-contained, explicitly invoked toolkit for creating, discovering, researching, optimizing, diagnosing, governing, harvesting, refactoring, evaluating, packaging, and orchestrating agent skills through isolated snapshots of the InnovationMachine metaskills.
- **Версия:** `1.4.1`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `orchestration`, `composite`, `metaskills`.

## Когда использовать

Используйте навык, когда запрос соответствует его назначению и границам ответственности из `SKILL.md`.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Варианты использования

### create

- **Пример запроса:** “create invoice-reviewer from this approved specification”
- **Ожидаемый маршрут:** `основной маршрут навыка`.

### scout

- **Пример запроса:** “scout these session exports”
- **Ожидаемый маршрут:** `основной маршрут навыка`.

### research-context-build

- **Пример запроса:** “research invoice-reviewer use docs/ and the repository”
- **Ожидаемый маршрут:** `основной маршрут навыка`.

### optimize

- **Пример запроса:** “optimize invoice-reviewer reduce false triggers”
- **Ожидаемый маршрут:** `основной маршрут навыка`.

### doctor

- **Пример запроса:** “doctor invoice-reviewer script fails on empty CSV”
- **Ожидаемый маршрут:** `основной маршрут навыка`.

### manage

- **Пример запроса:** “manage invoice-reviewer preview an upgrade”
- **Ожидаемый маршрут:** `основной маршрут навыка`.

### harvest

- **Пример запроса:** “harvest https://github.com/example/public-repo extract patterns read-only”
- **Ожидаемый маршрут:** `основной маршрут навыка`.

### refactor

- **Пример запроса:** “refactor skills/a split into two coherent skills”
- **Ожидаемый маршрут:** `основной маршрут навыка`.


## Ожидаемые результаты

### explicit-only-collision

Для запроса “Optimize this healthy skill, but metaskillpack was not named.” результат должен:

- does not implicitly claim the request;
- leaves routing to the individual skill-optimizer.

### progressive-mode-loading

Для запроса “$metaskillpack doctor broken-skill” результат должен:

- loads donors.json and only vendor/skill-doctor/DONOR.md initially;
- reports donor version and selected mode.

### research-compatibility-route

Для запроса “$metaskillpack research invoice-reviewer from docs and repository” результат должен:

- uses skill-harvester context-build;
- does not require a nonexistent skill-context donor.

### run-workflow-gate

Для запроса “$metaskillpack run productionize this recurring task” результат должен:

- proposes two to four workflows with one recommendation;
- waits for selection before skill-builder execution.

### upgrade-current-noop

Для запроса “$metaskillpack upgrade when all donor versions and digests match” результат должен:

- reports an evidence-backed current status;
- writes no files.

### upgrade-same-version-drift

Для запроса “A donor script changed but metadata.version did not.” результат должен:

- detects tree digest drift;
- marks the donor changed and flags missing version discipline.

### upgrade-missing-donor

Для запроса “skill-evaluator cannot be found in any supplied donor root.” результат должен:

- stops before the upgrade master prompt;
- lists searched roots and asks for restoration, installation, or an explicit architecture change.

### upgrade-readonly-donors

Для запроса “Rebuild from newer source donors.” результат должен:

- copies donor inputs into a fresh candidate;
- validates before an authorized promotion.


## Как проходит выполнение

1. **Parse the invocation.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Select a mode.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Dispatch one snapshot.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Handle native control modes.** Выполняется соответствующий этап контракта из `SKILL.md`.
5. **Treat run as an advisory gate.** Выполняется соответствующий этап контракта из `SKILL.md`.
6. **Preserve boundaries.** Выполняется соответствующий этап контракта из `SKILL.md`.
7. **Verify the pack.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Навык не должен расширять полученные полномочия, скрывать пропущенные проверки, выполнять необратимые или внешние действия без явного разрешения либо заявлять состояние host только по наличию файлов.

Критические анти-результаты:

- loads the full pack;
- claims that keyword optimize is sufficient activation;
- preloads every donor;
- uses skill-optimizer before a verified recovery;
- fabricates skill-context;
- installs an external namesake;
- starts the recommended flow immediately;
- asks the user to name internal specialists;
- rebuilds identical snapshots;
- bumps the pack version.

## Зависимости

Обязательные companion-навыки в каноническом dependency-графе не объявлены. Проверяйте доступность host-инструментов и ресурсов, на которые ссылается `SKILL.md`.

## Ресурсы пакета

- [`SKILL.md`](SKILL.md) — исполняемый контракт, маршрутизация и правила безопасности.
- [`agents/`](agents/) — UI-метаданные и host-конфигурация.
- [`evals/`](evals/) — routing- и behavior-сценарии.
- [`prompts/`](prompts/) — маршрутные и специализированные промпты.
- [`references/`](references/) — справочники, схемы и контракты.
- [`scripts/`](scripts/) — детерминированные проверки и автоматизация.
- [`vendor/`](vendor/) — зафиксированный снимок зависимых компонентов.

## Проверка результата

- Сверьте маршрутизацию с [`evals/routing.json`](evals/routing.json).
- Сверьте свойства результата с [`evals/behavior.json`](evals/behavior.json).
- Для детерминированной проверки используйте [`scripts/build_snapshot.py`](scripts/build_snapshot.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/check_donors.py`](scripts/check_donors.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/check_evals.py`](scripts/check_evals.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/donor_utils.py`](scripts/donor_utils.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/route_command.py`](scripts/route_command.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
