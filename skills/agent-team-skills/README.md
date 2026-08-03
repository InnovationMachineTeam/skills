# Agent-Team Skills

Use these skills when separate context, expertise, permissions, models,
write-sets, or independent verification justify multiple agents.

| Skill | Responsibility |
|---|---|
| `agent-team-manager` | lifecycle facade and durable state |
| `agent-team-architect` | smallest justified roles, topology, interactions, and spec |
| `agent-team-builder` | stage an approved exact specification |
| `agent-team-orchestrator` | execute an approved bounded task graph |
| `agent-workspace-manager` | govern isolated worktrees and integration handoffs |

## Full command examples

These examples assume the referenced specifications exist and are approved.

```text
/agent-team-manager Design and stage a private documentation team for this repository with separate research, writing, and independent verification responsibilities
```

Expected result: a resumable lifecycle plan that delegates architecture and
build phases while preserving approval and activation gates.

```text
/agent-team-builder Materialize the approved team specification at docs/teams/documentation-team.json into staging without activating the team
```

Expected result: exact staged agent and binding artifacts, validation evidence,
and a clear activation handoff rather than a running team.

```text
/agent-team-orchestrator Execute the approved documentation-team run plan at docs/teams/runs/onboarding-refresh.json and stop if independent verification fails
```

Expected result: bounded task execution with recorded handoffs, verified
artifacts, failure state, and no redesign of the frozen team.

Model selection and skill mapping remain owned by `agent-model-selector` and
`agent-skill-mapper`. Team build does not imply activation, and orchestration
cannot redesign the team.

Start with [the agent-team workflow](../../docs/ONBOARDING.md#the-agent-team-workflow)
and review the [worked use cases](../../docs/use-cases/README.md).
