# Sources: Patterns, Cycles, and the Operating Model

Checked: **2026-07-30**.

## Catalogs and Reference Architectures

### [Agent Design Pattern Catalogue](https://arxiv.org/abs/2405.10467)

An academic catalog of 18 architectural patterns for foundation-model agents.
It is most useful for its unified pattern-description template: context,
forces, solution, consequences, and relations, rather than as a mandatory
checklist.

### [Taxonomy of Architecture Options for Foundation Model-based Agents](https://arxiv.org/abs/2408.02920)

A taxonomy of design-time and run-time decisions and a decision model. It helps
distinguish architectural choices from a specific implementation or vendor
feature.

### [System-Theoretic Agentic Design Patterns](https://arxiv.org/abs/2601.19752)

Treats patterns as the interaction of five subsystems: reasoning/world model,
perception/grounding, action, learning/adaptation, and inter-agent
communication. It is used as an additional modern perspective; practical rules
are cross-checked against official runtime and security sources.

### [Responsible GenAI agent reference architecture](https://arxiv.org/abs/2311.13148)

A reference architecture for foundation-model agents with responsible AI
concerns. It is useful for separation of concerns and for linking technical
components to assurance.

## Core Agent/Workflow Patterns

### [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

Distinguishes workflows from autonomous agents; describes prompt chaining,
routing, parallelization, orchestrator-workers, and evaluator-optimizer. The
core principle is to start with minimally sufficient complexity and measure the
improvement.

### [OpenAI Agents SDK — Orchestrating multiple agents](https://openai.github.io/openai-agents-python/multi_agent/)

Distinguishes LLM-driven and code-driven orchestration, manager/agents-as-tools,
and handoffs. It provides practical forms for chains, loops, parallel
execution, and routing.

### [Microsoft Azure — AI agent design patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)

Describes the choice between single-agent and multi-agent patterns and
emphasizes that a multi-agent system inherits the failure modes of distributed
systems.

### [Microsoft — Multi-agent patterns](https://learn.microsoft.com/en-us/agents/architecture/multi-agent-patterns)

Practical topologies, communication, MCP/A2A, security, and human oversight.
Platform-specific details are not promoted to universal MUSTs without
adaptation.

### [Google ADK — Workflow agents](https://adk.dev/agents/workflow-agents/)

Deterministic sequential, parallel, and loop workflows, as well as the boundary
between workflow and adaptive agent orchestration.

## Cycles

### [ASQ — PDCA cycle](https://asq.org/quality-resources/pdca-cycle)

An official professional description of Plan-Do-Check-Act as a repeatable
method for change and continuous improvement. In agent systems it applies to
process and release improvement, not as a substitute for a runtime control
loop.

### [Air University — OODA loop](https://www.airuniversity.af.edu/AFCLC/News/Article-Display/Article/1777083/cultural-ksas-skill-development-using-the-ooda-loop/)

Observe-Orient-Decide-Act for decision-making in a changing environment. The
source emphasizes that orientation and early analysis cannot be mechanically
compressed for speed.

### [IBM — MAPE-K control loop](https://dominoweb.draco.res.ibm.com/reports/h-0219.pdf)

Monitor, Analyze, Plan, and Execute use shared Knowledge; the autonomic manager
is connected to the managed element through sensors/effectors. This is a basis
for self-management, reconciliation, and Agent OS operations.

### [Lean Startup principles](https://theleanstartup.com/principles)

Build-Measure-Learn tests hypotheses through a minimal product or experiment,
measures actual response, and leads to pivot/persevere decisions. It is useful
for discovering whether an agent/skill is needed and for validating value.

### [Chris Argyris — Double Loop Learning in Organizations](https://hbr.org/1977/09/double-loop-learning-in-organizations)

Distinguishes correcting actions within existing norms from revising the goals,
rules, and assumptions themselves. It applies to systemic recurring failures
and metric gaming; changing intent/policy remains a human responsibility.

### [ADLC](https://www.adlc.io/)

Intent, Generate, Validate, Govern, Deploy, and Observe are concurrent modes
for agentic delivery. It connects experimental generation, continuous
validation, human governance, deployment, and production learning.

## Risk, Delivery, and Operations

### [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)

Govern is a cross-cutting function; Map, Measure, and Manage are applied
iteratively throughout the lifecycle. It includes inventory, roles,
independent review, monitoring, and safe decommissioning; this is a risk
framework, not a sequential checklist.

### [DORA — Continuous delivery](https://dora.dev/capabilities/continuous-delivery/)

Links low-risk delivery to deployable state, test/deployment automation, small
batches, fast feedback, security, and observability. It is used for
release/eval loops and operational metrics for agents, skills, and workflows.

### [DORA — Continuous integration](https://dora.dev/capabilities/continuous-integration/)

Fast tests on every small change and immediate regression fixes. It supports
script/tool development and shortens the feedback cycle.

### [Google SRE — Monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/)

Latency, traffic, errors, and saturation are the system baseline; Agent OS adds
outcome, routing, tool, approval, safety, cost, and lifecycle signals.

## Protocols

### [Model Context Protocol](https://modelcontextprotocol.io/specification/latest)

Standardizes connecting tools/data/prompts. Discovery capability does not imply
permission; authorization, validation, and isolation remain the host's
responsibility.

### [A2A Protocol](https://a2a-protocol.org/latest/specification/)

Inter-agent discovery, tasks, messages, and artifacts for independent systems.
It is useful at organizational/runtime boundaries; local subagents do not need
to use a network protocol.

## Source Application Policy

1. A standard or current official documentation defines platform facts.
2. Official engineering guidance defines validated practical heuristics.
3. A peer-reviewed/preprint catalog provides pattern language and alternatives.
4. An implementation confirms feasibility, but does not turn a local choice
   into a MUST.
5. Every pattern must pass local risk assessment and evals.

If a source describes a trade-off, the document preserves the conditions for
selection. If sources conflict on runtime facts, the versioned specification
and verification of current behavior take priority.
