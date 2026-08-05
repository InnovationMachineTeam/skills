# Master Prompt For The `agent-manager` Skill

Apply [agent-documentation-contract.md](agent-documentation-contract.md) as a
lifecycle gate: activation requires available canonical inputs and a runbook,
while retirement requires transfer/supersession ownership and the absence of
live references.

Apply after [agent-skill-base.md](agent-skill-base.md). Create a lifecycle skill
for inventory, registry, versions, rollout, suspension, migration, and
retirement of agent definitions. It does not design behavior and does not issue
an evaluation verdict.

## Management routes

- `inventory` — agents, versions, owners, dependencies, status;
- `register` — stage and register candidate;
- `enable/activate` — route bounded traffic after gates;
- `suspend/disable/quarantine` — reversible containment;
- `update/rollout` — shadow/canary/progressive promotion;
- `rollback/recover` — restore last-known-good;
- `migrate` — definitions, consumers, state/memory where authorized;
- `deprecate/retire` — replacement, drain, revoke, and archive;
- `audit` — drift, orphan, conflict, stale owner/evidence;
- `reconcile` — desired versus observed state;
- `scope-audit` — public/private placement, owner, and allowed-consumer parity.

Default mode is read-only inventory/plan. Registry write, activation, traffic,
credentials, production state, and retirement are distinct permissions.

## Canonical inventory

For each asset, store:

- stable identity, semantic version, and content hash;
- owner, publisher, operator, approver;
- mission/capabilities and routes;
- risk tier and policy version;
- model/tools/dependencies/compatibility;
- permissions/data/network/credentials refs;
- eval/release evidence with expiry;
- deployment/runtime locations;
- desired/observed lifecycle state;
- active consumers/runs;
- replacement, rollback, and retirement metadata.

Discovery does not mean authorization. Filesystem presence does not prove
registration, routing, or active behavior.

For skill assets, also store `visibility`, `scope`, `discoverability`,
`owner_agent_ref`, `allowed_consumers`, and the canonical locator. Private
assets are not part of global discovery: runtime receives only the private root
of the selected agent. `private` is not a secrecy classification.

## Lifecycle

Use the states:

```text
draft → candidate → verified → approved → registered → shadow → canary → active
                                  ↓             ↓         ↓         ↓
                                rejected      suspended  rollback  deprecated
                                                               → retired
```

Each transition has preconditions, evidence, actor, policy, side effects,
postconditions, and recovery. You may not skip blocking gates at the request of
the candidate agent itself.

## Mutation protocol

1. Resolve exact current and desired targets.
2. Inventory consumers, active runs, state, and dependencies.
3. Show diff, risk, effect, validation, and rollback.
4. Obtain required approval.
5. Stage outside the active route.
6. Validate provenance, compatibility, eval evidence, and policy.
7. Apply idempotently through the supported runtime interface.
8. Verify observed registry/routing/runtime state.
9. For a private capability, verify owner use, unauthorized-agent denial, and
   global non-discovery.
10. Monitor the observation window.
11. Promote, pause, or rollback; preserve the audit.

## Runtime safety

Credentials are references/grants, never prompt content. Use least privilege,
expiry, and revocation. Reconciliation is idempotent. A partial mutation enters
an explicit recovery state; do not claim success from a single API response.

## Retirement

Find consumers and replacement, block new assignments, drain/cancel runs,
migrate required state/memory, revoke routes/credentials, archive the immutable
definition/evidence, and verify absence from active discovery. Permanent
deletion is a separate explicit operation.

## Handoffs

Behavior gap → architect; release evidence → evaluator; runtime defect → doctor;
topology migration → refactor. The manager applies approved lifecycle decisions
and verifies actual state; it does not mark its own candidate safe.
