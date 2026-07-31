# Ledger and cleanup

The canonical ledger records its revision, repository, policy, integration
owner, baseline, collision policy and each workspace's stable ID, task, owner,
relative path, branch, base/current revision, write-set, lease, quota, status,
tests, artifacts and retention decision.

Allowed statuses: `PLANNED`, `ALLOCATED`, `ACTIVE`, `READY`, `INTEGRATED`,
`FAILED`, `CANCELLED`, `ABANDONED`, `ARCHIVED`, `RELEASED`.

Cleanup is a state transition, not merely file deletion. It is allowed only for
an exact registered path after ownership, lease, unmerged commits, artifacts,
retention and repository-root checks pass. Preserve branch/commit references or
an archive when policy requires recovery. Report whether removal is recoverable.
