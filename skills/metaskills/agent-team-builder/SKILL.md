---
name: agent-team-builder
description: Materializes an approved, versioned agent-team specification into a staged `.agents` structure, canonical definitions, owner-private skills or commands, public capability candidates, host adapters, registry/map transactions and verification evidence. Use when a reviewed team design is ready to build, rebuild, migrate or dry-run. Requires an exact approved spec, destination and write authority. Do not redesign roles, substitute models or permissions, activate agents, create worktrees, publish private assets, or operate the team; route design changes to agent-team-architect and lifecycle execution to agent-team-manager.
metadata:
  version: "1.0.0"
---

# Build an Approved Agent Team

Translate one approved team specification into reviewable files without changing
its semantics. Build to staging first; activation is a separate decision.

## Gate the build

Require the exact spec ID, version and content hash, `approved` status,
destination, target hosts and versions, expected registry/map revisions, explicit
write authority and a clean rollback destination. Missing or stale inputs yield
`BLOCKED`, not inference.

Read [references/build-transaction-contract.md](references/build-transaction-contract.md)
and [references/host-projection-and-safety.md](references/host-projection-and-safety.md).

## Plan the exact write-set

Inventory existing files and classify collisions as absent, generated-compatible,
handwritten, stale or conflicting. Create a build manifest with every operation,
source spec path, resulting owner/visibility, adapter target and validation.

Canonical project agents belong under `.agents/definitions/<agent-id>/`. Put an
owner-private skill or command inside that agent's directory and declare exactly
one allowed consumer. Public capability candidates go to the repository's public
skill root and never contain private material.

Validate the manifest before writing:

```bash
python3 scripts/validate_build_manifest.py build-manifest.json
```

## Materialize into staging

Create canonical agent definitions and policy, private capabilities, generated
host adapters, registry/map candidate updates and evaluation fixtures in a
temporary or explicitly named staging root. Generated adapters project canonical
policy; they do not become an independent source of truth.

Never overwrite handwritten files or concurrent revision changes. Never create
worktrees, credentials, network policy, installations, activation or publication
unless an independently authorized workflow owns that side effect.

## Verify and promote atomically

Run structural/schema validation, reference and visibility checks, adapter drift
checks, private-boundary tests, routing/behavior evals and the approved smoke
tests. Compare staged output with the manifest. Present the diff and residual
risks for approval.

On approval, re-check revisions and apply the staged write-set as one recoverable
transaction. If any step fails, restore backups and report a partial-failure
artifact. Registration is not activation.

## Complete

Return `STAGED`, `APPLIED`, `NOOP`, `BLOCKED` or `ROLLED_BACK` with spec/hash,
destination, exact files, versions, registry/map revisions, validation evidence,
activation state and handoff to `agent-team-manager`.
