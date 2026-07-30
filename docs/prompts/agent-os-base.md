# Общий мастер-промпт Agentic OS

Используй этот contract после [agent-skill-base.md](agent-skill-base.md) и перед
ровно одним Agentic OS specialist prompt. Создавай platform/control capability,
а не mega-agent и не набор файлов без runtime contract.

## Planes и invariants

Разделяй:

- experience plane: user/API entry, progress, approvals and explanations;
- control plane: desired state, registry, policy, model/capability routing;
- execution plane: queues, tasks, leases, sandboxes, tools and checkpoints;
- knowledge plane: docs, retrieval, memory, provenance and deletion;
- assurance plane: evals, security, compliance and release gates;
- operations plane: telemetry, SLO, incidents, recovery and cost.

Каждый plane имеет API/schema, accountable owner, state store, permissions,
SLO, threat/failure model and lifecycle. LLM output is untrusted proposal until
validated by deterministic policy/execution boundaries.

## Required architecture

Model desired versus observed state and reconciliation. Use stable identities,
versioned definitions, immutable run references and typed registries for agents,
skills, workflows, models, tools and policies. Enforce least privilege through
identity, credential broker, PDP/PEP and scoped approvals. Execution must be
idempotent or explicitly compensated, resumable and cancellable with leases,
heartbeats, checkpoints, deduplication and bounded retries.

Preserve artifact/provenance graph. Separate working, episodic, semantic,
procedural and policy memory; define owner, TTL, deletion and poison recovery.
Use ports-and-adapters for MCP/A2A/provider/host boundaries. Every deployment
supports shadow/canary, rollback, compatibility, deprecation and retirement.

## Quality contract

Specify budgets for tokens, cost, latency, tool calls, delegation depth and
wall-clock. Emit traces with task/agent/model/tool/policy/artifact versions.
Design failure drills for provider outage, queue duplication, lease expiry,
partial side effects, stale policy, unavailable approver, corrupted memory,
cross-tenant access and rollback failure. Require operator/runbook ownership.

## Scope gate

Reject Agentic OS when a project workflow or team runtime is enough. Do not add
databases, service mesh, GraphRAG or dynamic model routing before a measured
scale/reliability need and an operating owner exist.
