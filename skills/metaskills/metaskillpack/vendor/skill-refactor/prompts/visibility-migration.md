# Visibility Migration Prompt

Choose `PROMOTE_PUBLIC` or `DEMOTE_PRIVATE` only after a consumer inventory and
boundary assessment prove that current visibility is wrong.

1. Resolve exact source skill, owner, consumers, registry/map, host adapters,
   current discovery behavior, desired visibility, and mutation authority.
2. Compare owner assumptions, triggers, permissions, data, resources, versions,
   release cadence, and evaluation criteria.
   Treat a second consumer as evidence to assess; require a generalized,
   owner-independent contract and justified public lifecycle before promotion.
3. Stage the destination candidate without removing the source.
4. Produce exact registry, binding, agent-definition, consumer, adapter, and
   version changes.
5. Test coexistence, owner use, unauthorized access, global discovery or
   non-discovery, behavior, hashes, and rollback.
6. Migrate consumers through the approved lifecycle manager.
7. Retire the source only after observed host state and consumers are verified.

Reject a migration whose only rationale is folder tidiness. Do not claim that a
private destination makes files confidential.
