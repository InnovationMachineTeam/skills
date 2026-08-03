---
name: agent-optimizer
description: Improves one healthy agent or subagent against a frozen measurable quality, cost, latency, reliability, context or documentation target while preserving mission, authority, consumers and lifecycle invariants. Use after baseline evaluation when tuning prompts, context selection, tool policy, model routing, budgets or output quality for an individual agent. Do not repair reproduced defects, change mission, permissions, ownership or topology, optimize teams or Agentic OS, tune against protected holdout, activate candidates, or claim improvement from incomparable runs.
metadata:
  version: "1.0.2"
---

# Optimize One Healthy Agent

Require a healthy baseline and a measurable unmet target. Reproducible defects
belong to `agent-doctor`; mission, authority, ownership or topology changes
belong to `agent-refactor` or `agent-architect`.

Read [references/skill-dependencies.md](references/skill-dependencies.md). Block
optimization when its required evaluator is missing or below the declared
minimum; never construct a self-scored substitute.

## Freeze the experiment

Resolve exact agent/version/hash, baseline run, metric and threshold, preserved
invariants, fixtures, environment, authority, budgets, candidate limit and
rollback. Read [references/optimization-contract.md](references/optimization-contract.md).
Do not expose protected holdout answers.

## Optimize one hypothesis at a time

Choose a bounded surface: instructions, context retrieval, tool selection,
model/fallback policy, loop/budgets, memory retrieval, output contract or
documentation workflow. State causal hypothesis and expected trade-offs.

Create a new candidate revision, run the same validation conditions, compare
quality/cost/latency/reliability and check routing, authority, failure,
documentation and lifecycle regressions. Multi-objective gains cannot hide a
blocking regression.

Preserve canonical document paths and owners when optimizing context or output.
Changing taxonomy, ownership or decision authority is a refactor.

## Complete

Return `ACCEPT`, `REJECT`, `INCONCLUSIVE` or `BLOCKED` with comparable baseline
and candidate evidence, hypothesis, deltas, regressions, version and rollback.
Hand an accepted immutable candidate to `agent-evaluator`; activation remains
with `agent-manager`.
