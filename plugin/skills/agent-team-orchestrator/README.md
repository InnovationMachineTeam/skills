# agent-team-orchestrator

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Executes an approved, active agent-team definition through a bounded task graph with typed envelopes, minimal context capsules, leases, budgets, checkpoints, cancellation, recovery and independent verification.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `runtime`, `orchestration`.

## When To Use

Launching, resuming, monitoring, cancelling or recovering a concrete team run. It may choose only among declared workflows and cannot redesign teams, edit agents or skills, broaden authority, create worktrees directly, publish outputs by implication, or replace the lifecycle control plane owned by agent-team-manager.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-team-orchestrator Plan an approved team run for this task envelope.
```

**Expected result:** route `plan` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### plan

- **Example request:** “Plan an approved team run for this task envelope.”
- **Expected route:** `plan`.

### run

- **Example request:** “Execute this task with active team review@1.0.0.”
- **Expected route:** `run`.

### monitor

- **Example request:** “Show leases, budget and blockers for run 42.”
- **Expected route:** `monitor`.

### resume

- **Example request:** “Resume run 42 from its verified checkpoint.”
- **Expected route:** `resume`.

### cancel

- **Example request:** “Cancel run 42 and preserve partial evidence.”
- **Expected route:** `cancel`.

### recover

- **Example request:** “Recover the team run after one worker failed.”
- **Expected route:** `recover`.


## Expected Results

### sequential

For request “Run two dependent stages.”, the result must:

- dispatches in dependency order;
- checks each exit gate.

### fork-join

For request “Run two independent reviews then integrate.”, the result must:

- uses disjoint write-sets;
- names integration owner;
- independently verifies result.

### worker-failure

For request “One fork fails deterministically.”, the result must:

- classifies failure;
- does not retry deterministic failure indefinitely;
- uses approved recovery.

### conflict

For request “Two workers produce conflicting outputs.”, the result must:

- routes conflict to integration policy and verifier.

### budget

For request “The run exhausts its step budget.”, the result must:

- stops new dispatch;
- returns resumable blocked evidence.

### cancel

For request “Cancel then resume the run.”, the result must:

- makes cancellation durable and idempotent;
- revalidates checkpoint and external state.

### duplicate

For request “The same task delivery arrives twice.”, the result must:

- uses idempotency key;
- avoids duplicate side effects.

### stale

For request “The agent version changed after plan approval.”, the result must:

- blocks dispatch and returns to assessment.


## Execution Flow

1. **Gate and plan the run.** Execute the corresponding contract step from `SKILL.md`.
2. **Dispatch bounded context.** Execute the corresponding contract step from `SKILL.md`.
3. **Observe, recover and cancel.** Execute the corresponding contract step from `SKILL.md`.
4. **Integrate and verify.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Add a verifier role to this team.” → `agent-team-architect`.
- “Retire this entire agent team.” → `agent-team-manager`.

Critical anti-results:

- parallelizes shared writes;
- lets workers self-merge without protocol;
- claims full completion;
- chooses silently;
- raises budget itself;
- continues stale leases;
- creates a second independent run;
- runs stale definition.

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
- For deterministic verification, use [`scripts/validate_run_plan.py`](scripts/validate_run_plan.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
