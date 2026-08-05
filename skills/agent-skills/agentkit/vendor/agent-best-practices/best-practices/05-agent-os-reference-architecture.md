# Agent OS Reference Architecture

## Purpose

Agent OS turns isolated prompts and tools into a managed system. It must
separate **what the agent can do** from **who, when, and with which authority
can launch it**.

## Layers

```text
Experience plane
  CLI · IDE · chat · dashboard · API · automation triggers
                         │
Control plane
  intent router · planner · scheduler · policy · approvals · budgets
                         │
Execution plane
  agents · workflows · models · tools · sandboxes · worktrees
                         │
Knowledge and state plane
  docs · specs · task graph · artifacts · memory · registry · provenance
                         │
Assurance plane
  evals · verification · security · tracing · metrics · audit · incident response
```

Assurance is a cross-cutting layer, not a final stage.

## Capability Registry

The registry MUST store for each agent, workflow, and tool:

- stable ID, owner, and semantic version;
- purpose, inputs, outputs, and examples;
- required permissions and risk class;
- supported runtime/model;
- dependencies and compatibility range;
- evaluation status and last verified;
- lifecycle: experimental, active, deprecated, revoked;
- supply signature, digest, and provenance.

The router selects not an agent name from a prompt, but a capability that
satisfies policy and contract. For external systems, an A2A Agent Card provides
discovery, capabilities, interfaces, and security schemes
([A2A specification](https://a2a-protocol.org/latest/specification/)).

## Control Plane

The control plane is responsible for:

- intent normalization;
- autonomy-level selection;
- DAG construction;
- compatibility checking;
- budget and permission-envelope allocation;
- lease/ownership;
- approvals and checkpoints;
- cancellation, retries, and recovery;
- final synthesis/verification;
- policy decision log.

The LLM may propose a plan, but the policy engine and scheduler SHOULD be
deterministic.

## Execution Plane

Each run receives:

- immutable run ID and parent trace;
- agent/tool/model versions;
- isolated workspace or read-only view;
- scoped credentials;
- network policy;
- input snapshot and artifact references;
- token/time/tool-call budget;
- cancellation signal;
- output sink and audit channel.

A worktree isolates file changes, but not necessarily `.git`, permissions,
plugins, or secrets. Therefore, a worktree MUST be supplemented with a sandbox
and policy ([Claude worktrees](https://code.claude.com/docs/en/worktrees)).

## State Model

Separate:

1. **Source state**: code, canonical specs, policies.
2. **Workflow state**: tasks, leases, checkpoints, retries.
3. **Session state**: current context and temporary results.
4. **Memory**: verified reusable knowledge.
5. **Observability data**: append-only traces, metrics, and audit.
6. **Artifacts**: versioned outcomes with provenance.

Markdown is convenient for people and agents, but the task scheduler SHOULD have
a strict schema. GSD Core uses file-based `STATE.md`; GSD Pi combines a local
database with Markdown projections. The recommended compromise is structured
canonical state plus human-readable projections that are checked for drift.

## Artifact Protocol

An artifact MUST have:

```yaml
artifact_id: spec-checkout-v3
type: specification
schema_version: 2
created_by: requirements-agent@1.4.0
run_id: run_...
sources: [prd@sha256:..., interview@sha256:...]
created_at: 2026-07-30T12:00:00Z
status: draft | reviewed | approved | superseded
owner: product-checkout
content_digest: sha256:...
```

Derived documents reference their sources; changing a canonical document marks
dependent artifacts as stale.

## Policy and Autonomy Levels

| Level | Behavior |
|---|---|
| A0 | Advice only, no tools |
| A1 | Read-only tools |
| A2 | Local reversible changes |
| A3 | External changes with prior approval |
| A4 | Delegated actions in a pre-approved envelope |
| A5 | Fully autonomous bounded loop with post-review |

The level is assigned based on the combination of agent trust, action risk,
data sensitivity, and environment. An agent cannot raise its own level.

## Runtime Adapters

The universal contract is translated into platform surfaces:

- Codex: `AGENTS.md`, skills, custom agents, sandbox, and worktrees;
- Claude Code: `CLAUDE.md`, subagents, teams, hooks, workflows, and worktrees;
- Cursor: rules, subagents, cloud agents, automations, Bugbot, and approval
  agents;
- service runtimes: SDK, queue, sandbox, A2A/MCP, and telemetry.

The adapter MUST document mismatches: delegation depth, permission inheritance,
resume, background behavior, tool syntax, and supported metadata.

## Extensions

GSD Pi practice is useful as a model:

- `core`: non-disableable minimum;
- `bundled`: ships with the system but can be disabled;
- `community`: external extension;
- manifest lists version, compatibility, capabilities, and dependencies;
- topological load order;
- unique namespaced tool IDs;
- state reconstruction on all lifecycle events;
- bounded tool output and cancellation.

An extension without a manifest MAY work in development, but must not enter the
managed registry.

## Lifecycle

```text
proposed → experimental → evaluated → active → deprecated → revoked → archived
```

Transitions require evidence. Revocation must immediately disable new runs and
define the fate of already-running ones. Upgrade is performed via compatibility
checks, canary evals, and rollback.

## Minimal Agent OS

Do not start with a full platform. A sufficient MVP:

1. registry of agents/tools;
2. task envelope and result envelope;
3. deterministic permission policy;
4. durable run/task state;
5. sandbox/worktree adapter;
6. traces and cost metrics;
7. eval suite;
8. human approval queue;
9. documentation index.
