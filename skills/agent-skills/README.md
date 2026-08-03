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

## Full command examples

These are illustrative commands; replace the example paths and acceptance
criteria with repository-backed inputs.

```text
/agent-builder Create and evaluate a private release-notes agent that reads merged pull requests, writes docs/releases/draft.md, and requires human approval before publication
```

Expected result: the minimum justified agent definition, its document and model
contracts, evaluation evidence, lifecycle state, and no automatic publication.

```text
/agent-doctor Diagnose why agents/release-notes routes ordinary changelog questions incorrectly, propose the smallest repair, and rerun its frozen routing cases
```

Expected result: an evidence-backed diagnosis, bounded repair when authorized,
and before/after regression results.

```text
/agent-optimizer Reduce the median latency of agents/release-notes by 20 percent without weakening approval, privacy, or output-quality gates
```

Expected result: a measured candidate improvement against a frozen baseline;
unverified savings remain explicitly unclaimed.

These skills do not design teams or Agentic OS. Route team work to
`agent-team-manager` and platform architecture to `agent-os-architect`.

Every created agent declares its document contract, model policy, capability
budget, public/private skills, evaluation evidence, and lifecycle state. See
[the individual-agent onboarding workflow](../../docs/ONBOARDING.md#the-individual-agent-workflow).
