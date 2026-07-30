# Scenario: resume-build

Use when the user supplies a prior `skill-build-state.json`, phase ledger, or explicit request to continue a paused build.

1. Validate the state structure and resolve every referenced target and artifact.
2. Compare current target hashes, external revisions, host state, tools, permissions, and acceptance criteria with the checkpoint.
3. Preserve completed consequential phases; do not repeat installs, publication, migrations, or deletions.
4. Mark stale evidence and recompute only affected downstream phases.
5. Resolve outstanding `waiting_approval` or `blocked` conditions before execution.
6. Continue from the first incomplete phase whose entry conditions remain valid.
7. Update the ledger atomically and verify the final scenario outcome.

If state is missing, contradictory, or materially stale, reconstruct a read-only plan from artifacts and ask one focused question rather than guessing what already happened.
