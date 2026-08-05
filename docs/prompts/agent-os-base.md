# General Agentic OS Master Prompt

Use this contract after [agent-skill-base.md](agent-skill-base.md) and before
exactly one Agentic OS specialist prompt. Create a platform/control capability,
not a mega-agent and not a set of files without a runtime contract.

## Planes And Invariants

Separate:

- experience plane: user/API entry, progress, approvals and explanations;
- control plane: desired state, registry, policy, model/capability routing;
- execution plane: queues, tasks, leases, sandboxes, tools and checkpoints;
- knowledge plane: docs, retrieval, memory, provenance and deletion;
- assurance plane: evals, security, compliance and release gates;
- operations plane: telemetry, SLO, incidents, recovery and cost.

Each plane has an API/schema, accountable owner, state store, permissions,
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
