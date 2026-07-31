---
name: agent-refactor
description: Assesses and safely changes the capability, ownership or topology boundaries of existing individual agents through merge, split, extraction, composition, promotion to a team, or public/private capability and documentation migration. Use when an agent has mixed missions, duplicated roles, unsafe authority coupling, excessive context, changing consumers, or needs a versioned topology migration. Do not tune a healthy agent, repair a local defect, design a new agent from scratch, silently rewrite teams or Agentic OS, move folders without consumer migration, or activate the result.
metadata:
  version: "1.0.0"
---

# Refactor Agent Boundaries

Topology changes are consumer and authority migrations, not file moves. Default
to read-only assessment and preserve the last-known-good topology.

Read [references/skill-dependencies.md](references/skill-dependencies.md) and
block only the architecture, evaluation or lifecycle route whose required
companion is unavailable.

## Assess the boundary

Inventory exact agents/versions, missions, triggers, users, tools, permissions,
state, memory, documents, capabilities, consumers, runtime bindings, evals and
owners. Read [references/refactor-contract.md](references/refactor-contract.md).

This skill owns migration assessment when one or more existing agent identities
already exist. `agent-team-architect` owns greenfield team-worth assessment and
the team design after this skill returns `PROMOTE_TO_TEAM`.

Choose one decision: `KEEP`, `MERGE`, `SPLIT`, `EXTRACT_CAPABILITY`,
`COMPOSE_WORKFLOW`, `PROMOTE_TO_TEAM`, `MIGRATE_VISIBILITY`, `RESEARCH` or
`REJECT`. Require evidence that the new boundary improves cohesion, authority,
context, ownership, evaluation or lifecycle cost.

## Plan a recoverable migration

Define old/new topology, stable identity strategy, SemVer impact, compatibility
facade, consumer order, registry/map changes, runtime drain, state/memory
migration, document ownership/path/link/index/freshness migration, coexistence
window, evaluation and rollback.

Use `agent-team-architect` after a `PROMOTE_TO_TEAM` decision; do not design the
team internally. Greenfield requests with no existing agent asset route directly
there. Use `skill-refactor` for capability-package topology.

Apply only with exact mutation authority and optimistic revisions. Validate old
and new routing, consumers, permissions, documentation, recovery and absence
conditions before retiring the old topology.

Return decision, evidence, migration plan, changed identities/versions,
consumer and document migrations, eval results, rollback and handoff to
`agent-evaluator` then `agent-manager`.
