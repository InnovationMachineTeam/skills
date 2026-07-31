# Agentic OS private canary report

Status: `PASS`  
Executed: `2026-07-31T09:02:58Z`  
Marketplace: `im-skills` `1.8.0`  
Release commit: `3bbed19`  
Owner: `InnovationMachineTeam`  
Reviewer: `@stanislavus86`

## Scope

The canary covered the seven new individually installable Agentic OS plugins:

- `agent-observer@1.0.0`;
- `agent-os-architect@1.0.0`;
- `agent-os-bootstrapper@1.0.0`;
- `agent-os-evaluator@1.0.0`;
- `agent-policy-manager@1.0.0`;
- `agent-registry-manager@1.0.0`;
- `agent-runtime-manager@1.0.0`.

It did not activate production infrastructure, use production credentials or
publish the marketplace publicly.

## Evidence

| Gate | Result |
|---|---|
| Repository forward/adversarial suite | PASS, 36 tests |
| Official Agent Skills quick validator | PASS, 28/28 skills |
| Canonical registry, hashes and generated views | PASS |
| Marketplace inventory | PASS, 28 entries on each of three host manifests |
| Selective package integrity | PASS, 28 one-skill packages |
| Claude Code strict package validation | PASS, aggregate plus 28 individual packages |
| Codex private selective install | PASS, 7/7 installed and enabled at `1.0.0` |
| Codex delivered-tree comparison | PASS, 7/7 match canonical packages |
| Cursor package and marketplace structure | PASS |

Cursor evidence is structural because a native private marketplace install
path equivalent to the Codex canary is not available in the supported contract.
The repository retains a self-contained Cursor manifest for each skill and
blocks public release until the separate public-publication gate is approved.

## Collision and isolation result

The portfolio gate proved unique skill names, descriptions and catalog entries;
explicit non-trigger routes for every new Agentic OS skill; literal
`$skill-name` invocation in OpenAI interfaces; exact version/provenance/hash
registration; identical inventory across Claude Code, Codex and Cursor; and no
agent-private roots in any individual marketplace package.

## Rollback and ownership

Rollback is bounded to the seven exact `name@im-skills` installations: disable
or uninstall those identifiers, restore the marketplace clone to the previous
known-good commit `2721182`, and rerun repository plus installed-state checks.
No data or infrastructure migration is involved. `InnovationMachineTeam` owns
repository and release recovery; `@stanislavus86` reviews promotion or rollback.

## Verdict

`PASS_PRIVATE_CANARY`. Release `1.8.0` may remain available in the private
marketplace. Public publication remains a separate approval and security gate.
