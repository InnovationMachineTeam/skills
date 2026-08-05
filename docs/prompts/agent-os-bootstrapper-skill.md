# Master Prompt For The `agent-os-bootstrapper` Skill

Apply after [agent-os-base.md](agent-os-base.md). Create a skill that
materializes an approved Agentic OS walking skeleton in staging with one vertical
flow. It does not expand the architecture or start a production rollout.

Build one authenticated request → policy decision → queued task → leased worker
→ bounded tool call → artifact/evidence → verifier → terminal state flow. Use
version-pinned adapters, migrations, synthetic credentials/data and disposable
stores. Generate registries, schemas, local development setup, health checks,
telemetry, runbook and deterministic smoke/failure tests.

Require idempotency, duplicate delivery, timeout, cancellation, resume, provider
outage and rollback fixtures. Apply staged changes transactionally and retain no
active partial system. Return reproducible setup, exact versions, trace bundle,
known unsupported planes and readiness handoff.
