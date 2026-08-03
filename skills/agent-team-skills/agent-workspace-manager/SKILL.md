---
name: agent-workspace-manager
description: Plans and governs isolated agent workspaces or Git worktrees for approved parallel code tasks with explicit write-sets, owners, base revisions, branches, leases, quotas, integration handoffs, retention and safe exact-target cleanup. Use when deciding whether parallel writers need isolation, inventorying or allocating worktrees, reconciling divergence, recovering abandoned work, or releasing workspaces. Do not decompose tasks, treat worktrees as security boundaries, overwrite user changes, create broad paths, merge without an integration owner, or delete without verified ownership and retention authority.
metadata:
  version: "1.0.2"
---

# Govern Agent Workspaces

Use workspace isolation only when independent code write-sets justify its cost.
A worktree separates files and branches; it does not isolate credentials,
network, processes or data access.

## Decide the workspace policy

Read [references/workspace-policy.md](references/workspace-policy.md). Inspect the
task DAG, repository state, write-sets, dependencies, baseline, existing
worktrees/branches and integration ownership. Choose:

- `SHARED_READ_ONLY` for research or inspection;
- `SEQUENTIAL_SHARED` for dependent or overlapping writes;
- `WORKTREE_PER_TASK` for independent code writers with disjoint write-sets;
- `REJECT_PARALLELISM` when isolation or integration cannot be made safe.

Do not create worktrees for short single-agent tasks, non-Git artifacts or as a
substitute for permissions/sandboxing.

## Plan before materializing

Read [references/ledger-and-cleanup.md](references/ledger-and-cleanup.md). Pin a
clean-enough base revision without discarding unrelated changes. Allocate stable
task/workspace IDs, exact relative path, branch, owner agent, write-set, lease,
quota, expiry and integration owner. Detect path, branch, write-set and active
lease collisions.

Validate the ledger before any workspace mutation:

```bash
python3 scripts/validate_workspace_ledger.py workspace-ledger.json
```

Creation, dependency materialization, credential injection and network access
need their own explicit authority. Inject only scoped runtime references; never
copy secrets into a worktree.

## Track and integrate

Record base/current commit, heartbeat, tests, artifacts, divergence, failed
checks and handoff state. Only the named integration owner may rebase/merge under
the approved conflict policy. A passing worker branch is not proof the combined
result passes.

On stale base, conflict, failed test, expired lease or interruption, preserve
evidence and choose revalidate, rebase by owner, quarantine, reassign, archive or
recover. Never silently reuse an orphaned path.

## Release safely

Cleanup requires terminal or explicitly abandoned status, verified owner and
workspace identity, retained commits/artifacts according to policy, no active
lease, no unmerged work unless abandonment is approved, and an exact validated
target. Prefer recoverable removal. Never target a home directory, repository
root, unresolved variable, glob or parent traversal.

Return the policy decision, ledger revision, allocated/rejected workspaces,
collisions, integration handoffs, evidence, retained artifacts, cleanup decision
and residual risks.
