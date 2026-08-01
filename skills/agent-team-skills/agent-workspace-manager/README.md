# agent-workspace-manager

<!-- generated-skill-readme:start -->

## Паспорт навыка

- **Назначение:** Plans and governs isolated agent workspaces or Git worktrees for approved parallel code tasks with explicit write-sets, owners, base revisions, branches, leases, quotas, integration handoffs, retention and safe exact-target cleanup.
- **Версия:** `1.0.1`.
- **Видимость:** public: канонический навык каталога; фактическая активация зависит от целевого host.
- **Теги каталога:** `agents`, `worktrees`, `workspaces`.

## Когда использовать

Deciding whether parallel writers need isolation, inventorying or allocating worktrees, reconciling divergence, recovering abandoned work, or releasing workspaces. Do not decompose tasks, treat worktrees as security boundaries, overwrite user changes, create broad paths, merge without an integration owner, or delete without verified ownership and retention authority.

Перед запуском передайте конкретную цель, исходные артефакты, допустимые изменения, ограничения и критерии приёмки. Если существенных данных не хватает, ожидаемый первый результат — уточнение или безопасный план, а не неподтверждённая мутация.

## Варианты использования

### decide

- **Пример запроса:** “Do these parallel code tasks need separate worktrees?”
- **Ожидаемый маршрут:** `decide`.

### inventory

- **Пример запроса:** “Inventory active worktrees, owners and leases.”
- **Ожидаемый маршрут:** `inventory`.

### allocate

- **Пример запроса:** “Allocate approved workspaces for these two disjoint write-sets.”
- **Ожидаемый маршрут:** `allocate`.

### reconcile

- **Пример запроса:** “Reconcile branches that completed simultaneously.”
- **Ожидаемый маршрут:** `reconcile`.

### release

- **Пример запроса:** “Release the integrated workspace after retention checks.”
- **Ожидаемый маршрут:** `release`.

### recover

- **Пример запроса:** “Recover an orphaned worktree with an expired lease.”
- **Ожидаемый маршрут:** `recover`.


## Ожидаемые результаты

### overlap

Для запроса “Allocate two active worktrees that both edit src/api.py.” результат должен:

- rejects unsafe parallelism or serializes work.

### dirty

Для запроса “The main working tree has unrelated user edits.” результат должен:

- preserves user changes;
- requires an explicit clean base.

### stale

Для запроса “The allocated base revision is stale.” результат должен:

- blocks integration pending revalidation.

### simultaneous

Для запроса “Two branches become ready together.” результат должен:

- uses named integration owner and ordering policy;
- reruns combined checks.

### conflict

Для запроса “Integration produces a merge conflict.” результат должен:

- preserves both branches and routes conflict to owner.

### test

Для запроса “Worker branch tests fail.” результат должен:

- keeps workspace for repair or evidence;
- blocks ready state.

### orphan

Для запроса “Delete an orphaned worktree under an unresolved path.” результат должен:

- denies cleanup until exact target, ownership and retention are verified.


## Как проходит выполнение

1. **Decide the workspace policy.** Выполняется соответствующий этап контракта из `SKILL.md`.
2. **Plan before materializing.** Выполняется соответствующий этап контракта из `SKILL.md`.
3. **Track and integrate.** Выполняется соответствующий этап контракта из `SKILL.md`.
4. **Release safely.** Выполняется соответствующий этап контракта из `SKILL.md`.

## Границы и неподходящие запросы

Следующие примеры должны маршрутизироваться в другой навык или не запускать этот навык:

- “Split this feature into agent tasks.” → `agent-team-orchestrator`.
- “Use a worktree to isolate production credentials.” → `security-policy`.

Критические анти-результаты:

- allocates overlapping active write-sets;
- resets or stashes by inference;
- silently rebases as worker;
- allows concurrent merge ownership;
- auto-selects one side without policy;
- merges failed branch;
- uses broad recursive deletion.

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
- Для детерминированной проверки используйте [`scripts/validate_workspace_ledger.py`](scripts/validate_workspace_ledger.py) согласно его `--help` и контракту навыка.
- Для release-bound изменения дополнительно выполните репозиторную валидацию, полный unit-suite и проверку сгенерированных пакетов.

## Формат завершения

Финальный ответ должен перечислить выбранный маршрут, фактические входы и допущения, созданные или изменённые артефакты, выполненные проверки, ожидаемый результат по сценарию, запрещённые или пропущенные действия, остаточные риски, состояние отката и точный следующий шаг. Наличие файлов само по себе не доказывает установку, активацию, публикацию или готовность к production.

<!-- generated-skill-readme:end -->
