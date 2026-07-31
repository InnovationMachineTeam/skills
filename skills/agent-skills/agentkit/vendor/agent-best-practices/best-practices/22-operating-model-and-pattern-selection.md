# Operating model и выбор паттернов

## Сначала классифицируйте задачу

Выбор начинается не с количества агентов. Оцените восемь осей:

| Ось | Низкое значение | Высокое значение | Архитектурное следствие |
|---|---|---|---|
| Неопределённость | Известный алгоритм | Путь зависит от evidence | Code/pipeline → adaptive agent |
| Декомпозируемость | Сильная связность | Независимые части | Single context → fork–join |
| Side-effect risk | Read-only/reversible | External/irreversible | Autonomy → approval/saga |
| Длительность | Секунды | Часы/дни | In-memory → durable workflow |
| Межсистемность | Один runtime | Vendors/organizations | Local calls → protocol/contracts |
| Требуемая независимость | Self-check достаточен | Conflict/high stakes | Reflection → independent verifier |
| Изменчивость | Stable facts/process | Dynamic environment | Snapshot → retrieval/observe/reconcile |
| Масштаб | Один run | Multi-tenant/high volume | Inline → queues, quotas, SRE |

Дополнительно определите sensitivity, latency SLO, cost envelope, auditability,
human judgment и blast radius.

## Лестница выбора

```text
Можно решить детерминированным кодом?
  yes → code/tool + tests
  no  → Достаточен один bounded model call?
          yes → structured generation + validation
          no  → Известна стабильная последовательность?
                  yes → workflow/pipeline
                  no  → Нужны новые наблюдения и адаптация?
                          yes → single agent with tools
                          no  → пересмотреть постановку

Независимые части дают доказанный выигрыш?
  yes → subagents/fork–join

Нужна peer coordination или разделённое владение?
  yes → agent team

Нужны durable multi-tenant governance и operations?
  yes → Agent OS platform patterns
```

Каждый переход требует eval evidence или обязательной boundary-причины:
разные permissions, context isolation, ownership, concurrency или protocol.

## Pattern recipes

### Исследование

```text
intent/questions
  → router по независимым темам
  → read-only researchers (fork–join)
  → evidence blackboard с provenance
  → contradiction resolver
  → synthesis
  → source/claim verifier
```

Роли: intent owner, research planner, source specialists, synthesizer,
independent verifier. Цикл: Build–measure–learn для discovery; bounded
generate–evaluate для отчёта.

### Разработка feature

```text
intent/spec → architect/planner → DAG
→ worktree-per-write-set executors
→ integration owner → automated tests/evals
→ independent verifier → release gate → canary → observe
```

Роли: product/intent owner, architect, implementers, integration owner,
test/eval, security по risk, release owner, SRE. Цикл: ADLC + TDD/eval-driven;
PDCA улучшает сам процесс поставки.

### High-risk automation

```text
map risk → plan → simulate/shadow → evidence gate → human approval
→ least-privilege execution → postcondition → canary/progressive
→ monitoring → compensation/rollback
```

Добавьте PDP/PEP, saga, immutable audit и separation of duties. Agent не может
сам расширять envelope или считать отсутствие ответа approval.

### Диагностика инцидента

```text
detect → triage/contain → competing hypotheses
→ evidence blackboard → falsification → root-cause gate
→ scoped remediation → recovery verification → after-action review
```

OODA управляет быстрыми решениями; MAPE-K — автоматическими stabilizing
controllers; double-loop review проверяет ошибочные assumptions после инцидента.

### Создание и развитие skill

```text
scout/duplication check → context harvest → skill architecture
→ atomic/composite build → trigger + outcome evals → security review
→ package/publish → install/canary → observe → optimize/doctor
→ upgrade or deprecate/retire
```

Роли: sponsor, skill architect/author, source curator, eval designer, security
reviewer, publisher, marketplace owner, migration steward.

### Agent OS

```text
inventory/contracts → registry → hybrid control plane
→ sandboxed execution + durable state → policy/evidence gates
→ telemetry/budgets → reconciliation/incidents
→ versioned rollout → lifecycle governance
```

Начните с одного workflow и общих primitives, а не с универсальной платформы.
Платформенный слой извлекается после появления повторяемых требований.

## Организационная модель

### Три уровня владения

1. **Asset ownership** — конкретный agent, skill, workflow, tool или dataset.
2. **Service ownership** — end-to-end user journey и production SLO.
3. **Platform/governance ownership** — registry, runtime, policy, security и
   portfolio lifecycle.

Локально успешный agent может ухудшать общий journey, поэтому service owner
владеет сквозным outcome. Platform owner не принимает продуктовые решения, а
обеспечивает paved road и guardrails.

### Federated governance

Центральная платформа задаёт minimum controls, manifests, risk tiers, identity,
telemetry и publication gates. Доменные команды владеют capabilities, eval cases
и on-call. Исключения имеют owner, rationale, expiry и compensating controls.

### Portfolio review

Периодически проверяйте inventory:

- usage, success, safety, latency и cost;
- дублирующие/перекрывающиеся agents и skills;
- stale owners, dependencies, sources и eval datasets;
- compatibility и unsupported runtimes;
- open incidents, exceptions и technical debt;
- candidates на merge, split, deprecation или retirement.

## Gates по risk tier

| Tier | Пример | До запуска | Во время | После |
|---|---|---|---|---|
| R0 | Read-only draft | Basic validation | Budget | Sample review |
| R1 | Reversible local edit | Tests + scope | Checkpoints | Diff + verify |
| R2 | Shared repo/publish candidate | Independent eval + security | Approval at publish | Canary + audit |
| R3 | Production/data/money | Threat model + SoD + accountable approval | Strong PEP + live monitoring | Postcondition + rollback window |
| R4 | Safety/legal critical | Formal governance and domain authority | Human command, constrained automation | Independent audit and incident readiness |

Tier определяется максимальным потенциальным impact, а не уверенностью модели.
Понижать tier может только утверждённый control evidence.

## Метрики без metric gaming

Сбалансированный набор:

- outcome success и task completion;
- correctness/groundedness и severity-weighted failures;
- safety violations, denied/approved actions и near misses;
- latency, queue time, handoffs, retries и loop depth;
- token/tool/compute cost на успешный outcome;
- human intervention, override и escalation quality;
- rollback/recovery time и orphan rate;
- user/customer value и unintended impacts;
- lifecycle health: owner/source/eval freshness, deprecated dependents.

Aggregate score не заменяет hard safety floors и анализ подгрупп. Связывайте
telemetry с exact versions и intent class.

## Документация operating model

Минимальный набор в `docs/`:

```text
docs/
  agents/          # contracts, cards, ownership, versions
  skills/          # capability map, trigger boundaries, donor manifests
  workflows/       # state/DAG definitions, checkpoints, recovery
  architecture/    # planes, contracts, ADRs, threat models
  operations/      # SLO, dashboards, runbooks, incidents
  assurance/       # eval plans, evidence, gates, known limitations
  governance/      # policies, risk tiers, approvals, exceptions
  lifecycle/       # inventory, deprecations, migrations, retirement
```

Каждый документ имеет owner, audience, source of truth, freshness trigger и
consumer. Runtime state и generated evidence не копируются вручную в prose;
документ ссылается на canonical store.

## Definition of ready и done

### Ready для нового agent/skill

- доказана потребность и проверены дубликаты;
- определены intent, users, non-goals и risk tier;
- выбран минимально достаточный механизм;
- назначены owner, verifier, operator и retirement path;
- существуют eval plan, permissions и source/provenance plan.

### Done для production capability

- versioned contract и package опубликованы;
- functional, negative-trigger, safety и regression evals пройдены;
- owner/SLO/telemetry/runbook/alerts работают;
- policy, approvals, sandbox и credentials проверены;
- rollback, deprecation и retirement механизмы доступны;
- production observation подтверждает outcome в заданном окне.

## Эволюция зрелости

| Уровень | Характеристика | Следующий bottleneck |
|---|---|---|
| 0. Ad hoc | Prompt и ручной результат | Контракт и воспроизводимость |
| 1. Repeatable | Skill/workflow, version control | Evals и ownership |
| 2. Controlled | Risk tiers, gates, independent verification | Runtime reliability |
| 3. Operated | SLO, traces, budgets, incidents | Portfolio and learning |
| 4. Adaptive | Canary, reconciliation, evidence-driven improvement | Governance of adaptation |
| 5. Federated | Paved road + domain ownership + lifecycle | Continuous simplification |

Зрелость не означает больше агентов. Высшая зрелость часто удаляет лишние
agents, заменяет устойчивые шаги кодом и сокращает количество маршрутов.

## Финальный review checklist

- Какой pattern решает какую force и чем измерен?
- Кто владеет intent, state, side effects, verification и residual risk?
- Где проходят trust, security и write boundaries?
- Как обрабатываются duplicate, timeout, partial failure и cancellation?
- Какой цикл работает на runtime, delivery, operations и governance уровнях?
- Когда внутренний цикл эскалирует наружу?
- Какие роли должны быть независимы для этого risk tier?
- Как воспроизвести run по versions, events и artifacts?
- Как capability обновляется, откатывается, устаревает и выводится из работы?
- Можно ли получить тот же outcome более простой архитектурой?
