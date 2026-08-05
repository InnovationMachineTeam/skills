# Master Prompt For The `agent-optimizer` Skill

Apply [agent-documentation-contract.md](agent-documentation-contract.md) if the
optimization affects context loading or document outputs. Preserve canonical
paths and ownership; taxonomy changes belong to `agent-refactor`.

Apply after [agent-skill-base.md](agent-skill-base.md). Create a skill that
experimentally improves a healthy existing agent against a measurable target,
while preserving mission, authority, safety floors, and compatibility.

## Entry gate

Require:

- exact healthy target revision;
- measurable optimization objective;
- reproducible baseline;
- preserved invariants and blocking thresholds;
- comparable evaluation environment;
- mutation authority and staged destination.

If there is a reproducible defect, route to `agent-doctor`. If mission,
ownership, permissions, or topology must change, route to `agent-architect` or
`agent-refactor`.

## Optimization domains

- task quality/groundedness;
- routing precision and scope;
- context/token footprint;
- tool selection/call count;
- latency/throughput;
- cost per successful outcome;
- loop depth/retries;
- delegation granularity/parallelism;
- memory retrieval precision/freshness;
- resilience/recovery;
- observability/diagnosability;
- portability/model-runtime compatibility.

Risk, policy, and required human oversight are not optimization variables
without a separate architecture/governance decision.

## Experimental method

1. Freeze the baseline definition, datasets, environment, and metrics.
2. Record one falsifiable hypothesis.
3. Change the minimal factor.
4. Create an immutable candidate.
5. Execute repeated comparable runs.
6. Compare the primary metric, guardrails, variance, and subgroups.
7. Analyze regressions and unexpected trade-offs.
8. Accept, reject, or mark inconclusive by a predefined rule.
9. Hand the accepted candidate to an independent evaluator/manager.

Do not choose the best result from many runs without accounting for selection bias.

## Multi-objective guardrails

Optimize in a Pareto-aware way: improving cost cannot break correctness/safety;
reduced latency does not justify new race/partial failures; compression cannot
remove authority or recovery instructions.

Minimal report:

```yaml
baseline: agent@1.2.0
candidate: agent@1.3.0-rc.1
hypothesis: bounded statement
primary_metric: cost_per_success
guardrails: [critical_failures, task_success, p95_latency]
comparison: {}
decision: INCONCLUSIVE
regressions: []
```

## Agent-specific evals

Verify neighboring intents, tool denial, partial worker failure, budget
pressure, state resume, memory freshness, adversarial context, and canary-like
load. For orchestrators, compare the end-to-end outcome, not just individual
worker quality.

## Handoff

An accepted candidate does not become active automatically. `agent-evaluator`
produces the independent layered verdict, and `agent-manager` manages
rollout/rollback.
