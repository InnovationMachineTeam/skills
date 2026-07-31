---
name: agent-team-manager
description: >-
  Governs the lifecycle of registered agent teams by assessing requests,
  selecting the next safe specialist workflow, maintaining durable run state
  and checkpoints, coordinating authorized operation, change, recovery or
  retirement, and verifying completion. Use when a user wants one entry point
  to design, build, map capabilities, launch, monitor, change, recover or retire
  an agent team. This is a thin lifecycle facade that delegates architecture,
  model selection, building and skill mapping to their owning skills and does
  not reimplement them, infer destructive authority, create worktrees or
  publish assets.
metadata:
  version: "1.2.0"
---

# Govern Agent-Team Lifecycles

Act as a stateful control plane, not a super-agent. Select the smallest complete
workflow, preserve specialist boundaries and make authority visible at every
side effect.

## Verify companion skills

Read [skill-dependencies.md](references/skill-dependencies.md) before routing.
Check that the companion owning the selected route is available at its minimum
version. Emit the specified dependency warning and block only that route when a
required companion is unavailable. Never imitate a missing specialist.

## Assess and route

Read [references/scenario-catalog.md](references/scenario-catalog.md). Resolve
the requested outcome, team/spec/run identifiers, current lifecycle state,
repository/docs/data scope, risk, target host, approvals and completion evidence.
If context is insufficient for a material choice, pause for the minimum blocking
question.

Choose one primary route:

- `assess`: determine whether a team or simpler mechanism is justified;
- `design`: delegate the team spec to `agent-team-architect` and exact current
  model evidence to `agent-model-selector`;
- `build`: delegate an approved spec to `agent-team-builder`;
- `map-capabilities`: delegate governed bindings to `agent-skill-mapper`;
- `operate`: delegate an approved run plan to `agent-team-orchestrator` and
  isolated code workspaces to `agent-workspace-manager` when justified;
- `change`: impact-analyze and version a controlled modification;
- `recover`: contain, diagnose, roll back or resume a failed run;
- `retire`: deactivate, preserve evidence and retire assets safely.

Present alternative workflows before a material multi-stage run when trade-offs
differ. Never hide a required human checkpoint behind routing.

## Maintain durable state

Read [references/lifecycle-and-state.md](references/lifecycle-and-state.md).
Create or update a run record with team/spec versions, current phase, status,
authority, selected workflow, specialist handoffs, checkpoints, artifact refs,
expected revisions, budgets, risks, timestamps, next action and rollback.

Validate a run record whenever it is created or resumed:

```bash
python3 scripts/validate_run_state.py agent-team-run.json
```

Re-read external state before mutation. A stale revision or changed authority
returns to assessment. Registration, approval, installation and activation are
separate states.

## Coordinate execution

Use typed handoffs with objective, inputs, constraints, authority, deliverables,
validation, return status and unresolved risks. Parallelize only independent
work with bounded write-sets. `agent-team-orchestrator` owns task dispatch and
run evidence; `agent-workspace-manager` owns any explicitly authorized worktree
ledger, allocation, integration handoff and cleanup. This facade owns neither.

Apply observe-orient-decide-act with bounded retries. Track heartbeats, leases,
budget, blocked dependencies, integration ownership and cancellation. Stop on
permission drift, unsafe partial failure, lost ownership, exhausted budget or a
human checkpoint.

## Verify and close

Completion requires artifact and evaluation evidence, not a specialist saying
"done". Reconcile registry/map/run state, record residual risks and next owner,
and choose `COMPLETED`, `PARTIAL`, `BLOCKED`, `FAILED`, `ROLLED_BACK` or
`RETIRED`. Preserve a resumable checkpoint for every non-terminal outcome.

Report route and rationale, state transitions, delegated specialists and exact
versions, authority consumed, artifacts/evidence, remaining risks and next safe
action.
