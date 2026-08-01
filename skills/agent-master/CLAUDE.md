# Agent Master Category Instructions

`CLAUDE.md` and `AGENTS.md` at this level are a synchronized pair. Any change to
this file must be applied to `AGENTS.md` in the same directory, and any change
to `AGENTS.md` must be applied to this file. Keep the two files byte-identical.

- Keep `agent-master` the only globally discoverable entry point in this category.
- Keep process-orchestrator, role-agent, role-skill and skill-implementation
  architects package-private under `agent-master/private-skills/`.
- Ask the public-versus-private structure question before research or design
  unless the current request already answers it.
- Announce the resolved execution mode and preserve safety gates in every mode.
- Apply the minimum-system gate before choosing an Agent Harness or agents.
- Run the private factory in dependency order with bounded state, handoffs,
  retries, independent evidence and end-to-end verification.
- Do not expose package-private subskills through marketplace discovery, bind
  them to another consumer, copy public donors, widen authority, install,
  publish or activate by assumption.
- Require current source evidence for harness/framework decisions and preserve
  registry, generated-package and rollback parity for lifecycle claims.
