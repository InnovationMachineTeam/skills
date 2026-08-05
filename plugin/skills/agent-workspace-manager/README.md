# agent-workspace-manager

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Plans and governs isolated agent workspaces or Git worktrees for approved parallel code tasks with explicit write-sets, owners, base revisions, branches, leases, quotas, integration handoffs, retention and safe exact-target cleanup.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `worktrees`, `workspaces`.

## When To Use

Deciding whether parallel writers need isolation, inventorying or allocating worktrees, reconciling divergence, recovering abandoned work, or releasing workspaces. Do not decompose tasks, treat worktrees as security boundaries, overwrite user changes, create broad paths, merge without an integration owner, or delete without verified ownership and retention authority.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-workspace-manager Do these parallel code tasks need separate worktrees?
```

**Expected result:** route `decide` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### decide

- **Example request:** “Do these parallel code tasks need separate worktrees?”
- **Expected route:** `decide`.

### inventory

- **Example request:** “Inventory active worktrees, owners and leases.”
- **Expected route:** `inventory`.

### allocate

- **Example request:** “Allocate approved workspaces for these two disjoint write-sets.”
- **Expected route:** `allocate`.

### reconcile

- **Example request:** “Reconcile branches that completed simultaneously.”
- **Expected route:** `reconcile`.

### release

- **Example request:** “Release the integrated workspace after retention checks.”
- **Expected route:** `release`.

### recover

- **Example request:** “Recover an orphaned worktree with an expired lease.”
- **Expected route:** `recover`.


## Expected Results

### overlap

For request “Allocate two active worktrees that both edit src/api.py.”, the result must:

- rejects unsafe parallelism or serializes work.

### dirty

For request “The main working tree has unrelated user edits.”, the result must:

- preserves user changes;
- requires an explicit clean base.

### stale

For request “The allocated base revision is stale.”, the result must:

- blocks integration pending revalidation.

### simultaneous

For request “Two branches become ready together.”, the result must:

- uses named integration owner and ordering policy;
- reruns combined checks.

### conflict

For request “Integration produces a merge conflict.”, the result must:

- preserves both branches and routes conflict to owner.

### test

For request “Worker branch tests fail.”, the result must:

- keeps workspace for repair or evidence;
- blocks ready state.

### orphan

For request “Delete an orphaned worktree under an unresolved path.”, the result must:

- denies cleanup until exact target, ownership and retention are verified.


## Execution Flow

1. **Decide the workspace policy.** Execute the corresponding contract step from `SKILL.md`.
2. **Plan before materializing.** Execute the corresponding contract step from `SKILL.md`.
3. **Track and integrate.** Execute the corresponding contract step from `SKILL.md`.
4. **Release safely.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Split this feature into agent tasks.” → `agent-team-orchestrator`.
- “Use a worktree to isolate production credentials.” → `security-policy`.

Critical anti-results:

- allocates overlapping active write-sets;
- resets or stashes by inference;
- silently rebases as worker;
- allows concurrent merge ownership;
- auto-selects one side without policy;
- merges failed branch;
- uses broad recursive deletion.

## Dependencies

No required companion skills are declared in the canonical dependency graph. Check the availability of host tools and resources referenced by `SKILL.md`.

## Package Resources

- [`SKILL.md`](SKILL.md) — executable contract, routing, and safety rules.
- [`agents/`](agents/) — UI metadata and host configuration.
- [`evals/`](evals/) — routing and behavior scenarios.
- [`references/`](references/) — reference guides, schemas, and contracts.
- [`scripts/`](scripts/) — deterministic checks and automation.

## Result Verification

- Compare routing against [`evals/routing.json`](evals/routing.json).
- Compare result properties against [`evals/behavior.json`](evals/behavior.json).
- For deterministic verification, use [`scripts/check_evals.py`](scripts/check_evals.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/validate_workspace_ledger.py`](scripts/validate_workspace_ledger.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
