# Мастер-промпт навыка `agent-registry-manager`

Применяй после [agent-os-base.md](agent-os-base.md). Создай control-plane skill
для typed desired-state registries of agents, skills, commands, workflows,
teams, tools, models and policies.

Implement stable IDs, discriminated kinds, SemVer/revision strategy, content
hash, locator, provenance, trust, lifecycle, accountable owner, compatibility
and replacement. Maintain versioned bindings separately. Mutations require
schema validation, optimistic revisions, authorization, referential checks,
candidate diff, atomic/rollback behavior and audit event. Generated Markdown,
search and graph views are projections only.

Reconcile desired and observed host/runtime state; quarantine unknown or stale
assets. Test duplicate IDs, missing refs, cycles, hash drift, stale writer,
partial transaction, unauthorized owner, private binding escape, deprecation
and retirement. Never equate registered with trusted or active.
