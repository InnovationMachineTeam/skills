---
name: agent-os-bootstrapper
description: Materializes an approved Agentic OS architecture as one staged, reproducible vertical walking skeleton from authenticated request through policy, registry, durable task and lease, bounded execution, artifact verification, telemetry and terminal state. Use when an exact approved architecture and destination are ready for local bootstrap, rebuild or migration. Do not redesign planes, use production credentials, activate or roll out production, retain partial active state, or expand beyond the approved vertical slice.
metadata:
  version: "1.0.1"
---

# Bootstrap an Approved Agentic OS Slice

Require exact architecture ID/version/hash, approved status, destination, host
versions, synthetic data/credentials, expected revisions, write authority and
rollback. Missing or stale inputs return `BLOCKED`.

Read [references/bootstrap-contract.md](references/bootstrap-contract.md).
Create an exact manifest covering schemas, registries, policy, local durable
state, adapters, health checks, telemetry, runbook and smoke/failure fixtures.
Use disposable stores and version-pinned adapters. Set production activation to
false and stage all operations before promotion.

```bash
python3 scripts/validate_bootstrap_manifest.py bootstrap-manifest.json
```

Exercise one authenticated request → policy decision → queued task → fenced
lease → bounded tool call → artifact/evidence → independent verifier → terminal
state. Test duplicate delivery, timeout, cancellation/resume, provider outage,
partial effect and rollback. Reconcile exact output against the manifest and
remove or roll back failed partial candidates.

Return `STAGED`, `VERIFIED`, `NOOP`, `BLOCKED` or `ROLLED_BACK` with versions,
write-set, trace bundle, tests, unsupported planes and readiness handoff. Never
call staged infrastructure production-ready.
