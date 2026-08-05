# Lifecycle and Orchestration Processes

This file describes end-to-end processes. The comparison of runtime,
improvement, delivery, risk, and learning loops, as well as the lifecycles of
individual entities, is covered in
[20-agentic-cycles-and-lifecycles.md](20-agentic-cycles-and-lifecycles.md).

## Universal loop

```text
Intent → Context → Specify → Plan → Generate ↔ Validate → Govern
  ↑                                                    ↓
Observe ← Operate ← Deploy ← Release readiness ← Integrate
```

This is not a mandatory waterfall. For a simple task, the loop compresses; in
ADLC, Generate, Validate, and Observe run in parallel. But no run should lose
intent, evidence, or governance.

## 1. Intake and mode selection

1. Normalize the request into goal, context, constraints, and done.
2. Classify uncertainty, risk, reversibility, and scope.
3. Check existing capabilities and avoid creating a duplicate agent.
4. Choose the mechanism: code, workflow, agent, subagents, or team.
5. Define the autonomy level and approvals.
6. Create run/task IDs and the initial trace.

Output: intent record + selected workflow with rationale.

## 2. Discovery

Use when the problem or solution is unknown:

1. Formulate research questions and the decision to inform.
2. Split sources/aspects across read-only researchers.
3. Gather evidence with provenance and date.
4. Separate facts, interpretations, and gaps.
5. Perform adversarial synthesis.
6. Form a bet: hypothesis, generation target, resolution signal, deadline.
7. Human governance: continue, change course, or stop.

OpenSpec `/explore` intentionally does not write code or artifacts until the
problem is clarified; Agent OS looks for reference implementations and
standards first; gstack follows the principle of search before building. This
reduces premature implementation.

## 3. Requirements

1. Define stakeholders and the system boundary.
2. Elicit needs, business rules, and constraints.
3. Create atomic functional requirements.
4. Operationalize quality attributes with scenarios and targets.
5. Add error, abuse, edge, and recovery cases.
6. Record assumptions and non-goals.
7. Build traceability to sources and verification.
8. Independently review ambiguity, conflicts, feasibility, and testability.
9. Human approval for scope and high-impact trade-offs.

## 4. Architecture and planning

1. Build the context/container view and critical flows.
2. Identify architecturally significant requirements.
3. Consider options and record an ADR.
4. Decompose into independently valuable vertical slices.
5. For each slice, define the owner, write-set, dependencies, and verification.
6. Build the DAG and waves.
7. Add a threat, migration, rollout, and rollback plan.
8. The plan reviewer checks goal achievement backward from the goal.
9. Record preconditions and human checkpoints.

Spec Kit separates WHAT from HOW and groups tasks by independently testable
user stories; GSD adds must-haves, artifacts, and key links; OpenSpec allows
moving back and forth between artifacts. Use them together without turning the
plan into an immutable contract.

## 5. Execution

For each wave:

1. Check dependencies and preconditions with read-only actions.
2. Issue leases and permission envelopes.
3. Dispatch independent scoped implementers.
4. Each implementer tests and returns evidence.
5. The integration owner checks collisions and contracts.
6. Run targeted reviews.
7. Update durable state and the next ready set.

The first slice SHOULD be a tracer/walking skeleton: a thin end-to-end
production-quality path that verifies integration before expansion.

## 6. Verification

Verification is executed from the outcome backward:

1. Derive truths from the goal/spec.
2. For each truth, determine the artifacts and wiring.
3. Check live code/runtime instead of trusting a summary.
4. Run tests/evals and verify scenarios.
5. Classify `verified`, `failed`, `uncertain`, `human_needed`.
6. Create a gap plan instead of silently fixing outside the role.
7. Repeat only failed items plus regression checks.

OpenSpec checks completeness/correctness/coherence; GSD checks
truth/artifact/wiring. The combined gate should account for both views.

## 7. Release and deploy

1. Check versions, migrations, docs, security, and rollback.
2. Form the release evidence bundle.
3. The policy engine computes the required approvals.
4. The deploy agent acts only within the approved envelope.
5. Use feature flag/canary and automated rollback triggers.
6. Verify production behavior and signals.
7. Close the change only after the observation window.

ADLC emphasizes agent-orchestrated, human-approved deployment and recoverability
([ADLC](https://www.adlc.io/)).

## 8. Observe and learn

1. Collect product, system, and agent signals.
2. Link them to the bet, requirement, and run.
3. Identify anomalies, drift, high-cost paths, and repeated failures.
4. Create candidate learnings with provenance.
5. Verify and approve changes to memory/policy.
6. Add production cases to the eval dataset.
7. Form new bets or corrective changes.

## Standard orchestration processes

### Parallel research

Split by independent sources → fan-out → evidence normalization → conflict
resolution → synthesis → source audit.

### Competing-hypothesis debugging

One investigator per hypothesis → fixes forbidden → shared evidence board →
falsification → root-cause gate → scoped fix → regression verification.

### Cross-layer feature

Contract-first plan → backend/frontend/data agents with non-overlapping
write-sets → integration agent → E2E verifier.

### Review army

The scope detector chooses relevant specialists → independent parallel review →
deduplication → severity/evidence gate → fix owner. gstack adds adaptive gating
based on the historical usefulness of each specialist, but security and
migrations SHOULD remain insurance checks.

### Evaluator-optimizer

Freeze the rubric → producer → evaluator → actionable feedback → bounded retry
→ best-candidate selection → human review when ambiguous.

### Long-running workflow

Durable job manifest → heartbeat → checkpoints → resumable artifacts → timeout
and cancel → human input state → reconciliation after restart.

### Multi-repo change

Shared intent/spec repo → per-repo change owners/worktrees → versioned
interface contracts → integration environment → cross-repo verifier →
coordinated release.

## Checkpoint types

- **Decision** — multiple valid options that change the outcome.
- **Approval** — a risky action is ready for execution.
- **Input required** — credentials/data/external operation missing.
- **Verification** — automated checks are insufficient for human judgment.
- **Blocker** — a precondition is demonstrably unmet.

A checkpoint contains context, options, consequences, a recommendation,
evidence, and what continues after the answer.

## Pause/resume

Pause saves the current task, branch/worktree, commits, decisions, blockers,
active jobs, expected artifacts, and verify/resume commands. Resume checks for
drift and does not take old state on faith.
