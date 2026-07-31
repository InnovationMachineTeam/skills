# Release 3.3.0 — stable agentkit 1.0.0

Release `3.3.0` publishes `agentkit@1.0.0` as one explicit, selectively
installable skill in the private `im-skills` marketplace.

The stable pack contains read-only, version- and hash-locked snapshots of ten
single-agent lifecycle donors. It exposes explicit specialist commands plus
`run`, `status`, `upgrade`, `route`, `help` and `e2e`. Direct `agent-*`, team and
Agentic OS requests remain owned by their specialist skills.

Promotion evidence:

- donor stability cycles `3.2.1` and `3.2.2` passed with unchanged hashes;
- three real semantic workflows passed without donor or active-state mutation;
- official structure, repository, marketplace, registry and package gates pass;
- upgrade, rollback and external holdout contracts are hash-frozen;
- first-release rollback returns to direct donor invocation; the executable
  rehearsal artifact is `docs/agents/evals/agentkit-1.0.0-rollback.json`.

This release registers and publishes repository source and generated packages.
It does not install or activate agentkit in a user host. Installation remains an
explicit separate command and host read-back is required before claiming active
state.
