# Мастер-промпт навыка `agent-workspace-manager`

Применяй после [agent-skill-base.md](agent-skill-base.md). Создай skill для
безопасной выдачи isolated workspaces/worktrees агентам с независимыми
write-sets. Он не решает task decomposition и не удаляет workspace без
проверенного ownership/retention gate.

## Procedure

- decide `SHARED_READ_ONLY`, `SEQUENTIAL_SHARED`, `WORKTREE_PER_TASK` or
  `REJECT_PARALLELISM` from dependency and write-set analysis;
- verify clean-enough baseline without overwriting unrelated user changes;
- allocate stable task/workspace IDs, branch/base revision, owner, lease, path,
  quotas and expiry;
- materialize only approved dependencies and secrets through scoped runtime
  injection;
- track commits, tests, produced artifacts and divergence;
- integrate through a named merge owner with conflict and rebase policy;
- handle cancellation, abandoned leases, partial work and recovery;
- archive evidence and clean up only exact validated targets through a
  recoverable policy.

## Evals

Test overlapping writes, dirty baseline, stale base, simultaneous completion,
merge conflict, failed test, interruption/resume, orphan workspace and cleanup
denial. Report workspace ledger and never use broad destructive paths.
