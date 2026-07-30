# Мастер-промпт навыка `agent-team-architect`

Применяй после [agent-skill-base.md](agent-skill-base.md). Создай skill, который
проектирует минимальную команду агентов из доказанного task/capability graph.
Он создаёт specification и ADR, но не scaffolding, runtime activation или
назначение credentials.

## Intake и worth gate

Требуй outcome, repository/docs/data scope, constraints, risk, target hosts,
human roles и acceptance criteria. Сначала докажи, что single agent, workflow
или deterministic code недостаточны. Не создавай отдельную роль ради persona:
роль нуждается в отдельном context, tools/permissions, state, model profile,
write-set, independent evaluation или accountability boundary.

## Design procedure

1. Построй task graph, artifact graph, uncertainty и failure model.
2. Выдели роли: lead/orchestrator, bounded specialists, integration owner,
   verifier, security/reliability reviewer, knowledge curator и operator —
   только если их boundary доказан.
3. Для каждой роли зафиксируй mission, non-goals, inputs/outputs, tools,
   permissions, model policy, budgets, stop/escalation и lifecycle owner.
4. Выбери topology: sequential, pipeline, fork–join, DAG, manager-as-tools,
   handoff, blackboard или competing hypotheses. Обоснуй forces/consequences.
5. Определи shared artifacts, single writers, leases, write-sets, merge owner,
   conflict resolution, cancellation и partial-failure recovery.
6. Пропусти каждую capability через placement gate: inline, private command,
   private skill, public skill, tool/script или workflow.
7. Спроектируй public/private bindings, registry/map transaction и host
   adapters. Private capability принадлежит ровно одному agent.
8. Выбери worktree policy только для действительно независимых code write-sets.
9. Создай threat model, eval matrix, rollout/rollback и retirement plan.

## Output

Верни versioned `agent-team-spec`, role cards, interaction/handoff schemas,
model recommendations with fallbacks, workflow/worktree decision, capability
placement ledger, registry candidate diff, ADR, eval plan и residual risks.
Передай approved spec в `agent-team-builder`; не создавай `.agents` сам.
