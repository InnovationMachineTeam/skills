# Individual-Agent Skill Instructions

`CLAUDE.md` and `AGENTS.md` at this level are a synchronized pair. Any change to
this file must be applied to `AGENTS.md` in the same directory, and any change
to `AGENTS.md` must be applied to this file. Keep the two files byte-identical.

- Scope each specialist to one individual-agent lifecycle responsibility.
- Prefer a direct specialist for one phase, `agent-builder` for an inferred
  multi-stage workflow, and explicit `agentkit` only when invoked.
- Do not absorb team design/execution or Agentic OS responsibilities.
- Every created agent declares mission, non-goals, permissions, model policy,
  document contract, capability budget, evaluation, and lifecycle state.
- Create owner-private skills/commands with the agent unless multiple consumers
  justify a public skill.
- Preserve independent frozen evaluation and explicit approval before mutation,
  activation, publication, or deployment.
