---
name: agent-manager
description: Governs the lifecycle of one registered agent or subagent through inventory, candidate registration, approval, shadow, canary, activation, suspension, migration, rollback, deprecation and retirement with version, registry, documentation and runtime verification. Use when managing an individual agent definition or instance, reconciling its desired and observed state, planning a rollout, or retiring it safely. Do not design or evaluate agents, operate teams, administer an entire Agentic OS registry, infer activation authority, issue credentials, or equate file presence with active state.
metadata:
  version: "1.0.3"
---

# Manage One Agent Lifecycle

Treat definition, registration, approval, installation, activation and observed
runtime state as separate facts. Default to read-only inventory and plan.

## Verify companions and select a route

Read [references/skill-dependencies.md](references/skill-dependencies.md) when
present and block only an affected route whose required companion is missing.

Choose one route: `inventory`, `register-candidate`, `plan-rollout`, `shadow`,
`canary`, `activate`, `suspend`, `migrate`, `rollback`, `deprecate`, `retire` or
`reconcile`. Resolve exact agent/version/hash, owner, registry/map revisions,
host/runtime, approvals, consumers, active runs, credentials, documents,
evidence and rollback target.

Read [references/lifecycle-contract.md](references/lifecycle-contract.md).
Current design or model changes belong to `agent-architect`; frozen release
evidence belongs to `agent-evaluator`; defects belong to `agent-doctor`.

## Apply lifecycle gates

Before mutation, present exact desired transition, write/runtime targets,
authority, preconditions, validation and rollback. Re-read observed state and
use optimistic revisions. Never activate a candidate merely because files or a
registry entry exist.

Activation requires approved definition, evaluator evidence, compatible model
and tools, least-privilege policy, documentation inputs, runbook, telemetry,
budgets, kill switch and rollback. Use shadow before canary when risk warrants.

At Agentic OS scope, delegate registry transactions to
`agent-registry-manager` and runtime instances to `agent-runtime-manager`.

## Retire safely

Stop new routing, drain/cancel runs by policy, revoke credentials, migrate state
and memory, transfer or supersede documentation ownership, update consumers and
preserve evidence. Delete nothing merely because status became retired.

Return desired and observed states, transition evidence, versions/revisions,
authority consumed, documentation state, rollback and `NOOP`, `PLANNED`,
`APPLIED`, `BLOCKED`, `ROLLED_BACK` or `RETIRED`.
