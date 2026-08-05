# Best Practices for Building Agent Systems

This catalog is a practical guide to designing agents, subagents,
orchestrators, agent teams, and Agent OS. It combines official guidance from
OpenAI, Anthropic, Claude Code, Cursor, Google ADK, A2A, MCP, and Microsoft
with patterns from Agent OS, BMAD, GSD Core, GSD Pi, gstack, Spec Kit, and
OpenSpec.

Research currency: **2026-07-30**. Constraints and numeric limits for specific
platforms should be rechecked through the links in the source files.

## Quick Route

1. Start with [01-foundations-and-selection.md](01-foundations-and-selection.md)
   to choose the minimally sufficient architecture.
2. Define the agent contract using
   [02-agent-design-and-contracts.md](02-agent-design-and-contracts.md).
3. If decomposition is needed, use
   [03-subagents-and-delegation.md](03-subagents-and-delegation.md) and
   [04-orchestration-and-agent-teams.md](04-orchestration-and-agent-teams.md).
4. For the platform layer, see
   [05-agent-os-reference-architecture.md](05-agent-os-reference-architecture.md).
5. For project documentation, see
   [07-documentation-as-operating-system.md](07-documentation-as-operating-system.md)
   and [08-docs-catalog-and-templates.md](08-docs-catalog-and-templates.md).
6. Roles and processes are covered in
   [09-agent-role-catalog.md](09-agent-role-catalog.md) and
   [10-lifecycle-and-orchestration-processes.md](10-lifecycle-and-orchestration-processes.md).
7. Requirements, observability, security, and evals are covered in files 11-14.
8. Practical implementations and resolved conflicts are covered in files 15-16.
9. For deeper design work, use the agent, Agent OS, and skills pattern catalogs
   in files 17-19.
10. Cycles, lifecycle, role separation, and the operating model are covered in
    files 20-22.

## Core Principle

> Use the least complex architecture that consistently achieves the required
> quality, security, and execution time.

Escalation order:

```text
deterministic code
  → single model call
  → workflow of calls
  → single agent with tools
  → manager + subagents
  → agent team
  → distributed Agent OS
```

Advancing to the next level is justified only by measurable gains in evals or
by the need to separate context, tools, permissions, ownership, or parallel
work. More agents mean more latency, cost, failure modes, and attack surface.

## Normative Terms

- **MUST** — mandatory rule; violating it makes the system unsafe or unreliable.
- **SHOULD** — recommended rule; deviations must be documented.
- **MAY** — permitted option.
- **Platform rule** — a fact of a specific runtime, not a universal practice.
  Such rules are moved into adapters or labeled with the platform name.

## File Map

| File | Purpose |
|---|---|
| `01-foundations-and-selection.md` | Terms, selection criteria, and the complexity ladder |
| `02-agent-design-and-contracts.md` | Contract, instructions, tools, outputs, and errors |
| `03-subagents-and-delegation.md` | Task boundaries, handoff, context, and file ownership |
| `04-orchestration-and-agent-teams.md` | Topologies, parallelism, teams, and workflow-as-code |
| `05-agent-os-reference-architecture.md` | Control plane, execution plane, state, policy, and registry |
| `06-context-memory-and-state.md` | Context, long-term memory, and recovery |
| `07-documentation-as-operating-system.md` | `docs/` as shared memory for people and agents |
| `08-docs-catalog-and-templates.md` | Document variants, directory tree, and minimal templates |
| `09-agent-role-catalog.md` | Common PDLC/SDLC/ADLC/Discovery/Delivery agents |
| `10-lifecycle-and-orchestration-processes.md` | Scenarios from discovery to operations |
| `11-requirements-and-quality-attributes.md` | FR, quality attributes, constraints, and traceability |
| `12-task-tracking-monitoring-and-observability.md` | Task states, events, metrics, and dashboards |
| `13-security-approvals-and-governance.md` | Least privilege, approvals, isolation, and supply chain |
| `14-evaluation-and-continuous-improvement.md` | Evals for agents, teams, routing, and production |
| `15-implementation-case-studies.md` | Comparison of seven studied repositories |
| `16-conflicts-and-resolutions.md` | Practice conflicts and adopted resolutions |
| `17-agent-and-orchestration-pattern-catalog.md` | Patterns for a single agent, delegation, orchestrators, and teams |
| `18-agent-os-and-runtime-pattern-catalog.md` | Control/execution/knowledge/assurance/operations patterns for Agent OS |
| `19-skill-design-pattern-catalog.md` | Atomic, composite, adapter, script, eval, and lifecycle patterns for skills |
| `20-agentic-cycles-and-lifecycles.md` | ReAct, OODA, MAPE-K, PDCA, ADLC, and lifecycle assets |
| `21-role-patterns-and-separation-of-duties.md` | Role archetypes, accountability, and separation of duties |
| `22-operating-model-and-pattern-selection.md` | Selection model, recipes, risk tiers, and maturity |
| `sources-platforms.md` | Platform and protocol sources |
| `sources-frameworks.md` | Repositories and practical implementations |
| `sources-standards-and-docs.md` | Standards, security, and documentation |
| `sources-patterns-and-cycles.md` | Pattern catalogs, cycles, and operating sources |

## What This Catalog Does Not Claim

- Multi-agent design is not a goal in itself.
- A worktree isolates changes, but it is not a full security boundary.
- LLM review does not replace automated checks and a responsible human.
- Memory is not a source of truth without provenance, lifetime, and validation.
- A document without an owner, update trigger, and consumer quickly becomes
  noise.
