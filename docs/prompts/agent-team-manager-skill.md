# Мастер-промпт навыка `agent-team-manager`

Применяй после [agent-skill-base.md](agent-skill-base.md). Создай lifecycle
facade, который анализирует задачу, код, документы и данные, выбирает нужный
team workflow и координирует specialist skills. Он не переimplementирует scout,
harvester, architect, builder, mapper, evaluator или orchestrator.

## Routes

- `assess`: task/code/docs → need/no-need decision;
- `design`: agent-scout + skill-scout/harvester → team-architect;
- `build`: approved spec → team-builder → evaluator;
- `map-capabilities`: inventory/locks → agent-skill-mapper;
- `operate`: approved active team → team-orchestrator;
- `change`: inventory → architect/refactor → builder/evaluator;
- `retire`: consumer inventory → migration → manager lifecycle gate;
- `recover`: doctor/observer evidence → bounded repair and re-evaluation.

## Invariants

Require exact scope, authority and lifecycle state. Generate role, interaction
and Agentic OS prompts only from evidence. Register agents, public/private
skills and commands through one asset/map transaction. Never scan arbitrary
private content without authority, activate candidates, create worktrees,
publish skills or broaden permissions by inference. Keep human accountable
owner distinct from technical owner agent.

## Durable state and completion

Maintain scenario, phase DAG, artifact hashes, approvals, budgets, checkpoints,
active operations and rollback. Inspect specialist artifacts rather than their
completion messages. Completion requires registry/map parity, host projection,
independent evaluation and observed target state. Report exact handoffs and
stopped/blocked phases without converting them into success.
