# Agent and Orchestration Pattern Catalog

## How to read the catalog

A pattern is a repeatable solution to a problem in a specific context, not the
name of a framework or a universal recommendation. For each use, record:

- the problem and forces: quality, latency, cost, risk, parallelism;
- preconditions and applicability context;
- participants, the state owner, and authority boundaries;
- the main flow, stop conditions, and failure path;
- the evidence by which the pattern is judged useful;
- consequences: new failure modes, cost, and operational burden.

Patterns can be composed, but each additional loop and participant must address
a measurable risk. The academic catalog of agent patterns also recommends
describing solutions through context, forces, solution, and consequences
([Agent Design Pattern Catalogue](https://arxiv.org/abs/2405.10467)).

## Level 1. One call or one agent

| Pattern | When to apply | Contract | Primary risk |
|---|---|---|---|
| Structured generation | Output is consumed by a program | Schema + validation + repair/fail | Valid form with incorrect content |
| Retrieval-grounded response | External or changing facts are needed | Query -> evidence with provenance -> answer | Irrelevant or poisoned context |
| Tool-use loop | Actions are needed for the result | Decide -> call -> observe -> stop | Infinite loop or dangerous side effect |
| ReAct | The next step depends on observation | Reason -> act -> observe with a budget | Unnecessary reasoning exposure and drift |
| Plan-and-execute | The task is long, but decomposition is available in advance | Versioned plan + checkpoints | An outdated plan continues to execute |
| Generate-verify-repair | The error can be detected by formal checking | Candidate -> deterministic verifier -> bounded repair | "Repair" masks a flawed framing |
| Reflection | There is a clear rubric and self-correction is useful | Draft -> critique -> revision, max N | Self-confirmation and extra cost |
| Human checkpoint | The decision is irreversible or requires judgment | Evidence + options + consequences | Formal approval without understanding |
| Bounded autonomy | Limited local autonomy is acceptable | Scope + tools + budget + expiry + escalation | Silent expansion of authority |

### Sense-think-act

The minimal agent model is: receive an observation, choose a permitted action,
execute it, and evaluate the new state. It is useful as a runtime primitive,
but does not itself define strategy, memory, or governance. A terminal
condition and limits on steps, time, cost, and side effects MUST exist.

### Plan-and-execute

The planner builds a verifiable sequence or DAG, and the executor runs ready
nodes. Separate them when the plan must be checked before actions or when the
executor should have fewer rights. Replanning should be allowed only on
recorded drift, failed verification, or new evidence; plan changes should be
saved as events rather than overwriting history.

### Evaluator-optimizer

Producer and evaluator work against a rubric until reaching a threshold or the
budget. Criteria are defined before the first generation. For meaningful risk,
the evaluator SHOULD be independent by context, model, data, or at least
prompt; the producer's self-critique does not count as independent review. This
workflow is part of Anthropic's core patterns
([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)).

## Level 2. Delegation to subagents

### Task envelope

Each delegation contains `goal`, `context_refs`, `constraints`, `owned_scope`,
`forbidden_actions`, `deliverables`, `acceptance`, `budget`, and
`return_schema`. This is a transactional boundary: the executor returns a result
and evidence rather than unilaterally expanding the task.

### Context capsule

A subagent receives a minimal self-contained package: goal, necessary facts,
links to canonical artifacts, local rules, and known decisions. Do not copy the
entire conversation history: a large shared context increases coupling, cost,
and the chance of following stale instructions.

### Manager-as-tools

The main agent keeps ownership of the dialog and calls specialists as tools. It
fits cases that need a single voice, global policy, and synthesis. The manager
MUST validate responses, because successful completion of a call does not prove
the correctness of the result.

### Handoff

Control and the subsequent dialog are transferred to a specialist. This is
useful when the new agent must directly clarify the domain task. Route history,
maximum depth, ping-pong prevention, and a fallback owner are required. OpenAI
distinguishes `agents as tools` from handoffs precisely by who owns the
subsequent interaction
([Agents SDK](https://openai.github.io/openai-agents-python/multi_agent/)).

### Fork-join

The orchestrator launches independent subtasks in parallel and combines the
results. Before launch, check independence, write-set, and the shared
bottleneck. The join must handle partial failure, timeout, duplicates, and
incompatible conclusions.

Variants:

- **scatter-gather** - different sources or aspects, then normalization;
- **map-reduce** - the same operation over partitions, then associative
  reduction;
- **competing hypotheses** - independent explanations and attempts to falsify
  them;
- **candidate ensemble** - several solutions and a separate selector;
- **review army** - only relevant critics selected by a scope detector.

### Blackboard

Agents publish typed claims, evidence, and tasks into a shared durable store
instead of forwarding everything through free-form chat. A blackboard is useful
for investigations and long-lived teams, but it MUST have schema, ownership,
conflict policy, provenance, TTL, and compaction. A shared mutable prompt is
not a blackboard.

### Independent verifier

The executor creates the result; the verifier checks the outcome against the
original intent and direct evidence. For high risk, the verifier is read-only
and does not receive the executor's summary as its only source. If the verifier
fixes the result, the verifier role ends and a new gate is needed after the
fix.

### Hierarchical delegation

Managers delegate to trees of specialists when flat coordination is overloaded.
Limit depth, fan-out, and total budget; capability and permissions may only
narrow down the tree. Recursive delegation without a global task graph creates
duplication and loss of accountability.

## Level 3. Orchestrators

| Pattern | Solution | Preferred implementation |
|---|---|---|
| Router | Choose one capability by request type | Typed classifier + confidence + fallback |
| Supervisor | Assign steps and maintain the overall goal | LLM locally, code for budgets and gates |
| Pipeline | Stable sequence of transformations | Workflow-as-code |
| State machine | Explicit states and allowed transitions | Durable deterministic runtime |
| DAG scheduler | Dependencies and parallel waves | Code + leases + idempotency |
| Dynamic graph | The plan depends on observations | Limited LLM planner + validated graph |
| Policy-gated workflow | Side effects depend on risk | Deterministic policy decision/enforcement |
| Reconciliation controller | Reconcile desired and observed state | Periodic idempotent loop |

### Router

The routing contract includes the chosen route, confidence, decision features,
and fallback. Check false-positive triggers, overlapping routes, and behavior on
out-of-domain input. At low confidence, choose a safe general workflow or ask
for clarification rather than picking a random specialist.

### State machine and DAG

A state machine is better than a free-form LLM plan when the process is
repeatable and involves approval, money, production, or long waits. A DAG adds
parallelism and dependencies. The model MAY propose nodes, but the runtime
validates types, allowed edges, permissions, cycles, and resource limits before
execution.

### Reconciliation controller

The controller regularly compares desired state with observed state and plans
the smallest correction. It fits orphan tasks, stuck approvals, stale skill
installations, and configuration drift. The operation must be idempotent, and
destructive reconciliation should require a separate gate.

### Policy decision / enforcement split

The Policy Decision Point computes a decision from verifiable attributes; the
Policy Enforcement Point technically blocks a disallowed action. An LLM may
explain rules and classify context, but should not be the sole enforcement
mechanism.

## Level 4. Agent teams

### Lead + specialists

The lead owns the mission, task graph, and integration; specialists own
non-overlapping deliverables. This is the default team pattern. The lead should
not become a bottleneck: standardize status/evidence and allow direct peer
communication only for explicit interfaces.

### Cross-functional pod

A small team covers intent, domain, build, verification, and operations for one
bounded outcome. A pod is more effective than a functional "pool" when it can
finish a vertical slice without fine-grained outside coordination. This aligns
with DORA's loosely coupled teams practice
([DORA](https://dora.dev/capabilities/loosely-coupled-teams/)).

### Driver-navigator

The driver creates the artifact, while the navigator continuously checks
direction, risks, and the next step. Roles switch only at a checkpoint. The
pattern is useful for complex migration or debugging, but the navigator does
not replace an independent final review.

### Producer-critic / red-blue

The producer proposes a solution; the critic looks for refutations and misuse
cases. For security, the red team must not have production credentials; the blue
team owns mitigations, and an independent gate confirms residual risk.

### Debate / jury

Participants first form independent positions, then exchange evidence; a judge
applies a predefined rubric. Use this only if diversity of hypotheses improves
evals. A majority does not turn an unverified fact into truth.

### Contract-net / bidding

The orchestrator publishes a task envelope, suitable agents respond with
capability, cost, timeline, and confidence, and a policy chooses the executor.
This is useful in a heterogeneous environment and dangerous if self-reported
confidence is not calibrated.

### Choreography

Participants react to typed events without a central step-by-step conductor.
This reduces the central bottleneck but complicates the global picture,
ordering, and compensation. For a high-impact process, preserve an accountable
owner, a correlation ID, and an observable process projection.

## Security and reliability patterns

- **Least-privilege envelope** - temporary rights only for a specific task.
- **Write-set partitioning** - one active writer per file/resource/aggregate.
- **Sandbox per worker** - a process/container boundary for untrusted code.
- **Worktree per worker** - change isolation; not a security boundary.
- **Idempotency key** - redelivery does not duplicate a side effect.
- **Lease + heartbeat** - temporary ownership and orphan worker detection.
- **Circuit breaker** - stops calls to a degraded capability.
- **Bulkhead** - separate queues/budgets limit blast radius.
- **Backpressure** - intake slows before downstream collapses.
- **Retry budget** - bounded retries only for transient failure with jitter.
- **Dead-letter state** - an irreparable task is preserved with evidence.
- **Saga** - a long workflow has compensation for each committed step.
- **Checkpoint/resume** - durable state allows safe continuation after failure.
- **Canary/shadow** - a new version is compared on limited traffic.

## Anti-patterns

| Anti-pattern | Why it fails | Replacement |
|---|---|---|
| Recursive swarm | Unbounded cost, depth, and duplicate work | Bounded task graph |
| Chat as database | No schema, consistency, or replay | Durable state + event log |
| Shared mutable context | Stale reads and implicit conflicts | Versioned artifacts |
| Everyone can write everything | Merge conflicts and unclear ownership | Write-set + merge owner |
| Author is sole judge | Confirmation bias | Independent verifier |
| Infinite reflection | No new evidence | Bounded loop + external check |
| Routing by labels only | Overlap and prompt gaming | Evals + confidence + fallback |
| Deep handoff chain | Loss of intent and accountability | Route limit + accountable owner |
| Consensus as truth | Correlated errors | Source/evidence adjudication |
| LLM as policy engine | Non-deterministic enforcement | PDP/PEP split |

## Minimal pattern decision record

```yaml
pattern: fork-join-with-independent-verifier
problem: verify a release across four independent aspects
forces: [latency, independence, security]
participants: [orchestrator, qa, security, reliability, verifier]
state_owner: orchestrator
write_sets: none
stop_conditions: [all_terminal, deadline, budget_exhausted]
failure_policy: partial_results_then_escalate
evidence: eval/release-review-v3
consequences:
  positive: shorter_review_latency
```
