# Scenario: repair-and-improve

Use when a skill has a confirmed or reported defect and may also need measurable improvement after recovery.

1. Invoke `skill-doctor` in diagnose mode, preserving the failing case and last-known-good evidence.
2. Ask for repair authority if edits are not already authorized.
3. Apply only the smallest confirmed repair and rerun the identical reproduction plus relevant regressions.
4. Stop if recovery is `UNVERIFIED`, `BROKEN`, or `UNSAFE`.
5. Invoke `skill-evaluator` to verify the repaired revision against the original reproduction, affected layers, frozen regressions, holdout, and catalog neighbors.
6. Preserve the accepted healthy evaluator run as the optimization baseline before invoking `skill-optimizer`.
7. Optimize one falsifiable hypothesis at a time; have evaluator compare baseline and candidate in the same environment and reject blocking regressions.
8. Use `skill-manager` only for an approved update or activation after recovery and improvement evidence.

Do not label a repair as an optimization or use optimization to conceal an unreproduced defect.
