# Мастер-промпт навыка `agent-refactor`

Применяй после [agent-skill-base.md](agent-skill-base.md). Создай skill, который
сначала оценивает, а затем безопасно меняет boundaries и topology существующих
agents, subagents, orchestrators и teams.

## Capability boundary

Поддержи routes:

- `compare` — read-only pairwise/multi-agent analysis;
- `merge` — объединить coherent missions;
- `split` — разделить oversized agent;
- `extract` — выделить reusable specialist/capability;
- `compose` — создать orchestrated topology без физического merge;
- `facade` — compatibility router/handoff bridge;
- `migrate` — staged consumer/runtime transition.
- `promote-public` — private capability становится independently reusable;
- `demote-private` — public capability с единственным owner agent перестаёт
  участвовать в global discovery.

Topology mutation требует evidence-backed decision и approval. Обычная prompt
optimization остаётся у `agent-optimizer`.

## Boundary model

Сравни:

- users, intents, mission и non-goals;
- tools, permissions, identities и data classes;
- context/memory/state ownership;
- runtime cycles, budgets и failure models;
- inputs/outputs/handoff contracts;
- evaluation criteria и risk tiers;
- owners, SLO, release cadence и on-call;
- consumers, dependencies и blast radius.

Strong split signals: разные identities/permissions, risk tiers, owners, state,
SLO или unrelated intents. Strong merge signals: одна mission, shared state,
same authority и unified completion contract. Similar prompts сами по себе не
доказывают merge.

## Refactor plan

До mutation создай:

- current/desired topology;
- capability and consumer mapping;
- interface/schema/version changes;
- state/memory migration;
- identity/credential changes;
- routing/coexistence plan;
- eval and shadow/canary plan;
- rollback and retirement plan;
- exact write/mutation set;
- approvals и stop conditions.

## Safe execution

- Stage new definitions beside current active versions.
- Не допускай двух writers одного external resource без arbitration.
- Используй compatibility facade только с owner, metrics и expiry.
- Drain/cancel/migrate active runs явно.
- Не копируй memory без provenance, consent и retention review.
- Revoke old routes/credentials только после verified migration.
- Visibility migration меняет registry/map, host adapters, owner agent version,
  consumers и evals; folder move недостаточен.
- Promotion требует второго independent consumer или самостоятельного
  lifecycle; demotion требует доказанного единственного owner.

## Evaluation

Проверяй preserved outcomes, route collisions, handoff fidelity, context loss,
partial failures, shared-state races, latency/cost, permissions, old/new
coexistence, rollback и removal of deprecated dependencies.

## Output

Верни `KEEP`, `COMPOSE`, `MERGE`, `SPLIT`, `EXTRACT`, `FACADE`,
`PROMOTE_PUBLIC`, `DEMOTE_PRIVATE` или `REJECT`,
decision evidence, topology plan, staged candidate, migration/rollback evidence
и unresolved risks. Не скрывай rejection только потому, что user suggested merge.
