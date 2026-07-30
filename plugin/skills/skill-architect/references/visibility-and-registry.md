# Visibility, placement, and registry

## Two independent classifications

Classify mechanism and deployment scope independently. Knowledge, workflow,
tool, script, artifact, evaluator, orchestrator, and router are primary
archetypes. `public` and `private` are visibility profiles applied after the
archetype is chosen.

`private` means agent-scoped discoverability and binding. It does not mean
encrypted, secret, or unreadable to a process that already has filesystem
access. Enforce confidentiality with repository permissions, sandboxing,
separate credentials, and runtime policy.

## Placement gate

Choose the least costly durable form:

1. Keep a tiny stable rule inline in the agent prompt when it has no reusable
   resources, tests, or independent lifecycle.
2. Use a private command for one agent's narrow named action or output template.
3. Use a private skill for one agent's reusable capability that needs routing,
   references, scripts, evals, or its own version.
4. Use a public skill when there are at least two independent consumers, or the
   capability has an owner, release cadence, contract, and value independent of
   one agent.
5. Use a deterministic tool/script when exact transformation is the hard part.
6. Use a workflow when durable multi-stage state, coordination, or recovery is
   the hard part.

Do not create a skill solely to shorten an agent prompt. Context savings must be
balanced against discovery cost, maintenance, evaluation, and version drift.

## Canonical layout

```text
skills/<category>/<skill>/SKILL.md                  # repository public
.agents/skills/<skill>/SKILL.md                     # project public
.agents/definitions/<agent-id>/skills/<skill>/SKILL.md
.agents/definitions/<agent-id>/commands/<command>.md
```

The last two paths are private to the named agent. Host-specific files are
generated adapters. A global loader must never recursively scan
`.agents/definitions/*/skills`; it receives public roots plus only the selected
agent's approved private root.

## Registry contract

Register every skill, including private ones. A registry entry should contain:

```json
{
  "id": "skill://project/code-reviewer/check-changelog",
  "name": "check-changelog",
  "version": "1.0.0",
  "content_sha256": "sha256:...",
  "locator": ".agents/definitions/code-reviewer/skills/check-changelog",
  "visibility": "private",
  "scope": "agent",
  "discoverability": "agent_scoped",
  "owner_agent_ref": "agent://project/code-reviewer",
  "allowed_consumers": ["agent://project/code-reviewer"],
  "source_type": "project",
  "provenance": {},
  "trust_status": "unreviewed",
  "lifecycle_status": "candidate"
}
```

Public entries use `visibility: public`, a repository or project scope,
`discoverability: global` or `project`, and no owner-agent requirement. The map
remains the canonical binding source. Registry presence does not imply trust,
activation, or runtime availability.

Validate uniqueness, path containment, version/hash parity, existing owner
agent, allowed consumer references, and map authorization. Reject a private
entry without an owner, a public entry inside a private root, or a private
binding to an unlisted agent.

## Version coupling

A private skill keeps its own semantic version. Because it contributes directly
to its owner agent's behavior, update the agent definition too:

- patch for non-functional metadata only;
- minor for backward-compatible capability additions or behavior changes;
- major for removal, replacement, authority, permission, input/output, or
  compatibility changes.

## Promotion and demotion

Promote private to public when a second independent consumer is approved, the
contract no longer assumes the original agent, and independent ownership,
versioning, evals, and lifecycle are justified. Inventory consumers, stage the
public candidate, migrate registry/map references, test coexistence and access,
then retire the private copy after rollback is proven.

Demote public to private only after proving there are no other consumers.
Migrate bindings before removing public discovery. Never move a folder and call
the migration complete without host discovery and consumer verification.
