# Individual-agent lifecycle contract

States: `draft`, `candidate`, `verified`, `approved`, `shadow`, `canary`,
`active`, `suspended`, `deprecated`, `retired`. Hosts may project fewer states;
record the adapter mapping without changing canonical meaning.

Every transition declares source/target, exact version/hash, expected registry
and map revisions, accountable approver, runtime authority, consumers, active
runs, evidence, observation window, abort conditions and rollback.

Documentation is a gate: canonical inputs must exist and be fresh; operations
need a runbook; retirement transfers or supersedes owned artifacts and removes
live bindings without erasing history.
