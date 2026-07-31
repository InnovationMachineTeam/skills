# Documentation Instructions

`CLAUDE.md` and `AGENTS.md` at this level are a synchronized pair. Any change to
this file must be applied to `AGENTS.md` in the same directory, and any change
to `AGENTS.md` must be applied to this file. Keep the two files byte-identical.

- `docs/` is human-reviewable project memory; code and canonical JSON remain
  authoritative for implemented and machine-readable state.
- Add a document branch only for a named artifact, owner, reviewer, and consumer.
- Record provenance, status, freshness, supersession, and review triggers.
- Label generated views and never edit them as canonical data.
- Verify links, paths, commands, versions, and state claims against the repo.
- Use `docs/decisions/architecture/` for ADRs by default.
- Use `docs/agents/` for agent specs, contexts, evals, operations, and changes.
- Keep raw evidence distinct from synthesis and deterministic fixtures distinct
  from real semantic workflow observations.
- Do not include credentials, sensitive payloads, private locators, or personal
  information without an explicit approved data contract.
