# Master Prompt For A Private Agent Command

Apply after the `PRIVATE_COMMAND` decision. A command is justified when one
agent gets a narrow named action/template, but the separate resources, scripts,
routing description, and release lifecycle of a full skill are not needed.

## Creation

Create `.agents/definitions/<agent-id>/commands/<command>.md` with purpose,
arguments, preconditions, allowed tools/effects, procedure, output contract,
failure/stop behavior, and examples. Register the command in the agent
definition and in `docs/AGENT-ASSET-REGISTRY.json` with technical owner,
accountable human/team owner, `revision`, hash, `visibility: private`, the
single allowed consumer, and `parent_version_ref` equal to the exact version of
the owner agent. The command does not receive its own SemVer. Update
`docs/AGENT-SKILLS-MAP.json` in the same revision-checked transaction.

The command must not:

- become globally discoverable;
- implicitly expand the agent's permissions;
- duplicate a complex reusable capability that needs a private skill;
- store credentials, durable state, or hidden side effects.

## Verification

Verify argument validation, owner invocation, unauthorized-agent denial,
global non-discovery, output/failure behavior, registry/hash parity, and
removal rollback. If the command grows into multiple workflows/resources/evals,
stop creation and return the `PRIVATE_SKILL` decision.
