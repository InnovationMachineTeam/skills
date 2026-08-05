# Master Prompt For The `agent-team-architect` Skill

Apply after [agent-skill-base.md](agent-skill-base.md). Create a skill that
designs the minimal agent team from a proven task/capability graph. It creates
the specification and ADR, but not scaffolding, runtime activation, or
credential assignment.

## Intake and worth gate

Require outcome, repository/docs/data scope, constraints, risk, target hosts,
human roles, and acceptance criteria. First prove that a single agent, workflow,
or deterministic code is insufficient. Do not create a separate role for a
persona alone: the role needs separate context, tools/permissions, state, model
profile, write-set, independent evaluation, or accountability boundary.

## Design procedure

1. Build the task graph, artifact graph, uncertainty, and failure model.
2. Extract roles: lead/orchestrator, bounded specialists, integration owner,
   verifier, security/reliability reviewer, knowledge curator, and operator,
   only if their boundary is proven.
3. For each role, record mission, non-goals, inputs/outputs, tools,
   permissions, model policy, budgets, stop/escalation, and lifecycle owner.
4. Choose the topology: sequential, pipeline, fork-join, DAG, manager-as-tools,
   handoff, blackboard, or competing hypotheses. Justify forces/consequences.
5. Define shared artifacts, single writers, leases, write-sets, merge owner,
   conflict resolution, cancellation, and partial-failure recovery.
6. Pass each capability through the placement gate: inline, private command,
   private skill, public skill, tool/script, or workflow.
7. Design public/private bindings, the registry/map transaction, and host
   adapters. A private capability belongs to exactly one agent.
8. Choose worktree policy only for truly independent code write-sets.
9. Create the threat model, eval matrix, rollout/rollback, and retirement plan.

## Output

Return the versioned `agent-team-spec`, role cards, interaction/handoff
schemas, model recommendations with fallbacks, workflow/worktree decision,
capability placement ledger, registry candidate diff, ADR, eval plan, and
residual risks. Hand the approved spec to `agent-team-builder`; do not create
`.agents` directly.
