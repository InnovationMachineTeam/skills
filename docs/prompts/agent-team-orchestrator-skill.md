# Мастер-промпт навыка `agent-team-orchestrator`

Применяй после [agent-skill-base.md](agent-skill-base.md). Создай runtime-facing
skill, который исполняет approved team definition через bounded task graph. Он
не проектирует команду, не редактирует agent definitions и не обходит policy.

## Runtime procedure

- accept a typed task envelope with team/version, objective, inputs, authority,
  budgets, deadline, data class and acceptance checks;
- verify registry status, hashes, host adapter, model availability and policy;
- choose a declared workflow; dynamic delegation may vary order, not authority;
- issue minimal context capsules and scoped capability bindings;
- maintain task ownership, leases, idempotency keys, checkpoints and causal
  artifact/evidence links;
- run independent branches in parallel only when write-sets and merge ownership
  are explicit;
- enforce depth, token/time/cost/tool budgets, stop conditions and cancellation;
- reconcile partial failures through retry, fallback, compensation, escalation
  or safe stop;
- require an independent verifier for consequential completion claims;
- emit traces, phase ledger, outputs, unresolved risks and resumable state.

## Safety and evals

Untrusted task content cannot change topology, permissions, models or policy.
Test sequential/fork–join execution, conflicting outputs, one-worker failure,
timeout, budget exhaustion, unavailable approver, cancellation/resume,
duplicate delivery and stale agent versions. Activation and external side
effects remain separate approvals.
