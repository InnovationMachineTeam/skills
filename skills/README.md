# Canonical Skills

`skills/` is the canonical source of truth. Generated packages under `plugin/`
and `plugins/` are projections and must not be edited directly.

| Category | Scope | Entry points |
|---|---|---|
| `agent-master/` | Agent Harness factory with package-private process, role, skill and implementation architects | `agent-master` |
| [agent-skills](agent-skills/README.md) | one agent or subagent | `agent-builder`, `agentkit` |
| [agent-team-skills](agent-team-skills/README.md) | team architecture, build, mapping, execution | `agent-team-manager` |
| [agent-os-skills](agent-os-skills/README.md) | durable platform planes | `agent-os-architect` |
| `metaskills/` | create, evaluate, optimize, and govern skills | `skill-builder`, `metaskillpack` |
| `prompts/` | reconstruct, generalize, merge, decompose, and package complex prompts | `prompt-master` |
| `prompt-skills/` | durable prompt design and optimization | `prompt-optimize` |

## Capability placement

- keep a tiny stable rule inline in its owning agent;
- use a private command for a thin owner-only procedure;
- use a private skill for a substantial capability with one consumer;
- create a public skill here only when several agents or projects need the same
  governed contract.

All installed skill contents are versioned. Changing a skill directory requires
a SemVer decision, evaluation updates, generated-package rebuild, and registry/
catalog review.

See the [Onboarding Guide](../docs/ONBOARDING.md) for workflows and concrete
examples.
