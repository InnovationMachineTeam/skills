# Route: generate-modification-prompt

Generate a reusable master prompt from the current practice index and managed-skill registry.

1. Validate the managed target list and preserve target-specific role and risk notes.
2. Require a passing validation artifact and matching practice revision, corpus hash, source-registry hash, snapshot ID/hash, and reconciliation ID.
3. Require per-target discovery, baseline, applicability, proposed change, preserved invariants, validation, rollback, and installation status.
4. Require `NO_CHANGE` when a target already complies or the practice is inapplicable.
5. Route defects, independent evaluation/release evidence, optimizations, topology changes, creation, and lifecycle work to the appropriate specialists.
6. Require approval before active-root, public, destructive, or cross-consumer mutations.
7. Include unresolved conflict and unavailable-source counts, emit to a reviewable destination, and validate that every managed skill appears exactly once.

Do not embed full practice files or assume listed targets are installed.
