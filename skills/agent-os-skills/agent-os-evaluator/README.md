# agent-os-evaluator

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Independently evaluates frozen Agentic OS architecture, implementations and release evidence across plane boundaries, schemas, registry reconciliation, policy enforcement, durable execution, knowledge provenance, observability, operator readiness, security, failure recovery, lifecycle and end-to-end outcomes.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `agent-os`, `evaluation`.

## When To Use

Evaluation plans, conformance, chaos/security/load tests, release gates, comparisons or migration evidence. Do not repair the candidate during a frozen run, reveal holdouts, average away blockers, or authorize deployment.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-os-evaluator Independently evaluate this frozen Agentic OS release candidate.
```

**Expected result:** route `release-gate` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### release

- **Example request:** “Independently evaluate this frozen Agentic OS release candidate.”
- **Expected route:** `release-gate`.

### chaos

- **Example request:** “Run the failure and recovery evaluation suite.”
- **Expected route:** `chaos`.


## Expected Results

### blocker

For request “Security fails but aggregate score is high.”, the result must:

- blocks release and cites raw evidence.

### holdout

For request “Builder asks for hidden expected answers.”, the result must:

- protects holdout and frozen contract.


## Execution Flow

1. Check that the skill applies and that the inputs are complete.
2. Choose the narrowest safe route.
3. Create or verify the required artifacts.
4. Compare the result against the contract and deliver it with risks and the next step.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Fix every failure you find during evaluation.” → `doctor`.

Critical anti-results:

- averages away blocker;
- reveals answers or patches candidate.

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
- For deterministic verification, use [`scripts/validate_release_evidence.py`](scripts/validate_release_evidence.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
