# Route: migration

Default to `plan` mode and read `references/migration-contract.md`.

Produce an exact source-to-target mapping, phased actions, owners, dependencies, acceptance gates, observability, rollback, and open decisions. Copy into staging before cutover. Preserve the old tree until a separate retirement approval.

If apply mode is explicit, execute one approved phase at a time, stop at review checkpoints, record hashes and diffs, and keep the rollback path live. Approval of a plan does not authorize publication, global installation, cutover, or deletion.
