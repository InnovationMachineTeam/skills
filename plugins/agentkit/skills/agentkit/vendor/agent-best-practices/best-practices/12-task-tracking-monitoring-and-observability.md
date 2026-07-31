# Трекинг задач, мониторинг и наблюдаемость

## Каноническая модель задачи

```yaml
id: TASK-1042
parent_goal: GOAL-88
type: research | plan | implement | verify | approval
status: queued | ready | running | waiting | blocked | completed | failed | cancelled
owner: agent-or-human-id
lease_expires_at: ...
attempt: 1
depends_on: [TASK-1041]
input_artifacts: [...]
output_contract: ...
write_set: [...]
risk: low | medium | high | critical
budget: {turns: 10, duration_s: 900, cost_usd: 3}
heartbeat_at: ...
evidence: [...]
terminal_reason: ...
```

Статус должен отражать факт scheduler, а не текст агента. `waiting` означает
ожидание внешнего события; `blocked` — доказанно невыполненное precondition;
`completed` — acceptance подтверждён evidence.

## Переходы состояния

```text
queued → ready → running ─┬→ completed
                         ├→ waiting → running
                         ├→ blocked → ready
                         ├→ failed → ready (retry)
                         └→ cancelled
```

Каждый переход — идемпотентное событие с actor, timestamp, reason и version.
Optimistic concurrency или compare-and-swap предотвращает потерю обновлений.

## Leases, heartbeat и orphan detection

- owner получает lease на задачу/write-set;
- heartbeat продлевает lease;
- потерянный lease запрещает дальнейшую запись;
- истёкшая задача переходит в reconciliation, не сразу к другому writer;
- scheduler проверяет незавершённые side effects и artifacts;
- повторный dispatch использует idempotency key.

GSD Pi применяет fail-closed worktree/branch/lease safety. Это важнее
optimistic предположения, что «агент всё ещё владеет задачей».

## Три уровня наблюдаемости

### Run-level

- task success и terminal state;
- latency, turns, tool calls, tokens, cost;
- retries, loops, cancellations;
- human checkpoints и wait time;
- agent/model/tool/policy versions.

### Step-level trace

- routing decision;
- model generation metadata;
- tool input/output metadata;
- handoff;
- guardrail/approval decision;
- artifact creation;
- state transition;
- error classification.

OpenAI Agents SDK встроенно трассирует runs, agents, generations, tools,
guardrails и handoffs
([tracing](https://openai.github.io/openai-agents-python/tracing/)). Полное
содержимое prompt/tool data чувствительно и должно быть opt-in/redacted.

### System-level

- queue depth и age;
- active/blocked/orphan tasks;
- throughput и saturation;
- error rate по capability/version;
- policy denials;
- approval backlog;
- eval regression;
- cost budget burn;
- stale memory/docs;
- security anomalies.

Для underlying service применяйте latency, traffic, errors и saturation из
Google SRE, но добавляйте agent-specific signals
([SRE](https://sre.google/sre-book/monitoring-distributed-systems/)).

## Agent-specific metrics

### Outcome

- end-to-end task success;
- verified goal achievement;
- human correction/rework rate;
- escaped defect/incident rate;
- bet resolution rate.

### Orchestration

- routing accuracy;
- delegation precision/recall;
- handoff completeness;
- duplicate work rate;
- merge conflict rate;
- critical path latency;
- parallel efficiency;
- loop/escalation rate.

### Tooling

- tool selection accuracy;
- invalid argument rate;
- tool error/retry rate;
- side-effect rollback rate;
- denied high-risk call rate;
- output truncation rate.

### Quality и cost

- rubric scores;
- requirement/test coverage;
- tokens/cost per successful outcome;
- model/tool latency share;
- context cache hit;
- stale-context incidents.

Не оптимизируйте локальную метрику ценой outcome: низкая стоимость run с высоким
rework хуже дорогого успешного run.

## Dashboard views

1. **Operator** — active, waiting, blocked, cancel/resume.
2. **Owner** — success, cost, eval regressions, versions.
3. **Security** — permissions, denials, anomalous tools, provenance.
4. **Product** — resolved bets, user outcomes, incidents.
5. **Developer** — traces, prompts/tools versions, failure clusters.

Каждый график должен вести к конкретному run/task/evidence.

## Alerts

Page только по actionable symptom:

- critical side effect без требуемого approval;
- repeated destructive failure;
- compromised credential/provenance signal;
- runaway loop или budget explosion;
- queue stall на critical workflow;
- production SLO breach с agent action correlation.

Ticket, но не page:

- gradual quality drift;
- растущая стоимость;
- stale docs/memory;
- низкая полезность specialist;
- non-critical orphan task.

## Audit log

Append-only audit содержит кто/что/когда/почему:

- human/agent identity;
- delegated authority chain;
- exact artifact/policy/tool digest;
- approval token и scope;
- внешнее действие и результат;
- rollback/compensation;
- data access class.

Не записывайте secrets и raw sensitive content по умолчанию. Retention и access
должны соответствовать data classification.

## Runbooks

Обязательные операционные сценарии:

- stuck run;
- orphan worker;
- duplicated side effect;
- failed handoff;
- corrupted/stale state;
- permission/approval outage;
- runaway cost;
- memory poisoning;
- compromised tool/agent version;
- trace export failure;
- emergency revoke и mass cancel.

Runbook считается готовым только после упражнения или test simulation.
