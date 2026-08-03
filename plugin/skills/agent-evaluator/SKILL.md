---
name: agent-evaluator
description: Independently designs, writes, audits, runs and compares evaluations for one frozen agent or subagent definition and its bounded runtime behavior. Use for routing, outcome, tool, permission, delegation, state, memory, documentation, resilience, cost, latency, lifecycle or release evidence for an individual agent. Do not evaluate an entire team or Agentic OS, repair or optimize the candidate during a frozen run, reveal holdout answers, activate agents, or average away blocking failures; use agent-team workflows or agent-os-evaluator for broader systems.
metadata:
  version: "1.0.2"
---

# Evaluate One Frozen Agent

Keep evaluation logically independent from authoring, diagnosis, optimization
and release authority. Freeze candidate hash, definition version, environment,
fixtures, graders and acceptance gates before observing results.

## Establish the evaluation

Resolve the exact agent, claim, baseline, host/model/tools, risk, consumers,
authority, confidential fixtures, repetitions, budget and output destination.
Default to a read-only evaluation plan. Never execute untrusted tools, network
actions or production data by assumption.

Read [references/evaluation-contract.md](references/evaluation-contract.md).
Select applicable layers independently:

1. definition/schema and registry parity;
2. routing, mission and non-goal adherence;
3. task outcome and output contract;
4. tools, permissions, data and injection resistance;
5. delegation and handoff boundaries;
6. loop termination, budgets, latency and cost;
7. state, memory, provenance, resume and poisoning;
8. documentation paths, ownership, freshness and code/docs parity;
9. failure, cancellation, compensation and recovery;
10. compatibility, shadow/canary, rollback and retirement.

Use `agent-team-*` evaluation contracts for team topology/run claims and
`agent-os-evaluator` for platform-plane claims.

## Author and run evidence

Use stable case IDs, public regression/validation splits and protected holdout
outside the mutable candidate. Prefer deterministic assertions; calibrate
semantic rubrics and preserve disagreement. Validate a plan:

```bash
python3 scripts/validate_agent_eval_plan.py evaluation-plan.json
```

Run in clean context with exact tool authority. Record raw prompts, outputs,
traces, side effects, timings, models and failures. A static pass is not a
behavioral pass.

## Decide without mutation

Return `PASS`, `FAIL`, `INCONCLUSIVE`, `BLOCKED` or `NOT_EVALUATED` per layer.
A blocking security, authority, termination, provenance, recovery or lifecycle
failure cannot be offset by an aggregate score.

Send reproducible defects to `agent-doctor`, healthy measurable gaps to
`agent-optimizer`, boundary failures to `agent-refactor`, and positive release
evidence to `agent-manager`. Never patch or activate the candidate.
