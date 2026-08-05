# Master Prompt For The `agent-refactor` Skill

Apply [agent-documentation-contract.md](agent-documentation-contract.md).
A topology change includes migration of document ownership, paths, links,
indexes, freshness triggers, and rollback; moving a directory by itself does
not complete the migration.

Apply after [agent-skill-base.md](agent-skill-base.md). Create a skill that
first evaluates and then safely changes the boundaries and topology of existing
agents, subagents, orchestrators, and teams.

## Capability boundary

Support routes:

- `compare` — read-only pairwise/multi-agent analysis;
- `merge` — merge coherent missions;
- `split` — split an oversized agent;
- `extract` — extract a reusable specialist/capability;
- `compose` — create an orchestrated topology without a physical merge;
- `facade` — compatibility router/handoff bridge;
- `migrate` — staged consumer/runtime transition;
- `promote-public` — a private capability becomes independently reusable;
- `demote-private` — a public capability with a single owner agent stops
  participating in global discovery.

Topology mutation requires an evidence-backed decision and approval. Ordinary
prompt optimization belongs to `agent-optimizer`.

## Boundary model

Compare:

- users, intents, mission, and non-goals;
- tools, permissions, identities, and data classes;
- context/memory/state ownership;
- runtime cycles, budgets, and failure models;
- inputs/outputs/handoff contracts;
- evaluation criteria and risk tiers;
- owners, SLO, release cadence, and on-call;
- consumers, dependencies, and blast radius.

Strong split signals: different identities/permissions, risk tiers, owners,
state, SLO, or unrelated intents. Strong merge signals: one mission, shared
state, the same authority, and a unified completion contract. Similar prompts
alone do not prove a merge.

## Refactor plan

Before mutation, create:

- current/desired topology;
- capability and consumer mapping;
- interface/schema/version changes;
- state/memory migration;
- identity/credential changes;
- routing/coexistence plan;
- eval and shadow/canary plan;
- rollback and retirement plan;
- exact write/mutation set;
- approvals and stop conditions.

## Safe execution

- Stage new definitions beside current active versions.
- Do not allow two writers for the same external resource without arbitration.
- Use a compatibility facade only with owner, metrics, and expiry.
- Drain/cancel/migrate active runs explicitly.
- Do not copy memory without provenance, consent, and retention review.
- Revoke old routes/credentials only after verified migration.
- Visibility migration changes registry/map, host adapters, owner agent version,
  consumers, and evals; a folder move is insufficient.
- Promotion requires a second independent consumer or an independent lifecycle;
  demotion requires a proven single owner.

## Evaluation

Verify preserved outcomes, route collisions, handoff fidelity, context loss,
partial failures, shared-state races, latency/cost, permissions, old/new
coexistence, rollback, and removal of deprecated dependencies.

## Output

Return `KEEP`, `COMPOSE`, `MERGE`, `SPLIT`, `EXTRACT`, `FACADE`,
`PROMOTE_PUBLIC`, `DEMOTE_PRIVATE`, or `REJECT`,
decision evidence, topology plan, staged candidate, migration/rollback evidence,
and unresolved risks. Do not hide a rejection just because the user suggested a merge.
