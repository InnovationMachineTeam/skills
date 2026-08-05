# Master Prompt For Private/Public Skill Visibility Migration

Run through `skill-refactor` when the current visibility does not match the
real consumers and lifecycle.

## Promotion gate

`PROMOTE_PUBLIC` is allowed only when an approved independent consumer exists,
the contract is generalized beyond the original agent, and an independent
owner/evals/release cadence/lifecycle justifies a public surface. A second
consumer triggers an assessment, but does not grant automatic promotion. Remove
owner-agent assumptions, stage the public candidate, assign a public
identity/version, update registry/map/adapters, verify coexistence and
consumers, then retire the private source through the manager.

## Demotion gate

`DEMOTE_PRIVATE` is allowed only after inventory proves a single remaining
owner agent. Stage the private candidate, set the owner and allowed consumers,
update agent version/registry/map/adapters, verify global non-discovery and
denial for other agents, then retire the public source.

## Plan and evidence

Return exact source/destination hashes, consumers, contract diff, permissions,
file operations, registry/map diff, agent version effect, compatibility window,
host adapter changes, eval matrix, approvals, rollback, and stop conditions.

Do not implement the migration as a simple move. Do not claim that a private
path provides confidentiality. `skill-manager` performs lifecycle mutations
after independent evaluation of the exact candidate.
