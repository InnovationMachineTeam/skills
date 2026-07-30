# Мастер-промпт навыка `agent-architect`

Применяй после [agent-skill-base.md](agent-skill-base.md). Создай skill, который
классифицирует потребность, выбирает минимальный agent pattern и создаёт
reviewable immutable agent-system candidate. Он не активирует runtime agent и не
выдаёт release verdict.

## Architecture routes

Классифицируй target как один primary route:

- single bounded agent;
- tool-using or retrieval-grounded agent;
- planner–executor;
- subagent/delegation topology;
- orchestrator/workflow;
- agent team;
- agent-oriented workflow/service;
- Agent OS component или platform architecture;
- redesign existing agent definition.

Если code, model call или deterministic workflow достаточны, верни более простое
решение. Не создавай отдельного agent только для persona, красивого имени или
одной роли без отдельного state/tools/permissions boundary.

## Pattern selection

Оцени uncertainty, coupling, parallelism, duration, side effects, reversibility,
independence, scale и cross-boundary protocols. Выбери patterns и явно запиши
forces/consequences:

- ReAct или plan–execute;
- router, manager-as-tools или handoff;
- pipeline, state machine, DAG или dynamic orchestrator;
- fork–join, blackboard, competing hypotheses;
- evaluator–optimizer, independent verifier, human checkpoint;
- saga, idempotency, lease, circuit breaker, bulkhead, reconciliation;
- shadow/canary и policy PDP/PEP.

Не используй pattern catalogue как checklist.

## Agent contract

Создай применимые artifacts:

- agent card и accountable ownership;
- mission, non-goals, user/stakeholder map;
- input/output/tool/handoff schemas;
- task envelope и context capsule;
- model/tool selection и fallback ladder;
- permissions, identities, data/network/secret policy;
- state/memory ownership, provenance, TTL и deletion;
- runtime cycle, budgets, stop и escalation;
- human-in/on/over-the-loop model;
- failure model, retries, compensation и recovery;
- telemetry/SLO/runbook requirements;
- evaluation contract и release thresholds;
- version, compatibility, migration и retirement.

Для team добавь mission charter, lead, write-sets, shared artifacts,
communication schema, task/lease ownership, merge/integration owner и conflict
resolution. Для Agent OS раздели control, execution, knowledge, assurance и
operations planes.

## Decision records

Зафиксируй alternatives, decision drivers, chosen pattern, rejected options,
risks, consequences и confirmation evidence. Не превращай сгенерированный plan
в authority: runtime/policy валидирует capabilities и side effects.

## Evaluation design

Перед завершением candidate задай claims и cases для:

- mission/outcome;
- routing и scope exclusions;
- tool success/denial/failure;
- delegation, partial failure и conflicting result;
- loop termination и budgets;
- memory/state resume and poisoning;
- human approval и unavailable approver;
- adversarial inputs;
- observability/recovery;
- compatibility, rollout и retirement.

## Output and handoff

Верни versioned candidate bundle, diagrams только где они проясняют boundaries,
decision record, threat model, eval plan и unresolved risks. Передай candidate
в `agent-evaluator`. Не исправляй результаты оценки внутри того же revision.
