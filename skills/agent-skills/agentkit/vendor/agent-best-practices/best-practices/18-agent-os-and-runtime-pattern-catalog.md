# Паттерны Agent OS и runtime

## Agent OS как платформа управления

Agent OS — не «главный супер-агент», а platform layer, который делает выполнение
агентов воспроизводимым, управляемым и наблюдаемым. Он отделяет вероятностные
решения моделей от детерминированных control, security и state mechanisms.

Рекомендуемая декомпозиция:

```text
experience plane   — users, IDE, API, chat, approvals
control plane      — intent, registry, planning, routing, policy, scheduler
execution plane    — agents, tools, sandboxes, connectors, model gateways
knowledge plane    — context, memory, artifacts, provenance, retrieval
assurance plane    — evals, verification, security, audit, release gates
operations plane   — telemetry, budgets, incidents, reconciliation, lifecycle
```

Planes — логические границы. В малой установке они могут работать в одном
процессе, но их контракты и ответственность всё равно должны быть различимы.

## Control plane

### Capability registry

Реестр описывает agents, skills, tools, workflows, модели и adapters через
версионируемые manifests. Минимальные поля: identity, version, owner,
capabilities, trigger/input/output schemas, permissions, compatibility,
dependencies, risk tier, eval status, lifecycle state и provenance.

Discovery не означает authorization: найденный capability ещё должен пройти
policy, compatibility и health gates.

### Workflow registry

Повторяемые процессы хранятся отдельно от runtime state. Definition immutable
после публикации; run ссылается на точную версию. Обновление workflow не меняет
уже начатые runs без явной migration policy.

### Hybrid orchestrator

Код владеет состояниями, retries, budgets, permissions, approvals и durable
execution. Модель выполняет классификацию, локальное планирование и синтез в
ограниченном пространстве. Любой сгенерированный plan проходит schema,
capability, cycle, permission и cost validation.

### Desired-state reconciliation

Для установленных skills, workers, schedules и long-running tasks храните
desired и observed state. Reconciler исправляет drift идемпотентно и создаёт
audit event. Этот паттерн надёжнее разовой команды `upgrade`, потому что
обнаруживает частичные сбои и последующий drift.

## Execution plane

### Ports and adapters

Канонический внутренний контракт изолирует platform-specific Claude Code,
Codex, Cursor, MCP, A2A и vendor APIs. Adapter переводит manifests, tool calls,
approvals и events, не протаскивая platform assumptions в core workflow.

### Sandboxed worker

Каждый run получает identity, readonly context, отдельное working state,
разрешённые tools, network policy, secret grants, quotas и expiry. Credentials
выдаются just-in-time и не попадают в prompt, logs или durable artifacts.

### Execution lease

Worker получает lease на task и продлевает heartbeat. После expiry scheduler
может назначить задачу заново; поэтому side effects требуют idempotency key или
проверки observed state. Lease не является distributed lock для внешней системы.

### Outbox / inbox

Изменение локального state и запись намерения отправить событие фиксируются
атомарно; dispatcher доставляет событие повторяемо, consumer дедуплицирует по
ID. Это устраняет классическую потерю между «сохранил задачу» и «отправил
сообщение».

### Saga

Long-running workflow разбивается на локальные commits. Для каждого irreversible
или externally visible шага задаётся compensation либо честно фиксируется, что
шаг non-compensatable и требует более сильного approval до исполнения.

## Knowledge и state plane

### Event log + projections

Append-only события являются историей run; task board, dashboard и current state
строятся как projections. Это даёт replay и audit, но не требует применять full
event sourcing к каждому документу. Команды должны быть idempotent, события —
versioned и коррелированы с intent, actor и artifact versions.

### Immutable artifact + mutable pointer

Spec, plan, result, evaluation и release bundle сохраняются как content-addressed
или immutable versions; короткий pointer обозначает current approved version.
Это предотвращает незаметную подмену evidence и упрощает rollback.

### Provenance graph

Связи `derived_from`, `supersedes`, `implements`, `verified_by`, `released_as`
дают traceability от intent до production observation. Edge содержит actor,
timestamp, method и confidence. Summary без ссылок не добавляется как факт.

### Tiered memory

- run context — живёт один run;
- episodic memory — проверенные события и результаты;
- semantic memory — устойчивые факты с источником и TTL;
- procedural memory — versioned skills/workflows;
- policy memory — только authoritative controlled store.

Запись в долгую память проходит curation, provenance, sensitivity и expiry.

## Assurance plane

### Policy decision point / enforcement point

PDP возвращает `allow`, `deny` или `require_approval` вместе с policy version и
reason codes. PEP находится у реального action boundary и не полагается на
послушание prompt. Policy changes версионируются и тестируются на historical
decision cases.

### Evidence gate

Gate принимает не текст «готово», а typed bundle: версии inputs, executed
checks, raw results, coverage, exceptions, approvals и residual risks. Verdict
машиночитаем и имеет expiry, если evidence быстро устаревает.

### Shadow, canary и champion–challenger

Новая версия сначала работает без side effects на production-like inputs,
затем на ограниченной доле runs. Champion и challenger сравниваются по quality,
safety, latency и cost; promotion требует заранее заданного threshold. Нельзя
оптимизировать одну метрику ценой невидимого ухудшения остальных.

### Tamper-evident audit

Audit record содержит actor/agent identity, delegated authority, exact versions,
tool calls, approvals, side effects и evidence refs. Sensitive prompt content
редактируется по policy, но факт действия и decision metadata сохраняются.

## Operations plane

### MAPE-K controller

Runtime operations удобно строить как Monitor → Analyze → Plan → Execute над
общим Knowledge. Sensors собирают signals, effectors меняют managed element.
Классическая IBM-модель отдельно рассматривает управляемый элемент и autonomic
manager
([IBM MAPE-K](https://dominoweb.draco.res.ibm.com/reports/h-0219.pdf)).

### Bulkheads и budget governors

Отдельные quotas по tenant, workflow, agent, model и tool предотвращают
cascading exhaustion. Budget включает tokens, деньги, wall time, tool calls,
parallel workers и retries. Превышение переводит run в явное terminal или
human-input state, а не в бесконечное ухудшение качества.

### Circuit breaker и fallback ladder

Breaker открывается по ошибкам/latency конкретной dependency; fallback идёт по
заранее утверждённой лестнице: retry → alternative model/tool → degraded
read-only mode → human queue → stop. Fallback MUST сохранять security и quality
floor; дешёвая модель не является допустимым fallback для любого решения.

### Reconciliation и orphan recovery

Периодический контроллер ищет expired leases, incomplete outbox, stale approval,
broken pointer, incompatible skill и незакрытый run. Recovery создаёт новое
событие и не переписывает историю. После максимума попыток задача попадает в
dead-letter state с actionable diagnostics.

## Interoperability

- **MCP** соединяет agent/runtime с tools, data и prompts; capability listing не
  заменяет authorization
  ([MCP specification](https://modelcontextprotocol.io/specification/latest)).
- **A2A** задаёт межагентное discovery, tasks, messages и artifacts между
  независимыми системами
  ([A2A specification](https://a2a-protocol.org/latest/specification/)).
- Внутренние calls используют typed contracts независимо от транспорта.
- Cross-boundary identity, policy, provenance и revocation обязательны.
- Negotiated capability и protocol version сохраняются в run record.

## Lifecycle states платформенных сущностей

Единая модель для agent, skill, workflow, tool adapter и policy:

```text
draft → candidate → verified → approved → published → active
                                ↓             ↓         ↓
                              rejected      suspended  deprecated → retired
```

`published` означает доступность в registry, `active` — разрешение на routing.
Deprecated entity остаётся читаемой и содержит replacement/migration deadline.
Retirement отзывает routes и credentials, архивирует evidence и проверяет, что
активные dependents отсутствуют или мигрированы.

## Reference runtime contract

```yaml
run:
  id: run_123
  intent_ref: artifact://intent/sha256:...
  workflow: feature-delivery@2.4.1
  policy: company-agent-policy@7
  identity: agent://orchestrator/release
  delegated_by: user://owner
  budgets:
    wall_time_s: 1800
    tool_calls: 80
    cost_usd: 12
  state: waiting_for_approval
  checkpoint_ref: event://run_123/42
  artifacts: []
  evidence: []
  approvals: []
```

## Agent OS anti-patterns

- один глобальный prompt одновременно хранит policy, state и память;
- registry без versions, owner, compatibility и revocation;
- «exactly once» предполагается без idempotency и reconciliation;
- observability сохраняет secrets или полный чувствительный контекст;
- worktree или prompt используется как security boundary;
- auto-upgrade меняет active behavior без eval, canary и rollback;
- human approval запрашивается без diff, evidence и описания side effect;
- long-running run нельзя отменить, продолжить или безопасно завершить;
- retired agent остаётся доступным через старый route или credential.
