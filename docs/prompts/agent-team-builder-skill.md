# Master Prompt For The `agent-team-builder` Skill

Apply after [agent-skill-base.md](agent-skill-base.md). Create a skill that
materializes only the approved `agent-team-spec` in staging, then generates
project adapters. It does not change the architecture, choose new roles, or
activate the runtime.

## Build contract

1. Verify spec version/hash, approval, destination, host versions and write
   authority; reject stale or incomplete inputs.
2. Plan exact write-set and detect collisions with existing assets.
3. Create canonical agent definitions under `.agents/definitions/<agent>/`.
4. Place each capability according to approved decision: inline, owner-private
   command/skill, project public skill, tool or workflow.
5. Generate agent-specific Codex, Claude Code and Cursor projections only from
   canonical definitions and registry bindings.
6. Produce complete agent/map candidate entries with accountable owners,
   versions, revisions, hashes, provenance, trust and lifecycle.
7. Apply registry and map through one expected-revision transaction with
   validation and rollback.
8. Run structural, access-denial, adapter drift and representative forward
   tests. Hand immutable output to independent evaluator.

## Failure rules

Use staged writes and deterministic generators. On any failure leave active
state unchanged; retain a diagnostics bundle but no dangling registry entry.
Never package private assets into a marketplace, expand permissions, silently
substitute models, or overwrite handwritten host files.

## Output

Return spec→artifact traceability, files, registry/map revisions, generated
adapters, validations, unbuilt optional items and activation status.
