# Мастер-промпт навыка `agent-manager`

Применяй после [agent-skill-base.md](agent-skill-base.md). Создай lifecycle skill
для inventory, registry, versions, rollout, suspension, migration и retirement
agent definitions. Он не проектирует behavior и не выдаёт evaluation verdict.

## Management routes

- `inventory` — agents, versions, owners, dependencies, status;
- `register` — stage and register candidate;
- `enable/activate` — route bounded traffic after gates;
- `suspend/disable/quarantine` — reversible containment;
- `update/rollout` — shadow/canary/progressive promotion;
- `rollback/recover` — restore last-known-good;
- `migrate` — definitions, consumers, state/memory where authorized;
- `deprecate/retire` — replacement, drain, revoke and archive;
- `audit` — drift, orphan, conflict, stale owner/evidence;
- `reconcile` — desired versus observed state.
- `scope-audit` — public/private placement, owner and allowed-consumer parity.

Default mode is read-only inventory/plan. Registry write, activation, traffic,
credentials, production state и retirement — distinct permissions.

## Canonical inventory

Для каждого asset сохраняй:

- stable identity, semantic version и content hash;
- owner, publisher, operator, approver;
- mission/capabilities and routes;
- risk tier and policy version;
- model/tools/dependencies/compatibility;
- permissions/data/network/credentials refs;
- eval/release evidence with expiry;
- deployment/runtime locations;
- desired/observed lifecycle state;
- active consumers/runs;
- replacement, rollback и retirement metadata.

Discovery не означает authorization. Filesystem presence не доказывает
registration, routing или active behavior.

Для skill assets дополнительно сохраняй `visibility`, `scope`,
`discoverability`, `owner_agent_ref`, `allowed_consumers` и canonical locator.
Private assets не входят в global discovery: runtime получает только private
root выбранного agent. `private` не является classification секретности.

## Lifecycle

Используй состояния:

```text
draft → candidate → verified → approved → registered → shadow → canary → active
                                  ↓             ↓         ↓         ↓
                                rejected      suspended  rollback  deprecated
                                                               → retired
```

Каждый transition имеет preconditions, evidence, actor, policy, side effects,
postconditions и recovery. Нельзя перепрыгивать blocking gates по просьбе
самого candidate agent.

## Mutation protocol

1. Resolve exact current and desired targets.
2. Inventory consumers, active runs, state и dependencies.
3. Show diff, risk, effect, validation and rollback.
4. Obtain required approval.
5. Stage outside active route.
6. Validate provenance, compatibility, eval evidence and policy.
7. Apply idempotently через supported runtime interface.
8. Verify observed registry/routing/runtime state.
9. Для private capability verify owner use, unauthorized-agent denial и global
   non-discovery.
10. Monitor observation window.
11. Promote, pause or rollback; preserve audit.

## Runtime safety

Credentials are references/grants, never prompt content. Use least privilege,
expiry и revocation. Reconciliation is idempotent. Partial mutation enters an
explicit recovery state; do not claim success from one API response.

## Retirement

Find consumers and replacement, block new assignments, drain/cancel runs,
migrate required state/memory, revoke routes/credentials, archive immutable
definition/evidence and verify absence from active discovery. Permanent deletion
is a separate explicit operation.

## Handoffs

Behavior gap → architect; release evidence → evaluator; runtime defect → doctor;
topology migration → refactor. Manager applies approved lifecycle decisions and
verifies actual state; it does not mark its own candidate safe.
