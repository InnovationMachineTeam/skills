# Перенос metaskill-паттернов на работу с агентами

Дата анализа: **2026-07-30**.

## Краткий вывод

Подход из `skills/metaskills/` применим к агентам на двух уровнях:

1. **Как архитектура навыков для работы с агентами** — `agent-architect`,
   `agent-evaluator`, `agent-doctor`, `agent-manager` и другие skills используют
   тонкий router, route-specific prompts, references, scripts и evals.
2. **Как operating model самих агентов** — bounded handoffs, immutable
   candidates, independent evaluation, lifecycle states, donor locks,
   checkpoints и authority gates переносятся в Agent OS.

Буквально копировать portfolio нельзя. Skill — загружаемый capability package;
agent — runtime actor с identity, tools, state, memory, budgets, delegation и
side effects. Поэтому agent-oriented skills должны проверять не только
структуру/trigger, но также execution traces, permissions, recovery, SLO,
human oversight и decommissioning.

Рекомендуемый результат — отдельный portfolio навыков для управления агентами,
создаваемый по мастер-промптам из [prompts/README.md](prompts/README.md). Не
следует добавлять `agent` как девятый первичный архетип `skill-architect`: это
домен применения навыка, а не его механизм. Вместо этого нужен agent-system
profile, накладываемый на существующие archetypes workflow, evaluation,
orchestration, tool integration и meta/router.

## Что представляет собой текущая система metaskills

В portfolio 12 metaskills и один связанный prompt skill:

- lifecycle specialists: `skill-scout`, `skill-harvester`, `skill-architect`,
  `skill-evaluator`, `skill-doctor`, `skill-optimizer`, `skill-refactor`,
  `skill-manager`;
- orchestrators/control: `skill-builder`, `metaskillpack`;
- supporting systems: `skill-best-practices`, `skill-marketplace-manager`;
- prompt engineering: `prompt-optimize` из категории `prompt-skills`.

### Повторяющаяся структура

```text
skill-name/
├── SKILL.md                 # тонкий контракт, routing и invariants
├── agents/openai.yaml       # host-facing metadata
├── prompts/                 # base + route-specific master prompts
├── references/              # подробные правила и schemas
├── scripts/                 # deterministic inventory/validation/comparison
├── evals/                   # routing, behavior, scripts, security
└── README.md                # только где полезна документация пакета
```

Не каждый навык содержит все папки. Ресурс добавляется, только если снижает
повторное рассуждение, даёт детерминированность или нужен как artifact.

### Системные паттерны

| Паттерн metaskills | Реализация | Почему полезен |
|---|---|---|
| Thin router | `SKILL.md` выбирает один route | Не загружает весь portfolio в контекст |
| Base + specialization | Общий prompt и один route prompt | Общие invariants без копирования |
| Classification before creation | Архетип/сценарий выбирается по outcome | Структура следует hardest constraint |
| Specialist boundaries | Evaluator не чинит, doctor не оптимизирует | Сохраняет независимость evidence |
| Bounded handoff | Target, objective, scope, authority, output | Не даёт downstream расширять задачу |
| Immutable candidate | Изменение получает новую revision | Baseline и regression воспроизводимы |
| Layered evidence | Structure, routing, behavior, safety, E2E | Static PASS не выдаётся за качество |
| Preview before mutation | Inventory/diff/plan до write/install | Ограничивает blast radius |
| Durable state | Phase ledger и resumable checkpoints | Поддерживает долгие workflows |
| Lifecycle states | Draft → active → deprecated → retired | Есть migration и retirement |
| Donor lock | Version + tree hash + snapshot | Composite можно воспроизвести и обновить |
| Explicit composite | `metaskillpack` включается явно | Не конкурирует со specialist triggers |

Эти паттерны согласуются с каталогами
[агентной оркестрации](../skills/agent-skills/agent-best-practices/best-practices/17-agent-and-orchestration-pattern-catalog.md),
[Agent OS](../skills/agent-skills/agent-best-practices/best-practices/18-agent-os-and-runtime-pattern-catalog.md)
и [skill design](../skills/agent-skills/agent-best-practices/best-practices/19-skill-design-pattern-catalog.md).

## Что переносится на agents напрямую

### Worth и duplication gate

До создания агента нужно решить, нужен ли автономный actor. Возможные решения:

- `USE_CODE_OR_WORKFLOW` — задача детерминирована;
- `USE_EXISTING_AGENT` — capability уже покрыта;
- `EXTEND_EXISTING_AGENT` — граница существующего агента остаётся coherent;
- `CREATE_NEW_AGENT` — нужны отдельные mission, tools, context или permissions;
- `KEEP_HUMAN` — решение требует непропорционального human judgment;
- `RESEARCH` — evidence недостаточно.

Это agent-аналог `skill-scout`, но лестница сложности должна начинаться с code,
одного model call и workflow, а не сразу с нового агента.

### Architect → evaluator → doctor/optimizer → manager

Последовательность переносится почти полностью:

```text
need/context
  → agent architect creates immutable candidate contract
  → agent evaluator produces independent layered evidence
  → doctor repairs reproduced defects
  → optimizer changes a healthy candidate against a metric
  → evaluator compares revisions
  → manager publishes/activates/canaries/retires
```

После каждого изменения создаётся новая candidate revision; release authority
не принадлежит author, evaluator или runtime agent.

### Builder as lifecycle orchestrator

`skill-builder` — наиболее полезный образец для `agent-builder`:

- выбирает один primary scenario по observable outcome;
- предлагает минимальную specialist chain;
- сохраняет phase ledger и bounded handoffs;
- не имитирует работу specialists;
- останавливается на mutation/approval gates;
- проверяет evidence и фактический target-host state.

Для agents необходимо добавить shadow/canary, SLO, credentials, kill switch,
incident readiness и observation window.

### Composite toolkit

`metaskillpack` показывает безопасный способ собрать specialists под одной
явной командой: root router остаётся тонким, donors read-only, версии и hashes
зафиксированы, upgrade строит staged candidate. Для agent portfolio подход можно
реализовать позже как `agentkit`, но только после появления стабильных
independent donor skills. Ранний monolithic `agentpack` закрепит плохие границы.

## Что требует адаптации

| Skill-specific предположение | Agent-specific замена |
|---|---|
| Trigger/description определяет discovery | Route + identity + capability registry + policy |
| Bundle files — основное состояние | Definition immutable; runtime state отдельно |
| Host validation | Simulation, trace, sandbox и production-like verification |
| Install/enable | Register → approve → shadow → canary → activate |
| Script permissions | Agent/tool/IAM permission envelope и credential lifetime |
| Routing eval | Routing + delegation + handoff + fallback evals |
| Behavior case | Multi-step outcome, variance, budget и recovery case |
| Skill conflict | Capability overlap, write-set, shared state и authority conflict |
| Version update | Definition/model/tool/policy/memory compatibility migration |
| Retirement files | Revoke routes/credentials, drain runs, migrate memory, archive evidence |

### Новые обязательные agent artifacts

Agent-oriented skill должен уметь работать хотя бы со следующими контрактами:

- agent card: identity, owner, mission, users, non-goals, risk tier;
- input/output and handoff schemas;
- tools, permissions, data classes, network and secret policy;
- state/memory model, provenance, retention и deletion;
- runtime loop, budgets, stop, escalation и human oversight;
- deployment topology, model/runtime compatibility;
- eval plan, traces, baselines и release thresholds;
- SLO, telemetry, runbook, incident/rollback/kill-switch;
- lifecycle state, dependencies, replacement и retirement plan.

## Рекомендуемый portfolio навыков для agents

### Первая очередь

| Навык | Primary archetype | Ответственность |
|---|---|---|
| `agent-architect` | Workflow + evaluation profile | Контракт, паттерн, boundary, risk и candidate definition |
| `agent-evaluator` | Evaluation/review | Offline, simulation, delegation, safety, resilience и release evidence |
| `agent-doctor` | Diagnostic workflow | Symptom → trace → root cause → minimal repair → recovery proof |
| `agent-manager` | Tool/workflow integration | Inventory, registry, versions, rollout, state и retirement |
| `agent-builder` | Orchestration/composition | End-to-end scenarios и bounded specialist handoffs |

### Вторая очередь

| Навык | Когда оправдан |
|---|---|
| `agent-scout` | Появился portfolio и нужен системный worth/duplication gate |
| `agent-context` | Agent design регулярно требует repository/domain/trace research |
| `agent-optimizer` | Есть здоровые agents, baselines и измеримые cost/latency/quality targets |
| `agent-refactor` | Появились merge/split/extract/topology migrations |
| `agent-best-practices` | Нужен обновляемый evidence corpus отдельно от статичных docs |

### Третья очередь

- `agentkit` — explicit composite из version-locked donors;
- `agent-registry-manager` — только если registry/platform отделился от общего
  `agent-manager`;
- `agent-os-manager` — только при реальном multi-tenant runtime и SRE ownership;
- platform adapters для Codex, Claude Code, Cursor, MCP/A2A — после появления
  канонического platform-neutral contract.

### Что не стоит делать отдельным навыком сразу

- `subagent-creator`: subagent — deployment/coordination role, а не отдельный
  lifecycle product;
- `agent-team-creator`: отдельный creator не нужен; team topology принадлежит
  существующему `agent-team-architect`, а lifecycle — `agent-team-manager`;
- отдельный навык на каждый pattern: patterns — decision options, не products;
- один `agent-supervisor`, который проектирует, запускает, оценивает и одобряет.

## Архитектура мастер-промптов

Все prompts используют композицию:

```text
agent-skill-base.md + exactly one specialist master prompt
```

Base задаёт skill-creation contract, authority, agent asset model, resources,
evals и completion gates. Specialist prompt задаёт domain-specific routes,
artifacts, failure model и anti-patterns. Нельзя склеивать все prompts: это
создаст mega-skill и разрушит trigger precision.

Карта prompts находится в [prompts/README.md](prompts/README.md).

## Предлагаемые изменения существующих metaskills

### `skill-architect`

Не добавлять `agent` как новый primary archetype. Добавить optional reference
`agent-system-profile.md`, который применяется, когда продуктом создаваемого
skill является проектирование или управление agents. Profile должен добавить
agent card, state/memory, tools/permissions, runtime cycle, observability,
deployment и retirement checks.

### `skill-evaluator`

Добавить agent-control evaluation profile:

- delegation/task-envelope и context isolation;
- partial failure, retry, timeout, cancellation и stale result;
- tool authority, prompt injection и credential boundaries;
- memory poisoning, provenance и retention;
- budget/latency/cost, loop depth и fallback;
- shadow/canary, SLO и recovery;
- team-level correlated error и independent-verifier tests.

Это профиль оценки skill, работающего с agents; сам `skill-evaluator` не должен
становиться evaluator runtime agents.

### `skill-builder`

Добавить scenario `create-agent-lifecycle-skill`: base prompt + выбранный
agent-specialist prompt → `skill-architect` → `skill-evaluator`. Scenario создаёт
skill для работы с agents, а не разворачивает сам agent без отдельного запроса.

### `skill-scout`

Расширить decision taxonomy для agent opportunities: `USE_CODE_OR_WORKFLOW`,
`USE_EXISTING_AGENT`, `EXTEND_EXISTING_AGENT`, `CREATE_AGENT_SKILL` и
`KEEP_HUMAN`. Проверять, не предлагается ли agent там, где достаточно script
или существующего workflow.

### `skill-harvester`

Добавить harvest units: agent definitions/cards, AGENTS.md, tool schemas,
handoff contracts, traces, eval datasets, runbooks, policies, incident reports
и registry manifests. Secrets, hidden reasoning и production memory не должны
попадать в inbox.

### `skill-manager`

Не расширять его до управления runtime agents: это нарушит capability boundary
и permissions. Он может управлять public и agent-private agent-oriented skills,
их visibility, registry parity и lifecycle, но не runtime agent instances.
Runtime agents должен обслуживать отдельный `agent-manager`.

### `skill-best-practices`

Добавить текущий `agent-best-practices` corpus как declared derived/local
source либо оставить отдельным managed corpus. Предпочтителен отдельный corpus,
поскольку update cadence и normative scope для skill format и Agent OS различны.

### Routing/coexistence

Добавить negative-trigger fixtures, различающие:

- «оптимизируй skill, который создаёт agents» → `skill-optimizer`;
- «оптимизируй runtime agent» → будущий `agent-optimizer`;
- «создай skill для оценки agents» → `skill-architect` с agent evaluator prompt;
- «оцени этот skill» → `skill-evaluator`;
- «оцени этого агента» → будущий `agent-evaluator`;
- «установи agent-oriented skill» → `skill-manager`;
- «активируй agent definition» → `agent-manager` с отдельным approval.

## Public/private capability optimization

Идея хранить single-agent skills и commands внутри agent directory
целесообразна как **scope-minimization pattern**. Она уменьшает global routing
surface, collision risk и число independently published packages. При этом
folder nesting не является security boundary: `private` означает scoped loader
и allowed consumers, а не confidentiality.

Visibility не следует добавлять как primary archetype. После выбора mechanism
используется placement profile:

1. inline rule для tiny instruction;
2. private command для narrow named action одного agent;
3. private skill для reusable complex capability одного agent;
4. public skill для нескольких independent consumers или independent lifecycle;
5. tool/script либо workflow, если skill abstraction не является минимальной.

Все skills регистрируются. Private entry содержит owner agent, allowed
consumers, canonical locator и `agent_scoped` discoverability. Agent definition
получает binding из canonical map; global loader не сканирует
`.agents/definitions/*/skills`. Promotion/demotion выполняет `skill-refactor`
как versioned consumer migration с evals и rollback.

Новые исполняемые prompts находятся в `docs/prompts/`:

- `agent-capability-placement.md`;
- `agent-private-skill.md`;
- `agent-private-command.md`;
- `agent-skill-visibility-migration.md`.

## Recommended rollout

1. Review этого анализа и prompt taxonomy.
2. Создать `agent-architect` по соответствующему prompt.
3. Создать независимый `agent-evaluator` и frozen eval dataset.
4. Создать `agent-manager` только после выбора registry/runtime contracts.
5. Добавить `agent-doctor`; затем `agent-optimizer` при наличии baselines.
6. Собрать `agent-builder` после стабилизации specialist handoffs.
7. Провести routing collision tests со всеми `skill-*` навыками.
8. Только после двух стабильных release cycles рассмотреть `agentkit`.

## Критерий успеха

Подход считается перенесённым успешно, если новый agent-oriented skill:

- имеет одну coherent capability и точный trigger;
- использует общий base и один specialist prompt;
- создаёт/изменяет immutable agent candidate, а не active runtime напрямую;
- отделяет author, evaluator, approver и operator;
- выдаёт typed artifacts и reproducible evidence;
- проходит negative routing, authority, failure и lifecycle evals;
- поддерживает rollback, deprecation и retirement;
- не дублирует существующий metaskill и не превращает skill в неявного
  автономного агента.

## Продолжение

Единый phased plan для project-local agent teams, registries, skill mapping,
model selection, docs/memory и Agent OS находится в
[AGENT-TEAM-AND-AGENT-OS-PLAN.md](AGENT-TEAM-AND-AGENT-OS-PLAN.md).
