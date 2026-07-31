# Release 3.1.0: companion skill dependencies

Status: `STAGED`

Owner: `InnovationMachineTeam`; reviewer: `@stanislavus86`.

## Outcome

- Keep one canonical required/recommended graph in
  `catalog/dependencies.json`.
- Auto-install required same-marketplace companions in Claude Code through its
  native `plugin.json → dependencies` contract.
- Use visible warnings, machine-readable package metadata and a dependency-first
  installer for Codex and other hosts without that contract.
- Block only the route owned by a missing required companion; never simulate an
  unavailable specialist.
- Keep individual packages single-skill and collision-free.

## Initial declarations

- `skill-builder`: nine required lifecycle specialists covering all advertised
  scenarios.
- `agent-team-manager`: five required route owners plus the optional
  `agent-workspace-manager` recommendation.

## Acceptance gates

1. Dependency graph validation rejects invalid identities, versions, duplicate
   edges, self-dependencies and required cycles.
2. Runtime references are generated and drift-checked.
3. Claude manifests contain native required dependencies; Codex and Cursor
   manifests contain no unsupported dependency field.
4. Affected package READMEs contain `DEPENDENCY WARNING` and install order.
5. Dependency CLI dry run, installed-state pass and simulated warning are tested.
6. Repository, official skill, local eval and strict host validation pass.
7. Published packages and installed Codex state match the canonical release.

## Rollback

Restore release `3.0.0` at commit `8f1a0c2`, refresh `im-skills`, reinstall the
previous versions of affected plugins, and rerun the `3.0.0` validation suite.
No external data or infrastructure is changed by this release.

## Cutover evidence

Pending publication and installed-state verification.
