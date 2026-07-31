# Scenario catalog

## Assess

Use when no approved team spec exists or the user asks whether multiple agents
are worthwhile. Route deep evidence gathering to existing scouting/harvesting
capabilities and design to `agent-team-architect`.

## Design

Requires a bounded outcome and design authority. `agent-team-architect` owns
roles, topology, interaction and worktree policy. `agent-model-selector` owns
current design-time model evidence. End at a review candidate or approved spec.

## Build

Requires an approved exact spec, write authority and destination.
`agent-team-builder` stages and validates files. Building never implies launch.

## Map capabilities

`agent-skill-mapper` inventories and recommends read-only by default. Applying a
map requires explicit mutation authority and versioned registry/map revisions.

## Operate

Requires an approved build, active bindings, run plan, budgets and host/runtime
authority. The manager coordinates available runtime primitives but must not
claim a host feature that is unavailable.

## Change and recover

Classify impact before selecting architect, builder, mapper or operator. Freeze
unsafe writes, preserve evidence, prefer rollback to improvising on corrupted
state and resume only from a validated checkpoint.

## Retire

Stop new assignments, drain or cancel runs, revoke active bindings, archive
evidence, update lifecycle state and leave a reversible migration path where
policy requires it.
