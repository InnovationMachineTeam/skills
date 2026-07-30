# Placement and registration profile

Apply this profile after `base.md` and exactly one primary archetype prompt. It
changes placement, discovery, registration, and access tests; it is not a new
skill archetype.

## Inputs

Resolve intended consumers, owner agent when private, target repository/runtime,
canonical public and private roots, registry/map paths, mutation authority, and
whether the request is creation, promotion, or demotion.

## Decision

Choose exactly one: `INLINE`, `PRIVATE_COMMAND`, `PRIVATE_SKILL`,
`PUBLIC_SKILL`, `TOOL_SCRIPT`, or `WORKFLOW`. Prefer the smallest form whose
resources, tests, lifecycle, and reuse justify its maintenance cost. Explain why
the next simpler form is insufficient.

## Private capability rules

- Place private skills under the owning agent's canonical `skills/` directory
  and private commands under its `commands/` directory.
- Require a stable owner-agent reference, one accountable human/team owner, and
  an allow-list containing only that owner agent.
- Keep private roots out of global discovery; pass only the current agent's
  approved root to the host adapter.
- Do not describe folder placement as secrecy or a complete security boundary.
- Give a private skill its own version and evaluation evidence; version the
  owner agent when behavior changes. Give a private command only a revision and
  hash; its `parent_version_ref` must equal the exact owner-agent version.

## Registration

Create or update a candidate in `docs/AGENT-ASSET-REGISTRY.json` containing
identity, kind, name, version strategy, revision, hash, locator, visibility,
scope, discoverability, technical owner, accountable owner, allowed consumers,
source/provenance, trust, lifecycle, and evidence. Update
`docs/AGENT-SKILLS-MAP.json` in the same revision-checked transaction. Validate
references and generated views before activation. On failure, roll back both
documents and their views; never leave an unregistered active asset or a
registry entry pointing to a missing asset.

## Evaluation

Test positive owner use, global non-discovery, unauthorized-agent denial,
missing-owner failure, registry/hash parity, host adapter behavior, explicit
invocation, trigger collisions, and rollback. Promotion/demotion also requires
consumer inventory, old/new coexistence, migration, and absence checks.

## Output

Return the placement decision, rationale, canonical paths, registry/map diff,
agent version impact, loader policy, validation evidence, and activation status.
