# Scenario: evaluate-skill

Use when the user's terminal outcome is trustworthy evaluation evidence for one or more exact skill revisions.

1. Invoke `skill-evaluator` and select the smallest sufficient route: plan, routing/triggers, behavior/quality, script/tooling, security/authority, catalog/coexistence, run, audit, or compare.
2. Freeze target identity, suite revision, host/model/tool environment, authority, baselines, metrics, budgets, blocking layers, split policy, holdout, and raw-artifact locations before execution.
3. Prefer deterministic assertions, then calibrated rubrics, then proxies or judgment. Include positive, negative, ambiguous, neighboring, boundary, failure, adversarial, and recovery cases as applicable.
4. Execute only scripts whose target, inputs, side effects, timeout, isolation, credentials, and cleanup are authorized. Treat repository code and test fixtures as untrusted.
5. Report every applicable layer as `PASS`, `FAIL`, `INCONCLUSIVE`, `BLOCKED`, or `NOT_EVALUATED`; do not average away blocking failures.
6. If a defect is confirmed, return a bounded handoff to `skill-doctor`; if a healthy measurable opportunity exists, hand it to optimizer; if boundaries collide, hand it to refactor.
7. Do not apply those mutations in this scenario. If the user later authorizes a new candidate, run a new evaluation revision and compare it with the frozen baseline and holdout.

Structural validation, a single successful stochastic sample, a model judge without calibration, or a self-authored suite alone cannot prove production readiness. A release recommendation is evidence for `skill-manager`, not installation or activation authority.
