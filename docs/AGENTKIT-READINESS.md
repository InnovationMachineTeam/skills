# Agentkit Readiness Gate

Status: **READY FOR STABLE PROMOTION**

The `agentkit` composite prompt exists at
`docs/prompts/agentkit-composite-skill.md`. Release `3.2.2` completes the
maturity gate; a discoverable bundle still requires a separate exact package
promotion and validation transaction.

Creation requires all of the following:

1. all ten donors released independently;
2. two consecutive stable portfolio releases after the last donor enters;
3. no blocking routing, authority, documentation, recovery or lifecycle
   regressions in those releases;
4. versioned donor interfaces and reproducible tree hashes;
5. at least three real end-to-end workflows that benefit from one explicit
   entry point;
6. a frozen donor manifest, upgrade comparison, rollback and pack-level holdout;
7. explicit invocation that does not compete with direct specialist triggers.

Release `3.2.0` is the initial donor release. Releases `3.2.1` and `3.2.2`
completed two post-donor stability cycles with unchanged donor hashes and all
blocking layers passing. The machine-readable evidence is in
`docs/agents/evals/individual-agent-stability-cycles.json`.

Current progress: **2/2 stable cycles and 3/3 real workflows**. Cycle 2 is tied
to a later timestamp, unchanged donor hashes, new E2E artifacts and release
`3.2.2`; it is not a repeated copy of cycle 1. Upgrade, rollback and external
pack holdout contracts are hash-frozen. The maturity gate is ready, but
`skills/agent-skills/agentkit/` remains absent until the next release performs
and verifies the promotion.

## Experimental candidate

A non-discoverable `agentkit@0.2.0` candidate exists at
`candidates/agentkit/`. It is excluded from `skills/`, all marketplaces,
generated plugins and host activation. Its purpose is to collect the missing
E2E evidence without bypassing the maturity gate.

The explicit `agentkit e2e` command scaffolds E2E cases, runs selected commands
through the candidate router, records raw evidence, classifies ownership and
proposes improvements. A donor-owned finding requires exact user approval
before the candidate may write an improvement prompt or dispatch a staged
`repair-and-improve` or `optimize-existing` process. Canonical and vendored
donors remain read-only, and promotion remains a separate lifecycle decision.

Synthetic candidate tests do not count toward the required three real workflow
observations.

Candidate evaluation `agentkit-candidate-0.2.0` passes all blocking layers.
Three user-authorized semantic workflows exercised full lifecycle,
repair/recovery and optimize/regression routes and retained artifact hashes.
They used the current task executor rather than an external model, so no
cross-model generalization claim is made. The correct lifecycle decision is
`PROMOTE_AFTER_STABILITY_CYCLE_2`, followed by exact stable-package evaluation.
