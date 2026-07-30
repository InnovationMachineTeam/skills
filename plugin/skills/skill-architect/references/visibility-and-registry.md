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
4. Consider a public skill when an approved independent consumer exists and the
   contract has been generalized beyond the original agent. Promote only when
   independent ownership, release cadence, evaluation, and reuse value justify
   the larger public surface.
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
  "id": "asset://project/skill/check-changelog",
  "kind": "skill",
  "name": "check-changelog",
  "version": "1.0.0",
  "content_sha256": "sha256:...",
  "locator": ".agents/definitions/code-reviewer/skills/check-changelog",
  "visibility": "private",
  "scope": "agent",
  "discoverability": "agent_scoped",
  "owner_agent_ref": "asset://project/agent/code-reviewer",
  "allowed_consumers": ["asset://project/agent/code-reviewer"],
  "accountable_owner": "team-or-person",
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

Use `docs/AGENT-ASSET-REGISTRY.json` and `docs/AGENT-SKILLS-MAP.json` as the
canonical machine-readable pair. Apply their changes as one optimistic,
revision-checked transaction; regenerate Markdown views only after candidate
validation. Validate uniqueness, path containment, version/hash parity,
existing owner agent, accountable owner, allowed consumer references, and map
authorization. Reject a private entry without an owner, any private allow-list
member other than the owner, a public skill inside a private root, or a private
binding to another agent.

## Version coupling

A private skill keeps its own semantic version. Because it contributes directly
to its owner agent's behavior, update the agent definition too:

- patch for non-functional metadata only;
- minor for backward-compatible capability additions or behavior changes;
- major for removal, replacement, authority, permission, input/output, or
  compatibility changes.

A private command does not receive independent SemVer. It inherits the owning
agent version through `parent_version_ref` and carries its own positive
`revision` plus `content_sha256` for audit and drift detection.

## Promotion and demotion

Promote private to public only when an independent consumer is approved, the
contract no longer assumes the original agent, and independent ownership,
versioning, evals, and lifecycle are justified. A second consumer alone is
evidence for assessment, not automatic promotion. Inventory consumers, stage the
public candidate, migrate registry/map references, test coexistence and access,
then retire the private copy after rollback is proven.

Demote public to private only after proving there are no other consumers.
Migrate bindings before removing public discovery. Never move a folder and call
the migration complete without host discovery and consumer verification.
