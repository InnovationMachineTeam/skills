# Transferring Metaskill Patterns to Agent Work

Analysis date: **2026-07-30**.

## Executive Summary

The approach from `skills/metaskills/` applies to agents at two levels:

1. **As a skill architecture for working with agents**: `agent-architect`,
   `agent-evaluator`, `agent-doctor`, `agent-manager`, and other skills use a
   thin router, route-specific prompts, references, scripts, and evals.
2. **As the operating model of the agents themselves**: bounded handoffs,
   immutable candidates, independent evaluation, lifecycle states, donor locks,
   checkpoints, and authority gates carry over into Agent OS.

The portfolio cannot be copied literally. A skill is a loadable capability
package; an agent is a runtime actor with identity, tools, state, memory,
budgets, delegation, and side effects. Therefore, agent-oriented skills must
validate not only structure and triggers, but also execution traces,
permissions, recovery, SLOs, human oversight, and decommissioning.

The recommended outcome is a separate portfolio of skills for managing agents,
created from the master prompts in [prompts/README.md](prompts/README.md). `agent`
should not be added as a ninth primary archetype to `skill-architect`: it is a
skill application domain, not a mechanism. Instead, an agent-system profile is
needed, layered onto the existing workflow, evaluation, orchestration, tool
integration, and meta/router archetypes.

## What the Current Metaskill System Is

The portfolio contains 12 metaskills and one related prompt skill:

- lifecycle specialists: `skill-scout`, `skill-harvester`, `skill-architect`,
  `skill-evaluator`, `skill-doctor`, `skill-optimizer`, `skill-refactor`,
  `skill-manager`;
- orchestrators/control: `skill-builder`, `metaskillpack`;
- supporting systems: `skill-best-practices`, `skill-marketplace-manager`;
- prompt engineering: `prompt-optimize` from the `prompt-skills` category.

### Recurring Structure

```text
skill-name/
├── SKILL.md                 # thin contract, routing, and invariants
├── agents/openai.yaml       # host-facing metadata
├── prompts/                 # base + route-specific master prompts
├── references/              # detailed rules and schemas
├── scripts/                 # deterministic inventory/validation/comparison
├── evals/                   # routing, behavior, scripts, security
└── README.md                # only where package documentation is useful
```

Not every skill includes every directory. A resource is added only if it
reduces repeated reasoning, provides determinism, or is needed as an artifact.

### System Patterns

| Metaskill pattern | Implementation | Why it is useful |
|---|---|---|
| Thin router | `SKILL.md` selects one route | Keeps the full portfolio out of context |
| Base + specialization | Shared prompt and one route prompt | Shared invariants without duplication |
| Classification before creation | Archetype/scenario selected by outcome | Structure follows the hardest constraint |
| Specialist boundaries | Evaluator does not fix, doctor does not optimize | Preserves independence of evidence |
| Bounded handoff | Target, objective, scope, authority, output | Prevents downstream task expansion |
| Immutable candidate | A change gets a new revision | Baseline and regression remain reproducible |
| Layered evidence | Structure, routing, behavior, safety, E2E | Static PASS is not mistaken for quality |
| Preview before mutation | Inventory/diff/plan before write/install | Limits blast radius |
| Durable state | Phase ledger and resumable checkpoints | Supports long-running workflows |
| Lifecycle states | Draft → active → deprecated → retired | Provides migration and retirement |
| Donor lock | Version + tree hash + snapshot | Composite can be reproduced and updated |
| Explicit composite | `metaskillpack` is included explicitly | Does not compete with specialist triggers |

These patterns align with the catalogs for
[agent orchestration](../skills/agent-skills/agent-best-practices/best-practices/17-agent-and-orchestration-pattern-catalog.md),
[Agent OS](../skills/agent-skills/agent-best-practices/best-practices/18-agent-os-and-runtime-pattern-catalog.md),
and [skill design](../skills/agent-skills/agent-best-practices/best-practices/19-skill-design-pattern-catalog.md).

## What Transfers Directly to Agents

### Worth and duplication gate

Before creating an agent, the system must determine whether an autonomous actor
is warranted. Possible decisions:

- `USE_CODE_OR_WORKFLOW` — the task is deterministic;
- `USE_EXISTING_AGENT` — the capability is already covered;
- `EXTEND_EXISTING_AGENT` — the boundary of an existing agent remains coherent;
- `CREATE_NEW_AGENT` — separate mission, tools, context, or permissions are required;
- `KEEP_HUMAN` — the decision requires disproportionate human judgment;
- `RESEARCH` — the evidence is insufficient.

This is the agent analogue of `skill-scout`, but the ladder of complexity
should start with code, a single model call, and a workflow rather than
immediately with a new agent.

### Architect → evaluator → doctor/optimizer → manager

The sequence transfers almost completely:

```text
need/context
  → agent architect creates immutable candidate contract
  → agent evaluator produces independent layered evidence
  → doctor repairs reproduced defects
  → optimizer changes a healthy candidate against a metric
  → evaluator compares revisions
  → manager publishes/activates/canaries/retires
```

After each change, a new candidate revision is created; release authority does
not belong to the author, evaluator, or runtime agent.

### Builder as lifecycle orchestrator

`skill-builder` is the most useful model for `agent-builder`:

- it selects one primary scenario by observable outcome;
- it proposes the minimal specialist chain;
- it maintains a phase ledger and bounded handoffs;
- it does not imitate the work of specialists;
- it stops at mutation and approval gates;
- it validates evidence and the actual target-host state.

For agents, shadow/canary, SLOs, credentials, a kill switch, incident
readiness, and an observation window must be added.

### Composite toolkit

`metaskillpack` demonstrates a safe way to assemble specialists under one
explicit command: the root router stays thin, donors are read-only, versions
and hashes are fixed, and upgrades build a staged candidate. For an agent
portfolio, the approach can later be implemented as `agentkit`, but only after
stable independent donor skills exist. An early monolithic `agentpack` would
lock in poor boundaries.

## What Requires Adaptation

| Skill-specific assumption | Agent-specific replacement |
|---|---|
| Trigger/description determines discovery | Route + identity + capability registry + policy |
| Bundle files are the primary state | Definition is immutable; runtime state is separate |
| Host validation | Simulation, trace, sandbox, and production-like verification |
| Install/enable | Register → approve → shadow → canary → activate |
| Script permissions | Agent/tool/IAM permission envelope and credential lifetime |
| Routing eval | Routing + delegation + handoff + fallback evals |
| Behavior case | Multi-step outcome, variance, budget, and recovery case |
| Skill conflict | Capability overlap, write-set, shared state, and authority conflict |
| Version update | Definition/model/tool/policy/memory compatibility migration |
| Retirement files | Revoke routes/credentials, drain runs, migrate memory, archive evidence |

### New mandatory agent artifacts

An agent-oriented skill must be able to work with at least the following
contracts:

- agent card: identity, owner, mission, users, non-goals, risk tier;
- input/output and handoff schemas;
- tools, permissions, data classes, network and secret policy;
- state/memory model, provenance, retention, and deletion;
- runtime loop, budgets, stop, escalation, and human oversight;
- deployment topology, model/runtime compatibility;
- eval plan, traces, baselines, and release thresholds;
- SLOs, telemetry, runbook, incident/rollback/kill switch;
- lifecycle state, dependencies, replacement, and retirement plan.

## Recommended Skill Portfolio for Agents

### First wave

| Skill | Primary archetype | Responsibility |
|---|---|---|
| `agent-architect` | Workflow + evaluation profile | Contract, pattern, boundary, risk, and candidate definition |
| `agent-evaluator` | Evaluation/review | Offline, simulation, delegation, safety, resilience, and release evidence |
| `agent-doctor` | Diagnostic workflow | Symptom → trace → root cause → minimal repair → recovery proof |
| `agent-manager` | Tool/workflow integration | Inventory, registry, versions, rollout, state, and retirement |
| `agent-builder` | Orchestration/composition | End-to-end scenarios and bounded specialist handoffs |

### Second wave

| Skill | When it is justified |
|---|---|
| `agent-scout` | A portfolio exists and a systematic worth/duplication gate is needed |
| `agent-context` | Agent design regularly requires repository/domain/trace research |
| `agent-optimizer` | Healthy agents, baselines, and measurable cost/latency/quality targets exist |
| `agent-refactor` | Merge/split/extract/topology migrations have emerged |
| `agent-best-practices` | An updatable evidence corpus is needed separately from static docs |

### Third wave

- `agentkit` — an explicit composite of version-locked donors;
- `agent-registry-manager` — only if the registry/platform separates from the
  general `agent-manager`;
- `agent-os-manager` — only with a real multi-tenant runtime and SRE ownership;
- platform adapters for Codex, Claude Code, Cursor, MCP/A2A — after a
  canonical platform-neutral contract exists.

### What should not become a separate skill immediately

- `subagent-creator`: a subagent is a deployment/coordination role, not a
  separate lifecycle product;
- `agent-team-creator`: a separate creator is unnecessary; team topology
  belongs to the existing `agent-team-architect`, while lifecycle belongs to
  `agent-team-manager`;
- a separate skill for every pattern: patterns are decision options, not products;
- one `agent-supervisor` that designs, runs, evaluates, and approves.

## Master Prompt Architecture

All prompts use the following composition:

```text
agent-skill-base.md + exactly one specialist master prompt
```

The base defines the skill-creation contract, authority, agent asset model,
resources, evals, and completion gates. The specialist prompt defines
domain-specific routes, artifacts, failure model, and anti-patterns. All
prompts must not be merged together: that would create a mega-skill and destroy
trigger precision.

The prompt map is in [prompts/README.md](prompts/README.md).

## Proposed Changes to Existing Metaskills

### `skill-architect`

Do not add `agent` as a new primary archetype. Add an optional reference
`agent-system-profile.md`, applied when the product of the created skill is
agent design or agent management. The profile should add agent card,
state/memory, tools/permissions, runtime cycle, observability, deployment, and
retirement checks.

### `skill-evaluator`

Add an agent-control evaluation profile:

- delegation/task-envelope and context isolation;
- partial failure, retry, timeout, cancellation, and stale result;
- tool authority, prompt injection, and credential boundaries;
- memory poisoning, provenance, and retention;
- budget/latency/cost, loop depth, and fallback;
- shadow/canary, SLOs, and recovery;
- team-level correlated error and independent-verifier tests.

This is an evaluation profile for a skill that works with agents; `skill-evaluator`
itself must not become an evaluator of runtime agents.

### `skill-builder`

Add the `create-agent-lifecycle-skill` scenario:
base prompt + selected agent-specialist prompt → `skill-architect` →
`skill-evaluator`. The scenario creates a skill for working with agents; it
does not deploy the agent itself without a separate request.

### `skill-scout`

Extend the decision taxonomy for agent opportunities:
`USE_CODE_OR_WORKFLOW`, `USE_EXISTING_AGENT`, `EXTEND_EXISTING_AGENT`,
`CREATE_AGENT_SKILL`, and `KEEP_HUMAN`. Check whether an agent is being
proposed where a script or existing workflow is sufficient.

### `skill-harvester`

Add harvest units: agent definitions/cards, `AGENTS.md`, tool schemas, handoff
contracts, traces, eval datasets, runbooks, policies, incident reports, and
registry manifests. Secrets, hidden reasoning, and production memory must not
enter the inbox.

### `skill-manager`

Do not expand it into runtime-agent management: that would violate the
capability boundary and permissions model. It may manage public and
agent-private agent-oriented skills, their visibility, registry parity, and
lifecycle, but not runtime agent instances. Runtime agents should be handled by
a separate `agent-manager`.

### `skill-best-practices`

Add the current `agent-best-practices` corpus as a declared derived/local
source, or keep it as a separate managed corpus. A separate corpus is
preferable because the update cadence and normative scope differ between the
skill format and Agent OS.

### Routing/coexistence

Add negative-trigger fixtures that distinguish:

- "optimize a skill that creates agents" → `skill-optimizer`;
- "optimize a runtime agent" → future `agent-optimizer`;
- "create a skill for evaluating agents" → `skill-architect` with the agent evaluator prompt;
- "evaluate this skill" → `skill-evaluator`;
- "evaluate this agent" → future `agent-evaluator`;
- "install an agent-oriented skill" → `skill-manager`;
- "activate an agent definition" → `agent-manager` with separate approval.

## Public/private capability optimization

The idea of storing single-agent skills and commands inside the agent directory
is reasonable as a **scope-minimization pattern**. It reduces the global
routing surface, collision risk, and the number of independently published
packages. However, folder nesting is not a security boundary: `private` means a
scoped loader and allowed consumers, not confidentiality.

Visibility should not be added as a primary archetype. After choosing the
mechanism, a placement profile is used:

1. inline rule for a tiny instruction;
2. private command for a narrow named action of one agent;
3. private skill for a reusable complex capability of one agent;
4. public skill for multiple independent consumers or an independent lifecycle;
5. tool/script or workflow if the skill abstraction is not the minimal one.

All skills are registered. A private entry contains the owner agent, allowed
consumers, canonical locator, and `agent_scoped` discoverability. The agent
definition receives a binding from the canonical map; the global loader does
not scan `.agents/definitions/*/skills`. Promotion/demotion is performed by
`skill-refactor` as a versioned consumer migration with evals and rollback.

The new executable prompts are in `docs/prompts/`:

- `agent-capability-placement.md`;
- `agent-private-skill.md`;
- `agent-private-command.md`;
- `agent-skill-visibility-migration.md`.

## Recommended rollout

1. Review this analysis and the prompt taxonomy.
2. Create `agent-architect` from the corresponding prompt.
3. Create an independent `agent-evaluator` and a frozen eval dataset.
4. Create `agent-manager` only after selecting registry/runtime contracts.
5. Add `agent-doctor`; then add `agent-optimizer` once baselines exist.
6. Assemble `agent-builder` after specialist handoffs stabilize.
7. Run routing collision tests across all `skill-*` skills.
8. Consider `agentkit` only after two stable release cycles.

## Success criterion

The approach is considered successfully transferred if the new agent-oriented
skill:

- has one coherent capability and a precise trigger;
- uses a shared base and one specialist prompt;
- creates or modifies an immutable agent candidate, not the active runtime directly;
- separates author, evaluator, approver, and operator;
- produces typed artifacts and reproducible evidence;
- passes negative routing, authority, failure, and lifecycle evals;
- supports rollback, deprecation, and retirement;
- does not duplicate an existing metaskill or turn the skill into an implicit
  autonomous agent.

## Continuation

A unified phased plan for project-local agent teams, registries, skill mapping,
model selection, docs/memory, and Agent OS is in
[AGENT-TEAM-AND-AGENT-OS-PLAN.md](AGENT-TEAM-AND-AGENT-OS-PLAN.md).
