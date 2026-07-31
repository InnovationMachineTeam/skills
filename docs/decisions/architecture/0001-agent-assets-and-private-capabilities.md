# ADR 0001: Agent assets and private capabilities

- Status: Accepted
- Date: 2026-07-31
- Owners: InnovationMachineTeam
- Reviewer: @stanislavus86

## Context

Creating every reusable instruction as a globally discoverable skill increases
routing collisions, context pressure, packaging work and lifecycle overhead.
Keeping everything inline creates oversized agent prompts with weak ownership
and evaluation. We need a middle scope for capabilities owned by one agent.

## Decision

1. Use `docs/AGENT-ASSET-REGISTRY.json` as the canonical typed registry for
   agents, skills, commands, workflows and teams.
2. Use stable `asset://<scope>/<kind>/<name>` identities independent of paths.
3. Keep public project skills in `.agents/skills/` and repository marketplace
   skills in `skills/<category>/`.
4. Keep private skills in
   `.agents/definitions/<agent>/skills/<skill>/` and private commands in
   `.agents/definitions/<agent>/commands/`.
5. Treat private as agent-scoped discovery and binding, not confidentiality.
6. Require `owner_agent_ref`, `allowed_consumers` and `accountable_owner` for
   private assets. The accountable owner is a person or team, never only an
   agent.
7. Give private/public skills independent SemVer. Private commands inherit the
   owning agent version and use an integer revision plus content hash.
8. Keep `docs/AGENT-SKILLS-MAP.json` as the canonical capability binding map.
9. Exclude private roots from marketplace packages and global discovery.
10. Use host adapters. Native integration is optional; deny-by-default fallback
    is mandatory.

## Placement decision

Choose the first sufficient form: inline instruction, private command, private
skill, public skill, tool/script, workflow, existing asset, or reject.
Promotion is justified by independent consumers and a generalized contract,
not folder convenience. Demotion requires a complete consumer inventory.

## Consequences

- Registry/map/schema updates become part of every agent capability change.
- Host projections are generated artifacts and can differ while preserving one
  canonical contract.
- A runtime unable to enforce agent scope must embed the capability in the
  agent projection or report unsupported; it must not publish it globally.
- CI rejects missing assets, hash/version drift, unregistered public skills,
  unauthorized private bindings and generated-view drift.
