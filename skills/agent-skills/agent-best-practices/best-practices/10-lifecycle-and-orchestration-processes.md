# Процессы жизненного цикла и оркестрации

Этот файл описывает end-to-end процессы. Сравнение runtime, improvement,
delivery, risk и learning loops, а также lifecycle отдельных сущностей вынесено
в [20-agentic-cycles-and-lifecycles.md](20-agentic-cycles-and-lifecycles.md).

## Универсальный контур

```text
Intent → Context → Specify → Plan → Generate ↔ Validate → Govern
  ↑                                                    ↓
Observe ← Operate ← Deploy ← Release readiness ← Integrate
```

Это не обязательный waterfall. Для простой задачи контур сжимается; в ADLC
Generate, Validate и Observe идут параллельно. Но ни один run не должен терять
intent, evidence и governance.

## 1. Intake и выбор режима

1. Нормализовать запрос в goal, context, constraints, done.
2. Классифицировать неопределённость, риск, reversibility и scope.
3. Проверить существующие capabilities и не создавать дубликат агента.
4. Выбрать механизм: code, workflow, agent, subagents или team.
5. Определить autonomy level и approvals.
6. Создать run/task IDs и начальный trace.

Выход: intent record + выбранный workflow с rationale.

## 2. Discovery

Используйте при неизвестной проблеме или решении:

1. Сформулировать research questions и decision to inform.
2. Разделить источники/аспекты между read-only researchers.
3. Собрать evidence с provenance и датой.
4. Отделить факты, интерпретации и gaps.
5. Провести adversarial synthesis.
6. Сформировать bet: hypothesis, generation target, resolution signal, deadline.
7. Human governance: продолжить, изменить или остановить.

OpenSpec `/explore` намеренно не пишет код и артефакты до прояснения; Agent OS
сначала ищет reference implementations и standards; gstack следует принципу
search before building. Это снижает преждевременную реализацию.

## 3. Requirements

1. Определить stakeholders и system boundary.
2. Извлечь потребности, бизнес-правила и constraints.
3. Создать атомарные functional requirements.
4. Операционализировать quality attributes сценариями и targets.
5. Добавить error, abuse, edge и recovery cases.
6. Зафиксировать assumptions и non-goals.
7. Построить traceability до источников и verification.
8. Независимо проверить ambiguity, conflicts, feasibility и testability.
9. Human approval для scope и high-impact trade-offs.

## 4. Architecture и planning

1. Построить context/container view и critical flows.
2. Найти architecturally significant requirements.
3. Рассмотреть варианты и оформить ADR.
4. Декомпозировать на independently valuable vertical slices.
5. Для каждого slice задать owner, write-set, dependencies и verification.
6. Построить DAG и waves.
7. Добавить threat, migration, rollout и rollback plan.
8. Plan reviewer проверяет достижение goal backward.
9. Зафиксировать preconditions и human checkpoints.

Spec Kit отделяет WHAT от HOW и группирует tasks по independently testable user
stories; GSD добавляет must-haves, artifacts и key links; OpenSpec позволяет
возвращаться между artifacts. Используйте их совместно, не превращая plan в
неизменяемый контракт.

## 5. Execution

Для каждой wave:

1. Проверить dependencies и preconditions read-only действиями.
2. Выдать leases и permission envelopes.
3. Dispatch независимых scoped implementers.
4. Каждый исполнитель тестирует и возвращает evidence.
5. Integration owner проверяет collisions и contracts.
6. Запустить targeted reviews.
7. Обновить durable state и следующий ready set.

Первый slice SHOULD быть tracer/walking skeleton: тонкий production-quality
end-to-end путь, который проверяет интеграцию до расширения.

## 6. Verification

Verification выполняется от outcome:

1. Из goal/spec вывести truths.
2. Для каждой truth определить artifacts и wiring.
3. Проверить live code/runtime, не доверяя summary.
4. Запустить tests/evals и проверить scenarios.
5. Классифицировать `verified`, `failed`, `uncertain`, `human_needed`.
6. Создать gap plan, а не молча исправлять вне роли.
7. Повторить только failed items плюс regression checks.

OpenSpec проверяет completeness/correctness/coherence; GSD — truth/artifact/
wiring. Объединённый gate должен учитывать оба взгляда.

## 7. Release и deploy

1. Проверить версии, migrations, docs, security и rollback.
2. Сформировать release evidence bundle.
3. Policy engine вычисляет требуемые approvals.
4. Deploy agent действует только в approved envelope.
5. Использовать feature flag/canary и автоматические rollback triggers.
6. Верифицировать production behavior и signals.
7. Закрыть change только после observation window.

ADLC подчёркивает agent-orchestrated, human-approved deploy и recoverability
([ADLC](https://www.adlc.io/)).

## 8. Observe и learn

1. Собирать product, system и agent signals.
2. Связывать их с bet, requirement и run.
3. Находить anomalies, drift, high-cost paths и repeated failures.
4. Создавать candidate learnings с provenance.
5. Проверять и утверждать изменения memory/policy.
6. Добавлять production cases в eval dataset.
7. Формировать новые bets или corrective changes.

## Типовые процессы оркестрации

### Parallel research

Разделение по независимым источникам → fan-out → evidence normalization →
conflict resolution → synthesis → source audit.

### Competing-hypothesis debugging

Один investigator на гипотезу → запрещены fixes → общий evidence board →
falsification → root-cause gate → scoped fix → regression verification.

### Cross-layer feature

Contract-first plan → backend/frontend/data agents с непересекающимися
write-sets → integration agent → E2E verifier.

### Review army

Scope detector выбирает релевантных specialists → независимый parallel review →
deduplication → severity/evidence gate → fix owner. gstack добавляет адаптивный
gating по исторической полезности specialist, но security и migrations SHOULD
оставаться insurance checks.

### Evaluator–optimizer

Зафиксировать rubric → producer → evaluator → actionable feedback → bounded
retry → best-candidate selection → human review при неоднозначности.

### Long-running workflow

Durable job manifest → heartbeat → checkpoints → resumable artifacts → timeout
и cancel → human input state → reconciliation после restart.

### Multi-repo change

Shared intent/spec repo → per-repo change owners/worktrees → versioned interface
contracts → integration environment → cross-repo verifier → coordinated release.

## Checkpoint types

- **Decision** — несколько допустимых вариантов, меняющих outcome.
- **Approval** — рискованное действие готово к выполнению.
- **Input required** — отсутствуют credentials/данные/внешняя операция.
- **Verification** — автоматические проверки недостаточны для человеческого
  суждения.
- **Blocker** — precondition доказанно не выполнен.

Checkpoint содержит контекст, варианты, последствия, рекомендацию, evidence и
что продолжится после ответа.

## Pause/resume

Pause сохраняет current task, branch/worktree, commits, decisions, blockers,
active jobs, expected artifacts, verify/resume commands. Resume проверяет drift
и не принимает старое состояние на веру.
