# Evaluation and optimization

Practice-ID: BP-EVAL-001
Scope: mixed
Status: current
Sources: SRC-AS-003, SRC-AS-004, SRC-ANT-001, SRC-ANT-002, SRC-EX-002, SRC-LOCAL-001
Last-rebuilt: 2026-07-30

## Separate evidence layers

Routing evals test whether the correct skill activates. Behavioral evals test whether the skill improves the actual result. Structural validity, script correctness, security, coexistence, lifecycle state, and user outcome are additional distinct layers.

## Case design

Use realistic prompts, fixtures, observable assertions, human-review criteria for subjective quality, malformed and adversarial inputs, unsupported actions, recovery cases, and neighboring-skill composition. Run the current skill against a no-skill or previous-version baseline in comparable environments and repeat stochastic cases.

Protect evaluation integrity: use fresh context, raw artifacts, no leaked expected answer or intended fix, separate train/validation/holdout, record model/host/tools/runtime, and prevent optimizers from reading holdout during iteration.

## Optimization discipline

State one falsifiable hypothesis, change the smallest coherent surface, keep other variables stable, inspect raw outputs, and accept only meaningful improvement without blocking regression. Measure quality, tokens, latency, tool calls, retries, and risk as a Pareto surface. Stop at plateau or disproportionate complexity.

Cross-model or cross-provider review can reduce correlated blind spots for high-risk artifacts, but it is not universal proof. Record identities, costs, disclosure, failures, and the limits of model-based grading.

Do not lock placeholder or mediocre behavior into tests. Review intended quality first, then encode regression behavior.
