# Task Tracking, Monitoring, and Observability

## Canonical task model

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

Status must reflect scheduler fact, not the agent's text. `waiting` means
waiting for an external event; `blocked` means a precondition is demonstrably
unmet; `completed` means acceptance is confirmed by evidence.

## State transitions

```text
queued → ready → running ─┬→ completed
                         ├→ waiting → running
                         ├→ blocked → ready
                         ├→ failed → ready (retry)
                         └→ cancelled
```

Each transition is an idempotent event with actor, timestamp, reason, and
version. Optimistic concurrency or compare-and-swap prevents lost updates.

## Leases, heartbeat, and orphan detection

- the owner receives a lease for the task/write-set;
- heartbeat extends the lease;
- a lost lease forbids further writes;
- an expired task moves to reconciliation, not immediately to another writer;
- the scheduler checks unfinished side effects and artifacts;
- redispatch uses an idempotency key.

GSD Pi applies fail-closed worktree/branch/lease safety. This is more important
than optimistic assumptions that "the agent still owns the task."

## Three levels of observability

### Run-level

- task success and terminal state;
- latency, turns, tool calls, tokens, cost;
- retries, loops, cancellations;
- human checkpoints and wait time;
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

The OpenAI Agents SDK natively traces runs, agents, generations, tools,
guardrails, and handoffs
([tracing](https://openai.github.io/openai-agents-python/tracing/)). Full
prompt/tool data is sensitive and should be opt-in/redacted.

### System-level

- queue depth and age;
- active/blocked/orphan tasks;
- throughput and saturation;
- error rate by capability/version;
- policy denials;
- approval backlog;
- eval regression;
- cost budget burn;
- stale memory/docs;
- security anomalies.

For the underlying service, apply latency, traffic, errors, and saturation from
Google SRE, but add agent-specific signals
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

### Quality and cost

- rubric scores;
- requirement/test coverage;
- tokens/cost per successful outcome;
- model/tool latency share;
- context cache hit;
- stale-context incidents.

Do not optimize a local metric at the expense of the outcome: a cheap run with
high rework is worse than an expensive successful run.

## Dashboard views

1. **Operator** — active, waiting, blocked, cancel/resume.
2. **Owner** — success, cost, eval regressions, versions.
3. **Security** — permissions, denials, anomalous tools, provenance.
4. **Product** — resolved bets, user outcomes, incidents.
5. **Developer** — traces, prompt/tool versions, failure clusters.

Each chart should lead to a specific run/task/evidence item.

## Alerts

Page only on an actionable symptom:

- critical side effect without required approval;
- repeated destructive failure;
- compromised credential/provenance signal;
- runaway loop or budget explosion;
- queue stall on a critical workflow;
- production SLO breach correlated with agent action.

Ticket, but do not page:

- gradual quality drift;
- rising cost;
- stale docs/memory;
- low specialist usefulness;
- non-critical orphan task.

## Audit log

Append-only audit contains who/what/when/why:

- human/agent identity;
- delegated authority chain;
- exact artifact/policy/tool digest;
- approval token and scope;
- external action and result;
- rollback/compensation;
- data access class.

Do not log secrets and raw sensitive content by default. Retention and access
must match the data classification.

## Runbooks

Required operational scenarios:

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
- emergency revoke and mass cancel.

A runbook is considered complete only after an exercise or test simulation.
