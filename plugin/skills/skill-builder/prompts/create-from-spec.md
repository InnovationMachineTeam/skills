# Scenario: create-from-spec

Use when the capability, users, triggers, outputs, authority, and destination are already sufficiently defined.

1. Audit the specification for material gaps; ask only discriminating questions.
2. Invoke `skill-architect` directly. Do not rerun opportunity discovery merely because it is available.
3. Invoke `skill-evaluator` to validate the eval plan and run the appropriate routing, behavior, script/tool, security, coexistence, portability, and realistic forward gates.
4. Route reproducible failures to `skill-doctor`, then let evaluator rerun affected regressions and holdout on the repaired revision.
5. Return a reviewable bundle plus layered verdict unless installation was explicitly requested.
6. If installation is requested, use `skill-manager` for provenance, version, staged activation, host verification, and rollback; evaluator evidence does not authorize activation.

If the specification actually describes multiple trigger families or capability owners, pause creation and route boundary work to `skill-refactor` or ask the user to approve a split.
