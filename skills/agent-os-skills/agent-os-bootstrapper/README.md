# agent-os-bootstrapper

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Materializes an approved Agentic OS architecture as one staged, reproducible vertical walking skeleton from authenticated request through policy, registry, durable task and lease, bounded execution, artifact verification, telemetry and terminal state.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `agent-os`, `bootstrap`.

## When To Use

An exact approved architecture and destination are ready for local bootstrap, rebuild or migration. Do not redesign planes, use production credentials, activate or roll out production, retain partial active state, or expand beyond the approved vertical slice.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-os-bootstrapper Stage this approved Agentic OS walking skeleton.
```

**Expected result:** route `bootstrap` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### stage

- **Example request:** “Stage this approved Agentic OS walking skeleton.”
- **Expected route:** `bootstrap`.

### rebuild

- **Example request:** “Rebuild the local disposable Agentic OS fixture.”
- **Expected route:** `rebuild`.


## Expected Results

### unapproved

For request “Bootstrap this draft architecture in production.”, the result must:

- blocks unapproved design;
- keeps production activation false.

### partial

For request “Migration fails halfway.”, the result must:

- rolls back staged state and preserves trace.


## Execution Flow

1. Check that the skill applies and that the inputs are complete.
2. Choose the narrowest safe route.
3. Create or verify the required artifacts.
4. Compare the result against the contract and deliver it with risks and the next step.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Decide which planes we need.” → `agent-os-architect`.

Critical anti-results:

- uses production credentials;
- leaves active partial system.

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
- For deterministic verification, use [`scripts/validate_bootstrap_manifest.py`](scripts/validate_bootstrap_manifest.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
