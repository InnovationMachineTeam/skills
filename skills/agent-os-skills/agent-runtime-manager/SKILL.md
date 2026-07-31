---
name: agent-runtime-manager
description: Governs platform-level durable task and run lifecycle with queues, attempts, leases, fencing, idempotency, checkpoints, cancellation, deadlines, backpressure, scoped execution, artifacts, compensation and dead-letter recovery. Use when designing, validating, operating or recovering Agentic OS runtime state across workers or teams. Do not design teams or agents, enforce permission only in prompts, silently retry permanent or ambiguous side effects, or mutate pinned agent/workflow/model/policy versions during a run.
metadata:
  version: "1.0.0"
---

# Govern Durable Agentic OS Runs

Pin exact agent, workflow, model and policy versions per run. Keep scheduler,
executor, policy and verifier responsibilities separate; enforce budgets and
stop conditions outside model prompts.

Read [references/runtime-contract.md](references/runtime-contract.md). Accept a
typed task envelope and advance only through declared state transitions. Use
idempotency/deduplication, bounded attempts, leases with fencing, heartbeats,
checkpoints, deadline/backpressure and scoped sandbox/credential references.

```bash
python3 scripts/validate_runtime_record.py runtime-record.json
```

Classify transient, permanent, policy, dependency, conflict, budget,
cancellation and ambiguous-effect failures. Retry only safe transient work;
use saga compensation, dead letter, rollback or escalation otherwise. Resume
after checkpoint and external-state revalidation. Test duplicate/out-of-order
delivery, worker loss, lease expiry, store/provider outage, partial effect,
cancellation race and poison task.

Return state, pinned versions, owner/lease, attempts, budgets, artifacts,
policy/verifier evidence, recovery and SLO signals. Never claim terminal success
without acceptance and independent verification.
