# role-agent-architect

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Creates one complete bounded specialist-agent specification from an approved process-orchestrator role, including inherited-skill audit, capability gaps, role contract, knowledge, tools, permissions, tasks, handoffs, self-review, Human-in-the-loop, errors, context, metrics, evals, agent card, and system prompt.
- **Version:** `1.0.3`.
- **Visibility:** package-private: invoked only by its parent `agent-master` and not published separately.

## When To Use

Use the skill when the request matches its purpose and responsibility boundaries in `SKILL.md`.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

This package-private skill is not invoked directly. The illustrative request is passed through its parent `/agent-master`:

```text
/agent-master Agent-master dispatches the approved evidence-reviewer role with the orchestrator spec and its proposed skills.
```

**Expected result:** route `role-agent-architect` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.
Direct `/role-agent-architect` is not a supported public command; parent `agent-master` must pass a bounded dispatch contract and verify the result.

## Usage Variants

### approved-role

- **Example request:** “Agent-master dispatches the approved evidence-reviewer role with the orchestrator spec and its proposed skills.”
- **Expected route:** `role-agent-architect`.


## Expected Results

### skill-audit

For request “The orchestrator proposes six overlapping skills for one reviewer role.”, the result must:

- audits every proposed skill;
- explains merge, split, move, or exclusion;
- separates skills from knowledge, tools, rules, and authority.

### neighbor-boundary

For request “The role is an analyst, but the task asks it to approve a regulated release.”, the result must:

- refuses approval authority;
- creates a handoff or Human gate;
- preserves the analyst output.

### complete-package

For request “Create the specialist agent package for an approved role.”, the result must:

- returns role contract;
- returns input/output and handoff contracts;
- returns system prompt and agent card;
- returns eval cases.


## Execution Flow

1. **Verify the handoff.** Execute the corresponding contract step from `SKILL.md`.
2. **Audit inherited capabilities.** Execute the corresponding contract step from `SKILL.md`.
3. **Specify bounded behavior.** Execute the corresponding contract step from `SKILL.md`.
4. **Design interactions and recovery.** Execute the corresponding contract step from `SKILL.md`.
5. **Evaluate and hand off.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Create some useful agents for my company.” → `agent-master`.
- “Turn the approved evidence-triangulation capability into a skill package.” → `role-skill-architect`.

Critical anti-results:

- silently drops capabilities;
- copies every proposal unchanged;
- impersonates the approver;
- claims runtime activation.

## Dependencies

There are no external catalog dependencies. Parent `agent-master` passes only a bounded dispatch envelope to this private skill and verifies its result.

## Package Resources

- [`SKILL.md`](SKILL.md) — executable contract, routing, and safety rules.
- [`evals/`](evals/) — routing and behavior scenarios.
- [`references/`](references/) — reference guides, schemas, and contracts.

## Result Verification

- Compare routing against [`evals/routing.json`](evals/routing.json).
- Compare result properties against [`evals/behavior.json`](evals/behavior.json).
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
