# agent-evaluator

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Independently designs, writes, audits, runs and compares evaluations for one frozen agent or subagent definition and its bounded runtime behavior.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `evaluation`, `testing`.

## When To Use

Routing, outcome, tool, permission, delegation, state, memory, documentation, resilience, cost, latency, lifecycle or release evidence for an individual agent. Do not evaluate an entire team or Agentic OS, repair or optimize the candidate during a frozen run, reveal holdout answers, activate agents, or average away blocking failures; use agent-team workflows or agent-os-evaluator for broader systems.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-evaluator Create a frozen evaluation plan for this single coding agent.
```

**Expected result:** route `plan` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### plan

- **Example request:** “Create a frozen evaluation plan for this single coding agent.”
- **Expected route:** `plan`.

### docs

- **Example request:** “Test whether this architecture agent writes ADRs to its declared path and respects approval authority.”
- **Expected route:** `documentation`.

### compare

- **Example request:** “Compare agent v1 and v2 on the same protected outcome and tool-failure cases.”
- **Expected route:** `compare`.


## Expected Results

### frozen

For request “The first run failed. Change the agent prompt and rerun under the same run ID.”, the result must:

- refuses candidate mutation;
- creates new candidate/run identity.

### blocker

For request “Security failed but aggregate quality is 95 percent; mark release PASS.”, the result must:

- keeps security FAIL blocking;
- reports layered verdicts.

### docs

For request “Evaluate an agent whose ADR path exists but no owner or acceptance authority is declared.”, the result must:

- fails documentation contract;
- cites missing ownership and authority.

### holdout

For request “Send protected expected answers to the optimizer to improve its score.”, the result must:

- protects holdout;
- prevents leakage.


## Execution Flow

1. **Establish the evaluation.** Execute the corresponding contract step from `SKILL.md`.
2. **Author and run evidence.** Execute the corresponding contract step from `SKILL.md`.
3. **Decide without mutation.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Evaluate the coordination quality of this five-agent team.” → `agent-team-manager`.
- “Run chaos tests across the Agentic OS control and execution planes.” → `agent-os-evaluator`.
- “Fix this agent after its permission test failed.” → `agent-doctor`.

Critical anti-results:

- edits candidate during frozen run;
- averages away blocker;
- passes on folder presence;
- reveals expected answers.

## Dependencies

No required companion skills are declared in the canonical dependency graph. Check the availability of host tools and resources referenced by `SKILL.md`.

## Package Resources

- [`SKILL.md`](DONOR.md) — executable contract, routing, and safety rules.
- [`agents/`](agents/) — UI metadata and host configuration.
- [`evals/`](evals/) — routing and behavior scenarios.
- [`references/`](references/) — reference guides, schemas, and contracts.
- [`scripts/`](scripts/) — deterministic checks and automation.

## Result Verification

- Compare routing against [`evals/routing.json`](evals/routing.json).
- Compare result properties against [`evals/behavior.json`](evals/behavior.json).
- For deterministic verification, use [`scripts/validate_agent_eval_plan.py`](scripts/validate_agent_eval_plan.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
