# Orchestration and Agent Teams

## Choosing the Control Plane

| Control plane | Strength | Primary risk |
|---|---|---|
| Code / state machine | Predictability, testability, budget control | Weak adaptation to novelty |
| LLM orchestrator | Dynamic decomposition and routing | Unpredictability and drift |
| Hybrid | Code holds the gates, LLM decides locally | Interfaces are more complex |

Use hybrid by default: the program owns lifecycle, permissions, budgets, and
durable state; the model owns classification, planning, and selection within a
limited action set. The OpenAI Agents SDK explicitly separates LLM and code
orchestration, and Google ADK offers deterministic sequential, parallel, and
loop workflows ([OpenAI](https://openai.github.io/openai-agents-python/multi_agent/),
[Google ADK](https://adk.dev/agents/workflow-agents/)).

## Core Topologies

### Router

Classifies the request and passes it to one specialist. Good for
non-overlapping domains. Routing output MUST be typed and include confidence and
fallback.

### Manager / agents as tools

The manager remains the owner of the dialog, invokes specialists, and
synthesizes the result. Choose this when you need a unified policy, response
tone, or final accountability.

### Handoff network

A specialist gains control and can pass it on further. Suitable for service
triage, but requires protection against ping-pong, a maximum number of
transfers, and route history.

### Orchestrator-workers

The orchestrator dynamically builds subtasks, workers execute them, and then the
result is assembled and verified. Best suited to complex work where the number
and type of parts are unknown in advance.

### Pipeline

Sequential narrow agents: research -> plan -> implement -> verify. Useful when
the output of each step is the contractual input of the next.

### Fan-out / fan-in

Independent specialists work in parallel, and an aggregator normalizes and
resolves conflicts. Use this for multiple sources, review dimensions, or
competing hypotheses.

### Evaluator-optimizer

The producer improves the artifact based on evaluator feedback until pass or
budget limit. Criteria and limits must be defined before launch.

### Debate / jury

Several independent candidates and a judge. Use where diversity is justified by
evals. Participants must not see each other's answers before the first
evaluation, or the independence is fake.

## Agent Team

A team is not needed for every kind of parallelism. Unlike subagents, peers can
coordinate directly and share a task board. This is useful for:

- parallel research with exchange of discoveries;
- splitting frontend/backend/infra with clear interfaces;
- validating competing debugging hypotheses;
- adversarial review where critics challenge one another's plans;
- long-running work where a lead reallocates tasks.

Do not use a team for a strict sequence, a short task, heavy file overlap, or
when one context must make all decisions.

Claude recommends starting with 3-5 teammates and several clear tasks for each,
but that is a platform heuristic, not a universal norm
([agent teams](https://code.claude.com/docs/en/agent-teams)). Start with 2-3
executors and scale after measuring the bottleneck.

## Team Charter

Before launch, the team receives:

```yaml
mission: Prove checkout readiness for release
lead: release-orchestrator
members:
  - id: qa
    owns: [tests/e2e/**]
  - id: security
    mode: read_only
  - id: reliability
    owns: [docs/runbooks/checkout.md]
shared_artifacts:
  task_board: .agent/tasks.json
  decisions: docs/decisions/
communication:
  message_schema: agent-message-v1
  max_rounds: 4
merge_owner: lead
exit:
  - all blocking tasks terminal
  - release gate evaluated
```

It MUST define the lead, owners, canonical state, message protocol, write-set,
merge owner, and stop conditions.

## Task Graph and Scheduler

Each task has:

- a stable ID;
- parent goal and acceptance criteria;
- dependencies;
- owner and lease;
- risk class and approvals;
- input/output references;
- status and timestamps;
- attempt, budget, and heartbeat;
- evidence and terminal reason.

The scheduler MUST prevent double ownership, validate leases, and must not treat
a task as complete based on one agent message alone. State transitions must be
machine-readable and idempotent.

## Workflow-as-code

When a scenario repeats or contains dozens of steps, move the plan from the
prompt into version-controlled code. Claude Code workflows emphasize that code
holds the plan and intermediate state, while only the final result returns to
the main context ([workflows](https://code.claude.com/docs/en/workflows)).

Workflow SHOULD have:

- dry-run and plan visualization;
- deterministic gates and typed payloads;
- checkpoints/resume;
- retry and compensation policy;
- unit tests for routing and transitions;
- trace correlation;
- cancellation support;
- explicit human-in-the-loop;
- a limited set of allowed agents/tools.

Before executing a generated workflow, a human must see its raw plan, especially
side effects and network usage.

## Conflict Resolution

The aggregator must not "average out" incompatible results. It:

1. normalizes claims and evidence;
2. distinguishes factual conflict from preference differences;
3. checks authoritative sources and freshness;
4. requests additional proof;
5. applies predefined policy;
6. hands high-impact ambiguity to a human.

The decision is recorded as an ADR/decision record with rejected alternatives.

## Distributed-systems Reality

A multi-agent system inherits distributed-systems problems: duplicate delivery,
message loss, split brain, stale reads, network partition, cascading retries,
and orphan jobs. Microsoft recommends accounting for these modes before choosing
a multi-agent pattern
([Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)).

Apply correlation IDs, idempotency keys, leases, heartbeats, a durable queue,
dead-letter state, backpressure, circuit breakers, and reconciliation jobs.
