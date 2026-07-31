# Agent context: agentkit release steward

## Question

Can one bounded agent prepare an agentkit release decision without receiving
publication authority or modifying the ten donor skills?

## Source inventory

| ID | Locator | Revision | Claims used |
|---|---|---|---|
| S1 | `docs/AGENTKIT-READINESS.md` | repository `f521574` | maturity conditions and current candidate state |
| S2 | `docs/agents/evals/individual-agent-stability-cycles.json` | repository `f521574` | donor hashes and cycle ledger |
| S3 | `candidates/agentkit/donors.json` | agentkit `0.2.0` worktree | exact donor interfaces and hashes |
| S4 | `scripts/validate_agent_donor_stability.py` | agentkit `0.2.0` worktree | fail-closed maturity checks |
| S5 | `catalog/release.json` | marketplace `3.2.1` | release identity and publisher roles |

All sources are repository-owned, private, read under the user's current
request, and contain no copied credentials or hidden reasoning.

## Verified constraints

- Donors are read-only and exact-hash locked.
- The agent may prepare evidence and a proposal, but cannot publish, install or
  activate.
- Deterministic scripts own hashes, generation and validators.
- `@stanislavus86` remains the required accountable reviewer.
- A failed blocking layer stops the release recommendation.

## Edge cases

- candidate and donor hashes drift between plan and run;
- generated packages pass while canonical registry state is stale;
- synthetic router fixtures are mislabeled as real workflows;
- rollback exists only as prose and cannot restore direct donor routing;
- a release proposal is mistaken for publication authority.

## Readiness

`READY` for an immutable evaluation-only agent definition. Current model names
remain host-policy references because this run has no authorized current-model
research phase.
