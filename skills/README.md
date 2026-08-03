# Canonical Skills

`skills/` is the canonical source of truth. Generated packages under `plugin/`
and `plugins/` are projections and must not be edited directly.

| Category | Scope | Entry points |
|---|---|---|
| [agent-master](agent-master/README.md) | Agent Harness factory with package-private process, role, skill and implementation architects | `agent-master` |
| [agent-skills](agent-skills/README.md) | one agent or subagent | `agent-builder`, `agentkit` |
| [agent-team-skills](agent-team-skills/README.md) | team architecture, build, mapping, execution | `agent-team-manager` |
| [agent-os-skills](agent-os-skills/README.md) | durable platform planes | `agent-os-architect` |
| [metaskills](metaskills/README.md) | create, evaluate, optimize, and govern skills | `skill-builder`, `metaskillpack` |
| [prompt-skills](prompt-skills/README.md) | durable prompt design, reconstruction, optimization, and packaging | `prompt-optimize`, `prompt-master` |

## Full command examples

Choose the narrowest skill that owns the requested outcome. These examples are
illustrative and must be adapted to the current repository and authority.

```text
/agent-builder Create and evaluate a private accessibility-review agent for this repository, write its reports under docs/accessibility, and require human approval before publication
```

Expected result: a governed single-agent package with observable evaluation and
lifecycle evidence.

```text
/skill-builder Create a private skill that audits WYSIWYG-editor accessibility requirements and returns a verification-ready report template
```

Expected result: a versioned skill package with routing, behavior, boundaries,
documentation, and verification artifacts.

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
