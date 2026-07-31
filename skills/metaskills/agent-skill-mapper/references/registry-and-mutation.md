# Registry and mutation rules

The registry is the inventory of record; the map is the relationship view.
Definitions remain canonical for agent behavior. A proposal must record the
registry and map revisions it analyzed so staleness is detectable.

Public capabilities use repository/public roots and may have many consumers.
Private capabilities live under one agent, declare `visibility: private`, name
that owner and list exactly that owner as the sole allowed consumer.

Mutation requires explicit authority and one transaction:

1. Re-read revisions and abort on mismatch.
2. Back up affected files.
3. Update agent definitions and SemVer.
4. Update relationship map and registry metadata.
5. Regenerate host adapters from canonical definitions.
6. Validate references, visibility, permissions, budgets and evals.
7. Commit atomically or restore the backup.

Mapping does not imply installation or activation. Keep `recommended`,
`approved`, `installed` and `active` as distinct states.
