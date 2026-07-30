# Scenario: compare-and-refactor

Use when two or more existing skills may overlap, conflict, compose, or deserve a topology change.

1. Run `skill-harvester` `pairwise-skill-comparison` for read-only evidence on outcomes, triggers, workflows, authority, resources, tools, evals, consumers, and release cadence.
2. Stop with the comparison if no mutation was requested.
3. Invoke `skill-refactor` for `KEEP_SEPARATE`, `COMPOSE`, `MERGE`, `SPLIT`, `EXTRACT_REFERENCE`, `EXTRACT_SUBSKILL`, or `CREATE_FACADE`.
4. Validate a complete refactor plan and obtain mutation approval.
5. Stage the new topology, preserve old entry points when consumers may depend on them, and use `skill-architect` for newly extracted packages.
6. Invoke `skill-evaluator` for old/new routing, catalog coexistence, behavior, consumer E2E, security, portability, facade, and rollback cases. Keep source and candidate revisions immutable during comparison.
7. Route confirmed defects to doctor and re-evaluate the new revision; do not let aggregate improvements mask a broken consumer or security gate.
8. Use `skill-manager` for activation, versioning, migration, and retirement.

Shared wording or files are not enough to merge. Different permissions, users, lifecycle, or completion criteria strongly favor separation or composition.
