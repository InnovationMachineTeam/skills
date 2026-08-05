# Agent OS and Runtime Patterns

## Agent OS as a management platform

Agent OS is not a "main super-agent", but a platform layer that makes agent
execution reproducible, governable, and observable. It separates probabilistic
model decisions from deterministic control, security, and state mechanisms.

Recommended decomposition:

```text
experience plane   - users, IDE, API, chat, approvals
control plane      - intent, registry, planning, routing, policy, scheduler
execution plane    - agents, tools, sandboxes, connectors, model gateways
knowledge plane    - context, memory, artifacts, provenance, retrieval
assurance plane    - evals, verification, security, audit, release gates
operations plane   - telemetry, budgets, incidents, reconciliation, lifecycle
```

Planes are logical boundaries. In a small setup they may run in one process,
but their contracts and accountability should still remain distinct.

## Control plane

### Capability registry

The registry describes agents, skills, tools, workflows, models, and adapters
through versioned manifests. Minimum fields: identity, version, owner,
capabilities, trigger/input/output schemas, permissions, compatibility,
dependencies, risk tier, eval status, lifecycle state, and provenance.

Discovery does not mean authorization: a discovered capability must still pass
policy, compatibility, and health gates.

### Workflow registry

Repeatable processes are stored separately from runtime state. A definition is
immutable after publication; a run references the exact version. Updating a
workflow does not change already started runs without an explicit migration
policy.

### Hybrid orchestrator

Code owns states, retries, budgets, permissions, approvals, and durable
execution. The model performs classification, local planning, and synthesis in
bounded space. Any generated plan passes schema, capability, cycle,
permission, and cost validation.

### Desired-state reconciliation

For installed skills, workers, schedules, and long-running tasks, keep desired
and observed state. A reconciler fixes drift idempotently and creates an audit
event. This pattern is more reliable than a one-off `upgrade` command because
it detects partial failures and later drift.

## Execution plane

### Ports and adapters

The canonical internal contract isolates platform-specific Claude Code, Codex,
Cursor, MCP, A2A, and vendor APIs. An adapter translates manifests, tool calls,
approvals, and events without leaking platform assumptions into the core
workflow.

### Sandboxed worker

Each run receives an identity, read-only context, separate working state,
allowed tools, network policy, secret grants, quotas, and expiry. Credentials
are issued just in time and do not enter prompts, logs, or durable artifacts.

### Execution lease

A worker receives a lease on a task and extends it with a heartbeat. After
expiry, the scheduler may assign the task again; therefore side effects require
an idempotency key or an observed-state check. A lease is not a distributed
lock for an external system.

### Outbox / inbox

A local state change and the intent to send an event are recorded atomically;
the dispatcher delivers the event repeatedly, and the consumer deduplicates by
ID. This eliminates the classic loss between "saved the task" and "sent the
message."

### Saga

A long-running workflow is split into local commits. For each irreversible or
externally visible step, define compensation or explicitly record that the step
is non-compensatable and requires stronger approval before execution.

## Knowledge and state plane

### Event log + projections

Append-only events are the run history; the task board, dashboard, and current
state are built as projections. This enables replay and audit without requiring
full event sourcing for every document. Commands should be idempotent, and
events should be versioned and correlated with intent, actor, and artifact
versions.

### Immutable artifact + mutable pointer

Spec, plan, result, evaluation, and release bundle are stored as
content-addressed or immutable versions; a short pointer denotes the current
approved version. This prevents silent substitution of evidence and simplifies
rollback.

### Provenance graph

Links such as `derived_from`, `supersedes`, `implements`, `verified_by`, and
`released_as` provide traceability from intent to production observation. An
edge contains actor, timestamp, method, and confidence. A summary without links
is not added as fact.

### Tiered memory

- run context - lives for a single run;
- episodic memory - verified events and results;
- semantic memory - stable facts with source and TTL;
- procedural memory - versioned skills/workflows;
- policy memory - only an authoritative controlled store.

Writes to long-term memory pass curation, provenance, sensitivity, and expiry.

## Assurance plane

### Policy decision point / enforcement point

The PDP returns `allow`, `deny`, or `require_approval` together with the policy
version and reason codes. The PEP sits at the real action boundary and does not
rely on prompt obedience. Policy changes are versioned and tested on historical
decision cases.

### Evidence gate

A gate accepts not the text "done", but a typed bundle: input versions,
executed checks, raw results, coverage, exceptions, approvals, and residual
risks. The verdict is machine-readable and has an expiry if the evidence becomes
stale quickly.

### Shadow, canary, and champion-challenger

A new version first runs without side effects on production-like inputs, then on
a limited share of runs. Champion and challenger are compared on quality,
safety, latency, and cost; promotion requires a predefined threshold. It is not
acceptable to optimize one metric at the cost of invisible degradation in the
others.

### Tamper-evident audit

An audit record contains actor/agent identity, delegated authority, exact
versions, tool calls, approvals, side effects, and evidence refs. Sensitive
prompt content is redacted by policy, but the fact of the action and decision
metadata are preserved.

## Operations plane

### MAPE-K controller

Runtime operations are conveniently built as Monitor -> Analyze -> Plan ->
Execute over shared Knowledge. Sensors collect signals, and effectors change
the managed element. The classic IBM model treats the managed element and the
autonomic manager separately
([IBM MAPE-K](https://dominoweb.draco.res.ibm.com/reports/h-0219.pdf)).

### Bulkheads and budget governors

Separate quotas per tenant, workflow, agent, model, and tool prevent cascading
exhaustion. A budget includes tokens, money, wall time, tool calls, parallel
workers, and retries. Exceeding it moves a run into an explicit terminal or
human-input state rather than endless quality degradation.

### Circuit breaker and fallback ladder

The breaker opens on errors/latency of a specific dependency; fallback follows a
preapproved ladder: retry -> alternative model/tool -> degraded read-only mode
-> human queue -> stop. A fallback MUST preserve the security and quality floor;
a cheaper model is not an acceptable fallback for every decision.

### Reconciliation and orphan recovery

A periodic controller looks for expired leases, incomplete outbox, stale
approval, broken pointer, incompatible skill, and an unclosed run. Recovery
creates a new event and does not rewrite history. After the maximum attempts,
the task enters a dead-letter state with actionable diagnostics.

## Interoperability

- **MCP** connects an agent/runtime to tools, data, and prompts; capability
  listing does not replace authorization
  ([MCP specification](https://modelcontextprotocol.io/specification/latest)).
- **A2A** defines cross-agent discovery, tasks, messages, and artifacts between
  independent systems
  ([A2A specification](https://a2a-protocol.org/latest/specification/)).
- Internal calls use typed contracts regardless of transport.
- Cross-boundary identity, policy, provenance, and revocation are mandatory.
- Negotiated capability and protocol version are preserved in the run record.

## Lifecycle states of platform entities

One model for agent, skill, workflow, tool adapter, and policy:

```text
draft -> candidate -> verified -> approved -> published -> active
                                v             v         v
                              rejected      suspended  deprecated -> retired
```

`published` means availability in the registry; `active` means routing is
allowed. A deprecated entity remains readable and includes a replacement/
migration deadline. Retirement revokes routes and credentials, archives
evidence, and verifies that active dependents are absent or migrated.

## Reference runtime contract

```yaml
run:
  id: run_123
  intent_ref: artifact://intent/sha256:...
  workflow: feature-delivery@2.4.1
  policy: company-agent-policy@7
  identity: agent://orchestrator/release
  delegated_by: user://owner
  budgets:
    wall_time_s: 1800
    tool_calls: 80
    cost_usd: 12
  state: waiting_for_approval
  checkpoint_ref: event://run_123/42
  artifacts: []
  evidence: []
  approvals: []
```

## Agent OS anti-patterns

- one global prompt simultaneously stores policy, state, and memory;
- a registry has no versions, owner, compatibility, or revocation;
- "exactly once" is assumed without idempotency and reconciliation;
- observability stores secrets or full sensitive context;
- a worktree or prompt is used as a security boundary;
- auto-upgrade changes active behavior without eval, canary, and rollback;
- human approval is requested without a diff, evidence, or side-effect
  description;
- a long-running run cannot be canceled, resumed, or safely terminated;
- a retired agent remains accessible through an old route or credential.
