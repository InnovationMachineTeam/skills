# Master Prompts For Agent Skill Creation

These prompts create **agent-oriented skills**: skills that design, research,
evaluate, diagnose, optimize, manage, or orchestrate agents. They are not
ready-made production agents and do not grant permission to activate an agent
at runtime.

Practical launch contexts for these prompts are in the
[Onboarding Guide](../ONBOARDING.md) and [worked use cases](../use-cases/README.md).
First choose the minimum sufficient operating unit and artifact graph, then the
prompt; do not create a role or skill only because a template exists for it.

## Composition Rule

Always use:

```text
agent-skill-base.md + exactly one specialist prompt
```

The base defines the shared skill-creation contract. The specialist prompt adds
the agent-domain procedure. Do not merge all prompts into one mega-prompt.

## Routing

| Desired skill | Prompt |
|---|---|
| Finds evidence-backed opportunities for agents | [agent-scout-skill.md](agent-scout-skill.md) |
| Gathers context from repositories, docs, and traces | [agent-context-skill.md](agent-context-skill.md) |
| Designs a single agent or subagent | [agent-architect-skill.md](agent-architect-skill.md) |
| Creates evals and release evidence | [agent-evaluator-skill.md](agent-evaluator-skill.md) |
| Diagnoses and minimally repairs | [agent-doctor-skill.md](agent-doctor-skill.md) |
| Improves a healthy agent against a metric | [agent-optimizer-skill.md](agent-optimizer-skill.md) |
| Changes boundaries and topology | [agent-refactor-skill.md](agent-refactor-skill.md) |
| Manages registry, rollout, and retirement | [agent-manager-skill.md](agent-manager-skill.md) |
| Orchestrates the full lifecycle | [agent-builder-skill.md](agent-builder-skill.md) |
| Maintains an evidence corpus of practices | [agent-best-practices-skill.md](agent-best-practices-skill.md) |
| Assembles an explicit composite toolkit | [agentkit-composite-skill.md](agentkit-composite-skill.md) |

## Team Lifecycle Prompts

These prompts are also applied after `agent-skill-base.md`:

| Desired skill | Prompt |
|---|---|
| Designs roles, topology, and the team contract | [agent-team-architect-skill.md](agent-team-architect-skill.md) |
| Manages lifecycle and specialist routes | [agent-team-manager-skill.md](agent-team-manager-skill.md) |
| Materializes the approved team spec | [agent-team-builder-skill.md](agent-team-builder-skill.md) |
| Executes the approved team task graph | [agent-team-orchestrator-skill.md](agent-team-orchestrator-skill.md) |
| Maps agents and skills | [agent-skill-mapper-skill.md](agent-skill-mapper-skill.md) |
| Selects current models for roles | [agent-model-selector-skill.md](agent-model-selector-skill.md) |
| Manages worktrees/workspaces | [agent-workspace-manager-skill.md](agent-workspace-manager-skill.md) |
| Manages docs/wiki/graph knowledge | [agent-knowledge-manager-skill.md](agent-knowledge-manager-skill.md) |

## Agentic OS prompts

For platform capability, use this composition:

```text
agent-skill-base.md + agent-os-base.md + exactly one Agentic OS specialist
```

| Plane/capability | Prompt |
|---|---|
| Architecture and ADRs | [agent-os-architect-skill.md](agent-os-architect-skill.md) |
| Walking skeleton bootstrap | [agent-os-bootstrapper-skill.md](agent-os-bootstrapper-skill.md) |
| Asset desired-state registry | [agent-registry-manager-skill.md](agent-registry-manager-skill.md) |
| Durable task/runtime lifecycle | [agent-runtime-manager-skill.md](agent-runtime-manager-skill.md) |
| Policy, approvals and credentials | [agent-policy-manager-skill.md](agent-policy-manager-skill.md) |
| Telemetry, SLO and incidents | [agent-observer-skill.md](agent-observer-skill.md) |
| Multi-model routing | [agent-model-router-skill.md](agent-model-router-skill.md) |
| MCP/A2A/host adapters | [agent-protocol-manager-skill.md](agent-protocol-manager-skill.md) |
| Independent platform evaluation | [agent-os-evaluator-skill.md](agent-os-evaluator-skill.md) |

The knowledge plane uses `agent-knowledge-manager-skill.md` with invariants from
`agent-os-base.md`; do not create a second duplicate knowledge skill without a separate
permission/state/SLO boundary.

## Placement overlays

Before creating a capability for a specific agent, run
[agent-capability-placement.md](agent-capability-placement.md). It selects
inline rule, private command, private skill, public skill, tool/script, or
workflow.

| Decision | Additional prompt |
|---|---|
| Private agent skill | [agent-private-skill.md](agent-private-skill.md) after base + primary archetype |
| Private agent command | [agent-private-command.md](agent-private-command.md) |
| Promotion/demotion | [agent-skill-visibility-migration.md](agent-skill-visibility-migration.md) via `skill-refactor` |

The visibility overlay is not a new primary archetype. `private` means
agent-scoped discovery/binding; it does not make files secret.

When a skill creates, changes, evaluates, or activates an agent definition,
add [agent-documentation-contract.md](agent-documentation-contract.md)
as a shared profile. It does not replace the specialist prompt.

## Input Envelope

Normalize the request before starting:

```yaml
skill_to_create: agent-architect
user_outcome: design safe tool-using agents
target_hosts: [codex, claude-code]
agent_assets: [agent_card, workflow, eval_plan]
sources: []
examples:
  positive: []
  negative: []
authority:
  write_project: true
  install: false
  publish: false
  runtime_activate: false
constraints: []
destination: path/to/reviewable/bundle
```

If `user_outcome`, the target, or the destination is materially ambiguous, ask
one to three questions. For all other gaps, use safe assumptions.

## How To Apply

1. Fully read [agent-skill-base.md](agent-skill-base.md).
2. Choose one specialist prompt by observable outcome.
3. Pass in user input, source artifacts, target-host rules, and approvals.
4. Execute the prompt rather than copying it into the final `SKILL.md`.
5. Hand the immutable candidate to an independent `skill-evaluator`.
6. Perform installation/publication/runtime activation as a separate lifecycle
   action after approval.

For a team use case, first form the outcome/artifact/capability/authority
graphs through `agent-team-architect`, then apply the placement prompt to each
capability. Owner-only procedures are created as private skills/commands inside
the agent; a public skill is created only when multi-consumer reuse is justified.
All created assets and bindings are included in the registry/map transaction candidate.

## Common Outputs

Each prompt must create or update a reviewable skill bundle and return:

- classification and capability boundary;
- positive, negative, and ambiguous triggers;
- created files/resources;
- schemas agent artifacts;
- validation and eval evidence;
- authority, security, and lifecycle risks;
- installation/publication status;
- the exact next handoff.

## Terminology

- **Agent definition** — immutable design/configuration candidate.
- **Agent instance/run** — a concrete runtime execution.
- **Agent-oriented skill** — a skill that works with definitions, runs,
  traces, the registry, or the lifecycle.
- **Agent OS** — platform control/execution/knowledge/assurance/operations layer.
- **Activation** — permission for the runtime to route real tasks to
  a specific agent version.
