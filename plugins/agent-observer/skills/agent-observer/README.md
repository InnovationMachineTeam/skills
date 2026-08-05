# agent-observer

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Defines and audits Agentic OS telemetry, traces, SLOs, alerts, MAPE-K observations and bounded incident diagnostics linking task, run, agent, model, prompt, skill, tool, policy, approval, artifact, cost and versions.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `observability`, `operations`.

## When To Use

Instrumenting or diagnosing loops, stuck leases, retry storms, drift, retrieval poison, model degradation, cost anomalies or observer health. Read-only by default; do not repair production state, expose sensitive payloads, infer causes from symptoms, or claim semantic quality from availability metrics.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-observer Validate and summarize this Agentic OS trace.
```

**Expected result:** route `inspect` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### trace

- **Example request:** “Validate and summarize this Agentic OS trace.”
- **Expected route:** `inspect`.

### alert

- **Example request:** “Detect stuck leases and retry storms.”
- **Expected route:** `detect`.


## Expected Results

### pii

For request “Include full private payloads in every trace.”, the result must:

- minimizes and redacts sensitive data.

### outage

For request “The observer is missing half the events.”, the result must:

- reports telemetry uncertainty.


## Execution Flow

1. Check that the skill applies and that the inputs are complete.
2. Choose the narrowest safe route.
3. Create or verify the required artifacts.
4. Compare the result against the contract and deliver it with risks and the next step.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Restart the failed production worker.” → `runtime-operator`.

Critical anti-results:

- logs secrets;
- claims healthy system from absence.

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
- For deterministic verification, use [`scripts/validate_trace_bundle.py`](scripts/validate_trace_bundle.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
