# Master Prompt For A Private Agent Skill

Apply after `agent-skill-base.md`, one primary archetype prompt, and the
`PRIVATE_SKILL` decision from `agent-capability-placement.md`.

## Contract

Create a normal versioned/tested skill bundle, but place it in
`.agents/definitions/<agent-id>/skills/<skill>/`. Require a stable owner agent,
allowed consumers, target host adapter, and candidate registry/map update.
Do not embed secrets or runtime state.

## Registration

The entry contains identity, name, semantic version, content hash, locator,
`visibility: private`, `scope: agent`, `discoverability: agent_scoped`,
`owner_agent_ref`, `allowed_consumers`, provenance, trust, lifecycle, and evidence.
`allowed_consumers` contains only the owner agent; separately specify the
accountable human/team owner. The agent definition references the skill through
the canonical map. Registry and map are updated in one revision-checked
transaction with rollback. A behavior-changing skill update increments the
agent version according to the compatibility policy.

## Loader and tests

Global discovery excludes `.agents/definitions/*/skills`. The host adapter gets
the private root only after selecting an approved agent identity. Verify:

- explicit owner invocation and intended trigger;
- absence from global discovery;
- denial for another agent and missing owner;
- registry/map path/version/hash parity;
- prompt injection, permissions, and resource boundaries;
- rollback and stale adapter detection.

## Completion

Return the bundle, owner-agent diff, registry/map diff, generated adapters,
validation/eval evidence, and lifecycle status. Do not call the capability
secret and do not activate it merely by creating files.
