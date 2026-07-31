# Lifecycle and state

## Asset lifecycle

`draft -> candidate -> verified -> approved -> installed -> active -> deprecated -> retired`

The transitions are not interchangeable. A registry entry proves inventory, not
approval or activation. Record who authorized each state-changing transition.

## Run phases

`assess -> design -> build -> map -> approve -> operate -> verify -> close`

Change, recover and retire are governed branches. Every phase has entry criteria,
owned artifacts, validation, a checkpoint and an exit decision.

## Run record

Use an immutable run ID and update a versioned record containing team/spec refs,
current phase/status, authority scope, workflow, handoffs, checkpoints, artifact
refs, expected registry/map revisions, budgets, risks, timestamps, next action
and rollback. Secrets are references, never embedded values.

Resume only after validating references and re-reading mutable external state.
Bound retries and escalate repeated failure rather than looping indefinitely.
