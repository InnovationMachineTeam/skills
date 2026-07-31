# Agentkit Readiness Gate

Status: **DEFERRED**

The `agentkit` composite prompt exists at
`docs/prompts/agentkit-composite-skill.md`, but no discoverable skill bundle or
catalog entry is allowed yet.

Creation requires all of the following:

1. all ten donors released independently;
2. two consecutive stable portfolio releases after the last donor enters;
3. no blocking routing, authority, documentation, recovery or lifecycle
   regressions in those releases;
4. versioned donor interfaces and reproducible tree hashes;
5. at least three real end-to-end workflows that benefit from one explicit
   entry point;
6. a frozen donor manifest, upgrade comparison, rollback and pack-level holdout;
7. explicit invocation that does not compete with direct specialist triggers.

Release 3.2.0 is the initial donor release and does not satisfy the gate. A
future review records stable release evidence here before creating
`skills/agent-skills/agentkit/`.
