# Optimization plan: agentkit-release-steward

Healthy baseline: `0.1.1`, exact hash recorded in `baseline.json`.

One hypothesis is changed: lower `runtime.budgets.max_cycles` from 6 to 4.
This should reduce unnecessary re-analysis while retaining one inventory pass,
one deterministic validation pass, one reconciliation pass and one final
proposal pass. Mission, permissions, documentation, tools, stop conditions,
review and lifecycle state remain byte-equivalent except for the version.

Acceptance: candidate metric equals 4; all blocking guardrails pass; no active
state changes. Rejection or rollback restores the immutable 0.1.1 definition.
