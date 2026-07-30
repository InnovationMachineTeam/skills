# Agent assets and access evaluation

Use for an exact frozen agent definition plus registry, binding map and host
projections. Do not modify the candidate or activate an agent.

1. Bind the run to agent/asset IDs, versions, revisions, hashes, registry/map
   revisions, target hosts and adapter generator version.
2. Validate schemas, locator containment, definition↔registry↔map parity,
   duplicate/orphan references, SemVer/revision strategy and accountable owner.
3. Verify capability budget and that every declared capability has exactly one
   intended binding. A private capability must allow only its owner agent.
4. Prove owner use, another-agent denial, global non-discovery, missing-owner
   fail-closed behavior, stale hash/version rejection and adapter drift failure.
5. Rebuild Codex, Claude Code and Cursor projections. Record `native`,
   `generated` or `unsupported` per host and test the selected enforcement.
6. Confirm marketplace and global packages contain no private roots or embedded
   private content.
7. Test expected-revision conflicts and injected partial registry/map updates;
   last-known-good documents and generated views must remain consistent.
8. Report separate structure, access, portability, lifecycle and user-outcome
   verdicts with raw evidence and unsupported host cases.
