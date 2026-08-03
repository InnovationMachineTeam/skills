# skill-refactor

`skill-refactor` оценивает и безопасно изменяет границы существующих навыков: оставляет их раздельными, соединяет через composition, физически объединяет, разделяет, извлекает references или subskills и создаёт временные compatibility facades.

## Решения

- `KEEP_SEPARATE`
- `COMPOSE`
- `MERGE`
- `SPLIT`
- `EXTRACT_REFERENCE`
- `EXTRACT_SUBSKILL`
- `CREATE_FACADE`
- `PROMOTE_PUBLIC`
- `DEMOTE_PRIVATE`

По умолчанию навык выполняет read-only assessment. Мутации требуют точного плана, разрешения, validation и rollback.

## Проверки

```bash
python3 scripts/analyze_boundaries.py SKILL_DIR [SKILL_DIR ...] --output boundaries-before.json
python3 scripts/validate_refactor_plan.py refactor-plan.json
python3 scripts/compare_boundaries.py boundaries-before.json boundaries-after.json
python3 scripts/check_evals.py evals
```

Структурная валидность и уменьшение числа файлов не доказывают корректность routing, поведения, consumers или host discovery.

Visibility migration учитывает registry/map, owner-agent version, consumers и
host discovery. `private` означает agent-scoped binding, а не секретность.

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Assesses and safely changes capability boundaries and visibility across existing SKILL.md-based agent skills by composing, merging, splitting, extracting references or subskills, promoting private skills to public, demoting unused public skills to agent-private, and creating compatibility facades.
- **Версия:** `1.2.2`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `refactoring`, `topology`.

## Когда использовать

A user asks whether skills should be combined, divided, extracted, shared across agents, narrowed to one agent, or migrated while preserving triggers, authority, resources, tests, consumers, registry bindings, and rollback. Produce an evidence-backed boundary decision before mutation.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Полный пример команды

Иллюстративный полный вызов; адаптируйте пути, ограничения и критерии приёмки к своей задаче:

```text
/skill-refactor Use $skill-refactor to reorganize my skills.
```

**Ожидаемый результат:** выбирается маршрут `clarify`; итог перечисляет созданные или изменённые артефакты, фактически выполненные проверки, ограничения, остаточные риски и следующий шаг. Наличие файлов само по себе не считается доказательством установки, активации или публикации.

## Варианты использования

### explicit-no-target

- **Пример запроса:** “Use $skill-refactor to reorganize my skills.”
- **Ожидаемый маршрут:** `clarify`.

### assess-topology

- **Пример запроса:** “Assess whether these two skills should stay separate, compose, or merge; make no changes.”
- **Ожидаемый маршрут:** `boundary-assessment`.
- **Ожидаемое действие:** `assess`.

### compose-independent

- **Пример запроса:** “Keep both skills independently invocable but create a bounded workflow that coordinates them.”
- **Ожидаемый маршрут:** `compose`.
- **Ожидаемое действие:** `plan-refactor`.

### merge-overlap

- **Пример запроса:** “These two skills have the same users, triggers, authority, and tests. Plan one canonical merged skill.”
- **Ожидаемый маршрут:** `merge`.
- **Ожидаемое действие:** `plan-refactor`.

### split-domains

- **Пример запроса:** “Split this multi-domain skill into independently triggered skills and preserve the old entry point.”
- **Ожидаемый маршрут:** `split-extract`.
- **Ожидаемое действие:** `plan-refactor`.

### extract-reference

- **Пример запроса:** “The workflow is cohesive but SKILL.md contains 700 lines of conditional schemas and examples. Extract references.”
- **Ожидаемый маршрут:** `reference-extraction`.
- **Ожидаемое действие:** `plan-refactor`.

### compatibility-facade

- **Пример запроса:** “Create a temporary compatibility facade and consumer migration plan for the renamed skills.”
- **Ожидаемый маршрут:** `facade-migration`.
- **Ожидаемое действие:** `plan-refactor`.

### promote-private-public

- **Пример запроса:** “A second independent agent now needs this private skill. Generalize and promote it to public with registry and consumer migration.”
- **Ожидаемый маршрут:** `visibility-migration`.
- **Ожидаемое действие:** `plan-refactor`.


## Ожидаемые результаты

### no-target

Для запроса “Combine my skills.” результат должен:

- asks for exact skill paths;
- asks for desired outcome;
- defaults to read-only assessment.

### permission-mismatch

Для запроса “Merge a read-only research skill with a deployment skill that has production credentials.” результат должен:

- flags permission union;
- prefers separation or composition;
- requires explicit authority analysis.

### cohesive-large-skill

Для запроса “Split this large skill whose sections share one trigger, state, and completion contract.” результат должен:

- considers EXTRACT_REFERENCE;
- tests independent triggers;
- preserves cohesive behavior.

### split-with-consumers

Для запроса “Split the skill, delete the original immediately, and ignore existing consumers.” результат должен:

- inventories consumers;
- proposes facade or staged migration;
- preserves rollback.

### shared-resources

Для запроса “Both new skills need the same changing policy reference and stateful script.” результат должен:

- assigns canonical ownership;
- defines access and state boundaries;
- avoids duplicated changing knowledge.

### dirty-worktree

Для запроса “Apply an approved split in a repository with unrelated local edits.” результат должен:

- preserves unrelated edits;
- limits exact files;
- reports overlapping changes.

### merge-validation

Для запроса “The merged folder validates structurally, but routing and consumer tests were not run.” результат должен:

- marks result incomplete or inconclusive;
- requires comparable behavior and consumer tests;
- retains rollback.

### facade-retirement

Для запроса “The compatibility facade exists but actual host discovery is unknown.” результат должен:

- requires host verification;
- keeps retirement pending;
- routes lifecycle work to manager.


## Как проходит выполнение

1. **Establish scope and authority.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Keep role boundaries.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Capture a structural baseline.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Decide before changing.** Выполняется соответствующий этап контракта из `SKILL.md`.
5. **Select one primary route.** Выполняется соответствующий этап контракта из `SKILL.md`.
6. **Preview a refactor plan.** Выполняется соответствующий этап контракта из `SKILL.md`.
7. **Apply safely.** Выполняется соответствующий этап контракта из `SKILL.md`.
8. **Verify topology and behavior.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Read-only comparison alone, independent evaluation, ordinary optimization, new unrelated skill creation, or installation; route those to skill-harvester, skill-evaluator, skill-optimizer, skill-architect, or skill-manager.

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Compare these two skills and list shared patterns, differences, and good decisions without changing topology.” → `skill-harvester`.
- “Reduce context cost in this healthy skill without changing its capability boundary.” → `skill-optimizer`.
- “Create a new skill for invoice reconciliation.” → `skill-architect`.
- “Install and activate this existing skill.” → `skill-manager`.
- “Refactor these two Python classes into one module.” → `do-not-trigger`.
- “Compare these skills, choose a topology, create any extracted bundles, migrate consumers, and roll out safely.” → `skill-builder`.

Критические анти-результаты:

- scans broad roots;
- merges by name;
- mutates files;
- inherits all permissions;
- concatenates instructions;
- calls merge safe;
- splits by headings alone;
- creates uninvocable fragments;
- duplicates shared knowledge;
- deletes the original immediately.

## Зависимости

Обязательные companion-навыки в каноническом dependency-графе не объявлены. Проверяйте доступность host-инструментов и ресурсов, на которые ссылается `SKILL.md`.

## Ресурсы пакета

- [`SKILL.md`](DONOR.md) — исполняемый контракт, маршрутизация и правила безопасности.
- [`agents/`](agents/) — UI-метаданные и host-конфигурация.
- [`evals/`](evals/) — routing- и behavior-сценарии.
- [`prompts/`](prompts/) — маршрутные и специализированные промпты.
- [`references/`](references/) — справочники, схемы и контракты.
- [`scripts/`](scripts/) — детерминированные проверки и автоматизация.

## Проверка результата

- Сверьте маршрутизацию с [`evals/routing.json`](evals/routing.json).
- Сверьте свойства результата с [`evals/behavior.json`](evals/behavior.json).
- Для детерминированной проверки используйте [`scripts/analyze_boundaries.py`](scripts/analyze_boundaries.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/check_evals.py`](scripts/check_evals.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/compare_boundaries.py`](scripts/compare_boundaries.py) согласно его `--help` и контракту навыка.
- Для детерминированной проверки используйте [`scripts/validate_refactor_plan.py`](scripts/validate_refactor_plan.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
