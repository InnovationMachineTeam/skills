---
name: agent-model-selector
description: Selects and audits evidence-backed model policies for agents, subagents, evaluators, orchestrators, and team routes. Use when a user asks which current model best fits an agent role, wants a quality/latency/cost comparison, needs a fallback or escalation ladder, or must revisit a stale model assignment. Fetch current authoritative model and host documentation before recommending exact models, bind claims to evidence and checked dates, and separate design-time selection from runtime routing. Do not configure providers, buy access, activate agents, benchmark without execution authority, or claim one universally best model.
metadata:
  version: "1.0.2"
---

# Select Agent Models

Create the smallest versioned model policy that clears each role's quality and
safety floor at acceptable latency and cost. Treat exact model availability and
capabilities as current facts that require authoritative verification.

## Establish the decision

Resolve:

- exact roles or routes, task classes, risk tier, tools, modalities, context and
  structured-output needs;
- target hosts, providers, regions, data controls and models already available;
- quality floor, latency/throughput ceiling, cost budget and evaluation corpus;
- whether the request is recommendation, benchmark design, benchmark execution,
  policy audit or migration;
- authority for network research, model calls, data disclosure and spend.

Ask only when a missing constraint changes the candidate set, data boundary or
acceptance gate. Default to a read-only recommendation plan.

## Verify current candidates

Read [references/selection-contract.md](references/selection-contract.md).
Fetch current official provider and host documentation. Record URL, checked
date, model identifier/version, availability and every capability claim used.
Do not infer availability from a model name, marketing tier or training memory.

Reject candidates that fail required tools, modality, context, regional, data,
policy or host constraints before comparing quality. Keep the candidate set
small and explain exclusions.

## Evaluate and decide

Read [references/evidence-and-benchmarking.md](references/evidence-and-benchmarking.md).

1. Freeze representative, adversarial and failure cases before candidate runs.
2. Keep prompts, tools, data, budgets and graders comparable.
3. Measure task success and applicable safety, tool reliability, latency,
   tokens, cost and variance. Label estimates separately from observations.
4. Choose the fastest or least expensive candidate that clears every blocking
   gate. Escalate on uncertainty or consequence, not prestige.
5. Reduce correlated failure between producer and independent evaluator where
   practical.
6. Define exact fallback order, retry/escalation conditions, degraded mode,
   provider outage behavior and hard stop.
7. Define pinning, migration compatibility and re-evaluation triggers.

When execution is unauthorized or representative data is unavailable, return
`RESEARCH_REQUIRED` or `INCONCLUSIVE`, not a fabricated ranking.

## Produce and validate policy

Create a policy matching [references/selection-contract.md](references/selection-contract.md)
and validate it:

```bash
python3 scripts/validate_model_policy.py model-policy.json
```

Use `RECOMMEND`, `CONDITIONAL`, `RESEARCH_REQUIRED`, `INCONCLUSIVE` or `REJECT`
per role. Report exact evidence, measurements, unknowns and next review date.

## Boundaries

- Runtime per-request routing belongs to `agent-model-router` or the host.
- Team topology belongs to `agent-team-architect`.
- Independent execution evidence belongs to an evaluator with a frozen plan.
- Provider configuration, credentials, purchase and rollout require separate
  authority.
- Do not send proprietary or personal fixtures to an external provider without
  explicit data-handling approval.

## Complete

Return policy identity/version, candidate and exclusion table, role decisions,
fallback/escalation ladder, benchmark evidence, sources and checked dates,
residual risk, re-evaluation triggers and configuration status.
