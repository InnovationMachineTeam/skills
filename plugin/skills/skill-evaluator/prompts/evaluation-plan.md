# Route: evaluation-plan

Create a versioned evaluation manifest before execution.

1. State the claim or release decision being evaluated.
2. Bind target hash/version, host, model, tools, runtime, baseline, and consumers.
3. Select applicable evidence layers and justify exclusions.
4. Define datasets, fixtures, splits, graders, repetitions, budgets, timeouts, metrics, and raw artifacts.
5. Freeze layer-specific acceptance and blocking-regression criteria.
6. Define authority, confidentiality, side-effect, abort, cleanup, and recovery rules.
7. Define handoffs for failure, improvement, topology, and lifecycle outcomes.

Emit `evaluation-plan.json` and validate it. Do not run cases unless execution was also requested and authorized.
