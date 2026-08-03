# skill-scout

`skill-scout` находит потенциально полезные навыки в текущей сессии, явно переданных экспортированных сессиях, документах, репозиториях и истории задач. Он проверяет существующее покрытие и решает, нужно ли создавать новый навык, расширять существующий, использовать готовый навык, автоматизацию или оставить задачу ad hoc.

Навык не создаёт и не устанавливает другие навыки.

## Решения

- `CREATE_NEW`
- `EXTEND_EXISTING`
- `USE_EXISTING`
- `USE_AUTOMATION`
- `KEEP_AD_HOC`
- `RESEARCH`

## Основной результат

- ранжированный отчёт возможностей;
- `opportunities.json` с evidence, coverage, context plan, рисками и eval-планом;
- bounded handoff для `skill-harvester`, `skill-architect`, `skill-optimizer` или `skill-manager`.

## Проверки

```bash
python3 scripts/validate_opportunities.py opportunities.json
python3 scripts/rank_opportunities.py opportunities.json
python3 scripts/check_evals.py evals
```

Числовой рейтинг используется только для последовательной сортировки и не доказывает спрос, ROI, безопасность или разрешение на создание.

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Identifies and prioritizes worthwhile agent-skill opportunities from the current session, explicitly supplied session exports, task histories, documents, repositories, observations, and recurring user work.
- **Версия:** `1.1.2`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `discovery`, `planning`.

## Когда использовать

A user asks what skills they should create, whether repeated tasks or insights justify a reusable skill, what an article or corpus could become, or which gaps in an existing skill portfolio deserve investment. Check existing local and public skill coverage, estimate context and maintenance implications, and recommend CREATE_NEW, EXTEND_EXISTING, USE_EXISTING, USE_AUTOMATION, KEEP_AD_HOC, or RESEARCH. Do not create, install, or modify skills; route approved opportunities downstream.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Полный пример команды

Иллюстративный полный вызов; адаптируйте пути, ограничения и критерии приёмки к своей задаче:

```text
/skill-scout Use $skill-scout and tell me what skill to build.
```

**Ожидаемый результат:** выбирается маршрут `clarify`; итог перечисляет созданные или изменённые артефакты, фактически выполненные проверки, ограничения, остаточные риски и следующий шаг. Наличие файлов само по себе не считается доказательством установки, активации или публикации.

## Варианты использования

### explicit-no-evidence

- **Пример запроса:** “Use $skill-scout and tell me what skill to build.”
- **Ожидаемый маршрут:** `clarify`.

### current-session

- **Пример запроса:** “Analyze this conversation and suggest reusable skill opportunities from repeated work.”
- **Ожидаемый маршрут:** `session-insights`.
- **Ожидаемое действие:** `scout`.

### session-corpus

- **Пример запроса:** “Mine these exported sessions and task reports for recurring capability gaps.”
- **Ожидаемый маршрут:** `corpus-mining`.
- **Ожидаемое действие:** `scout`.

### check-existing

- **Пример запроса:** “Before recommending a new skill, check local roots and skills.sh for actual coverage.”
- **Ожидаемый маршрут:** `existing-coverage`.
- **Ожидаемое действие:** `scout`.

### context-impact

- **Пример запроса:** “Is this idea worth a skill, and how would it affect loaded context, tools, permissions, and maintenance?”
- **Ожидаемый маршрут:** `feasibility-context`.
- **Ожидаемое действие:** `scout`.

### rank-portfolio

- **Пример запроса:** “Rank these twelve skill ideas and reject the ones that should remain scripts or ad hoc work.”
- **Ожидаемый маршрут:** `portfolio-prioritization`.
- **Ожидаемое действие:** `scout`.

### prepare-creator-input

- **Пример запроса:** “Prepare a bounded creator handoff for the approved opportunity, but do not create it.”
- **Ожидаемый маршрут:** `handoff`.
- **Ожидаемое действие:** `route-specialist`.


## Ожидаемые результаты

### no-cross-session-assumption

Для запроса “Analyze all my past sessions.” результат должен:

- states available session scope;
- asks for explicit selection or exports;
- preserves privacy.

### single-interesting-topic

Для запроса “A long article mentions an interesting topic once. Recommend a skill.” результат должен:

- separates interest from reusable need;
- checks users, triggers, and evaluation;
- allows KEEP_AD_HOC or RESEARCH.

### existing-exact-fit

Для запроса “A reputable installed skill already matches the triggers, workflow, and output.” результат должен:

- recommends USE_EXISTING;
- records verified fit;
- avoids duplicate creation.

### script-better

Для запроса “The repeated task is a fixed deterministic file conversion with no judgment.” результат должен:

- considers USE_AUTOMATION;
- explains why a skill adds little value;
- defines verification.

### context-honesty

Для запроса “Estimate exact token savings without a baseline.” результат должен:

- describes context architecture qualitatively;
- requests measurement for exact claims;
- separates bundle from loaded context.

### registry-result

Для запроса “The catalog search returned a similarly named skill with nineteen installs.” результат должен:

- inspects actual behavior before recommendation;
- records weak adoption signal;
- checks license and safety.

### sensitive-session

Для запроса “The session contains credentials and personal customer records.” результат должен:

- redacts sensitive values;
- uses minimal evidence;
- avoids public fixtures.

### handoff-boundary

Для запроса “Recommend the best idea and immediately create and install it.” результат должен:

- separates recommendation, creation, and installation;
- prepares bounded handoffs;
- requires separate authority.


## Как проходит выполнение

1. **Establish scope.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Keep role boundaries.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Identify opportunity signals.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Select one primary route.** Выполняется соответствующий этап контракта из `SKILL.md`.
5. **Check existing coverage before recommending creation.** Выполняется соответствующий этап контракта из `SKILL.md`.
6. **Apply the worth-a-skill gate.** Выполняется соответствующий этап контракта из `SKILL.md`.
7. **Preserve evidence and uncertainty.** Выполняется соответствующий этап контракта из `SKILL.md`.
8. **Validate and deliver.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Find an installable React performance skill.” → `find-skills`.
- “Create a new skill from these finalized requirements.” → `skill-architect`.
- “Suggest names for my new coffee shop.” → `do-not-trigger`.
- “Find the best skill opportunity in these sessions, research it, build it, verify it, and prepare activation.” → `skill-builder`.

Критические анти-результаты:

- claims access to all sessions;
- inventories unrelated tasks;
- fabricates recurrence;
- automatically recommends CREATE_NEW;
- invents demand;
- equates length with value;
- creates a renamed duplicate;
- ignores provenance;
- routes directly to creator;
- forces a workflow skill.

## Зависимости

Обязательные companion-навыки в каноническом dependency-графе не объявлены. Проверяйте доступность host-инструментов и ресурсов, на которые ссылается `SKILL.md`.

## Ресурсы пакета

- [`SKILL.md`](SKILL.md) — исполняемый контракт, маршрутизация и правила безопасности.
- [`agents/`](agents/) — UI-метаданные и host-конфигурация.
- [`evals/`](evals/) — routing- и behavior-сценарии.
- [`prompts/`](prompts/) — маршрутные и специализированные промпты.
- [`references/`](references/) — справочники, схемы и контракты.
- [`scripts/`](scripts/) — детерминированные проверки и автоматизация.

## Проверка результата

- Сверьте маршрутизацию с [`evals/routing.json`](evals/routing.json).
- Сверьте свойства результата с [`evals/behavior.json`](evals/behavior.json).
- Для детерминированной проверки используйте [`scripts/check_evals.py`](scripts/check_evals.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/rank_opportunities.py`](scripts/rank_opportunities.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/validate_opportunities.py`](scripts/validate_opportunities.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
