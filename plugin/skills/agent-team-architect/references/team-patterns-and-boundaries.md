# Team patterns and role boundaries

## Team worth gate

Use multiple agents when at least one force is material:

- independent work can reduce critical-path time;
- context or tools conflict and benefit from isolation;
- permissions or data access require separation;
- independent verification reduces consequential correlated failure;
- distinct state, owner, SLO or release cadence exists;
- competing hypotheses need blinded exploration.

Prefer one agent or a workflow when coordination, merge and context-transfer cost
outweighs these benefits.

## Role boundary evidence

A role must identify its separate mission plus at least one of: tool/permission
boundary, context corpus, model profile, state ownership, write-set, independent
verdict or accountable human owner. Do not duplicate planner, coordinator and
orchestrator titles when one state owner can perform them.

Common conditional roles:

- lead/orchestrator: task ownership, authority, budgets and integration;
- bounded specialist: one capability and output contract;
- independent verifier/evaluator: frozen gates and no mutation;
- integration owner: merge, end-to-end checks and release candidate;
- security/reliability reviewer: high-risk threat/failure evidence;
- knowledge curator: durable docs provenance and freshness;
- operator/incident owner: active SLO, recovery and retirement.

## Topologies

- sequential/pipeline: strong dependency and stable stage contracts;
- fork-join/DAG: independent branches with explicit fan-in;
- manager-as-tools: centralized authority and bounded specialists;
- handoff: context and ownership intentionally transfer;
- blackboard: multiple contributors share versioned artifacts with ownership;
- competing hypotheses: independent approaches evaluated after blind work.

Dynamic orchestration increases uncertainty and must not change permissions,
budgets or topology outside the approved envelope.

## Worktree gate

Choose `per-worker` only for independent code write-sets, clean base revision,
named branch/workspace owner, integration order, conflict policy, test gate and
recoverable cleanup. Read-only discovery does not need a worktree.
