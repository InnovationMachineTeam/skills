# Scenario: optimize-existing

Use for a healthy skill with a measurable routing, quality, safety, portability, performance, or context-cost target.

1. Confirm health or run a bounded doctor check when health is uncertain.
2. Invoke `skill-evaluator` to freeze the baseline suite, target revision, environment, metric, blocking gates, holdout, and raw artifacts.
3. Invoke `skill-optimizer` with that baseline, one falsifiable hypothesis, preserved invariants, and allowed files.
4. Have `skill-evaluator` run the candidate and compare it with the baseline under comparable conditions, including affected neighbor/catalog and holdout regressions.
5. Accept only `ACCEPT`; preserve `REVISE`, `REJECT`, `INCONCLUSIVE`, and incomparable results honestly.
6. Route confirmed defects to doctor, not back into an unbounded optimization loop.
7. Use `skill-manager` for approved rollout and rollback of the exact accepted revision.

Route merge, split, extraction, or facade work to `skill-refactor` rather than expanding optimization scope.
