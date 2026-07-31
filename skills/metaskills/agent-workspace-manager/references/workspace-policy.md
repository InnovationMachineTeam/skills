# Workspace policy

Use `WORKTREE_PER_TASK` only when all are true:

- at least two code-writing tasks can run independently;
- their write-sets are disjoint or have an explicit merge protocol;
- each task has a stable owner and bounded branch;
- the base revision and repository state are known;
- one integration owner owns ordering, conflict resolution and final tests;
- workspace lifecycle and cleanup have an accountable owner.

Use `SEQUENTIAL_SHARED` for overlapping files, migrations with ordering, one
mutable environment or high merge cost. Use `SHARED_READ_ONLY` for research.
Reject parallelism when ownership, base, paths or recovery are ambiguous.

Dirty state belonging to the user is evidence to stop or isolate from a clean
explicit commit; it is never authorization to reset, stash or overwrite it.
