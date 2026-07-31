# Release 3.1.0: companion skill dependencies

Status: `CUTOVER`

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

Executed at `2026-07-31T10:34:29Z` from release commit `c2f0f53`.

- Dependency graph and generated-reference checks passed for two dependent
  orchestrators and all 28 catalog skills.
- Repository suite: 43/43 tests passed, including simulated missing/outdated
  companion warnings.
- Official Agent Skills validator: 28/28 passed.
- Skill-local eval validators: 19/19 passed.
- Claude Code strict validation: aggregate plus 28/28 individual packages;
  both affected plugins passed native dependency schema validation.
- Official Codex plugin validator: aggregate plus 28/28 individual packages.
- Skills CLI discovered 28/28 canonical skills.
- Dependency-aware Codex installation completed for `skill-builder@1.4.0`
  with nine required companions and `agent-team-manager@1.2.0` with five
  required plus one explicitly requested recommended companion.
- `metaskillpack@1.4.0` and `skill-marketplace-manager@1.3.0` are current.
- Codex installed state: 28/28 `im-skills` plugins enabled; both dependency
  checks pass.
- Delivery integrity: all 28 package trees match the Git-backed Codex
  marketplace snapshot.

Claude auto-install was schema-validated but not used to mutate the user's
Claude installation. The previous release remains recoverable through the
rollback procedure.
