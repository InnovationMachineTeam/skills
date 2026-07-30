# Route: audit-evaluation

Review an existing evaluation system without rerunning it by default.

1. Check target binding, baseline comparability, layer coverage, realistic cases, splits, holdout protection, and acceptance criteria.
2. Check deterministic assertions, rubric anchors, grader calibration, human review, repetitions, and metric validity.
3. Detect expected-answer leakage, optimizer access to holdout, cherry-picking, duplicate lineage, flaky cases, brittle exact text, and silent exclusions.
4. Verify raw artifacts, environment identity, failures, costs, side effects, and skipped gates.
5. Classify gaps by whether they invalidate a claim, weaken confidence, or merely improve maintainability.

Do not call missing evidence a failure of the target; mark the evaluation claim `INCONCLUSIVE` or `BLOCKED`.
