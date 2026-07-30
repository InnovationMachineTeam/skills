# Scenario: split-and-migrate

Use when an oversized skill contains materially different trigger families, owners, permissions, resources, or release cycles.

1. Invoke `skill-refactor` boundary assessment and select `SPLIT`, `EXTRACT_SUBSKILL`, `EXTRACT_REFERENCE`, or a justified alternative.
2. Inventory consumers, old triggers, shared resources, mutable state, dependencies, versions, and active host routing.
3. Produce an approved topology and file-operation plan before edits.
4. Use `skill-architect` to scaffold new skill packages and one owner per trigger/resource/state surface.
5. Add a compatibility facade or explicit migration when consumers may use the old entry point.
6. Invoke `skill-evaluator` to validate new and legacy routing, behavior, security, portability, consumer E2E, rollback, and catalog coexistence against an immutable baseline.
7. Route failures to doctor, architect, or refactor according to root cause, then rerun affected and holdout gates.
8. Use `skill-manager` for staged activation and recoverable retirement of the old skill.

Do not delete the source skill or duplicate changing knowledge until replacement behavior and migration are verified.
