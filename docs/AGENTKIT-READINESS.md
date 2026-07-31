# Agentkit Readiness Gate

Status: **DEFERRED**

The `agentkit` composite prompt exists at
`docs/prompts/agentkit-composite-skill.md`, but no discoverable skill bundle or
catalog entry is allowed yet.

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

Release `3.2.0` is the initial donor release. Release `3.2.1` completed the
first post-donor stability cycle with unchanged donor hashes and all blocking
layers passing. The machine-readable evidence is in
`docs/agents/evals/individual-agent-stability-cycles.json`.

Current progress: **1/2 stable cycles**. The second cycle must be a distinct
later observation; it must not be manufactured by immediately repeating the
same validation. Real workflow observations and the pack-level upgrade,
rollback and holdout contracts also remain incomplete. Therefore no
`skills/agent-skills/agentkit/` bundle or catalog entry is allowed yet.

## Experimental candidate

A non-discoverable `agentkit@0.1.0` candidate exists at
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

Candidate evaluation `agentkit-candidate-0.1.0` passed structure, routing,
scripts/tools, authority, coexistence and lifecycle gates. Semantic behavior is
still `INCONCLUSIVE` because no fresh-context model run or real user workflow
has executed the donors through the candidate. The correct lifecycle decision
is therefore `KEEP_EXPERIMENTAL_CANDIDATE`.
