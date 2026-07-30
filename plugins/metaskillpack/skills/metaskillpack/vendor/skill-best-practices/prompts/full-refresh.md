# Route: full-refresh

Run the complete maintenance cycle.

1. Audit the source registry.
2. Refresh current source snapshots.
3. Compare previous and current snapshots.
4. Reconcile material claims against the practice corpus.
5. If semantic changes or integrity defects exist, rebuild the entire corpus in staging; otherwise record `NO_REBUILD`.
6. Validate and compare the corpus.
7. Generate the managed-skill modification master prompt from the resulting practice revision.
8. Produce a read-only applicability matrix unless exact modifications were separately authorized.
9. Report source coverage, semantic changes, conflict decisions, rebuild result, generated files, and next refresh trigger.

Stop before installed-skill mutation or activation unless the user explicitly authorized that later phase.
