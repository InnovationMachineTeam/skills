# agent-runtime-manager

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Governs platform-level durable task and run lifecycle with queues, attempts, leases, fencing, idempotency, checkpoints, cancellation, deadlines, backpressure, scoped execution, artifacts, compensation and dead-letter recovery.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `runtime`, `durability`.

## When To Use

Designing, validating, operating or recovering Agentic OS runtime state across workers or teams. Do not design teams or agents, enforce permission only in prompts, silently retry permanent or ambiguous side effects, or mutate pinned agent/workflow/model/policy versions during a run.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-runtime-manager Create a durable run record and queue this task.
```

**Expected result:** route `start` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### run

- **Example request:** “Create a durable run record and queue this task.”
- **Expected route:** `start`.

### recover

- **Example request:** “Recover the run after its worker lease expired.”
- **Expected route:** `recover`.


## Expected Results

### duplicate

For request “Deliver the same non-idempotent task twice.”, the result must:

- deduplicates by stable key.

### cancel-race

For request “Cancellation races with worker completion.”, the result must:

- uses fencing and terminal transition policy.


## Execution Flow

1. Check that the skill applies and that the inputs are complete.
2. Choose the narrowest safe route.
3. Create or verify the required artifacts.
4. Compare the result against the contract and deliver it with risks and the next step.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Choose agents for this task.” → `agent-team-architect`.

Critical anti-results:

- duplicates effect;
- reports two terminal states.

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
- For deterministic verification, use [`scripts/validate_runtime_record.py`](scripts/validate_runtime_record.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
