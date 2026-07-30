# Route: compare-evaluations

Compare baseline and candidate evidence without hiding regressions.

1. Require matching case identity, splits, environment, model/host/tool state, repetitions, graders, and target-bound run manifests.
2. Separate added, removed, changed, flaky, improved, regressed, unchanged, and incomparable cases.
3. Compare layer metrics plus tokens, latency, tool calls, retries, cost, and risk where observable.
4. Apply frozen acceptance thresholds and blocking-regression rules.
5. Inspect raw artifacts for material disagreements and Simpson's-paradox-like aggregation effects.
6. Return `ACCEPT`, `REJECT`, `INCONCLUSIVE`, or `BLOCKED` as an evaluation recommendation, not deployment authority.

Do not average away a security, authority, data-loss, or lifecycle regression.
