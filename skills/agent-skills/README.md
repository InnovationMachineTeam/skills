# Individual-Agent Skills

Use these skills for one agent or subagent. Prefer one direct specialist for a
known phase, `agent-builder` for an inferred multi-stage workflow, and explicit
`agentkit` for the version-locked composite command surface.

## Lifecycle

```text
agent-scout -> agent-context -> agent-architect -> agent-evaluator
            -> agent-doctor/agent-optimizer/agent-refactor
            -> agent-evaluator -> agent-manager
```

Supporting capabilities include `agent-best-practices`,
`agent-model-selector`, `agent-knowledge-manager`, and `agent-skill-mapper`.

These skills do not design teams or Agentic OS. Route team work to
`agent-team-manager` and platform architecture to `agent-os-architect`.

Every created agent declares its document contract, model policy, capability
budget, public/private skills, evaluation evidence, and lifecycle state. See
[the individual-agent onboarding workflow](../../docs/ONBOARDING.md#the-individual-agent-workflow).
