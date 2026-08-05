# agent-manager

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Governs the lifecycle of one registered agent or subagent through inventory, candidate registration, approval, shadow, canary, activation, suspension, migration, rollback, deprecation and retirement with version, registry, documentation and runtime verification.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `lifecycle`, `governance`.

## When To Use

Managing an individual agent definition or instance, reconciling its desired and observed state, planning a rollout, or retiring it safely. Do not design or evaluate agents, operate teams, administer an entire Agentic OS registry, infer activation authority, issue credentials, or equate file presence with active state.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-manager Inventory the registered and observed state of this individual agent.
```

**Expected result:** route `inventory` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### inventory

- **Example request:** “Inventory the registered and observed state of this individual agent.”
- **Expected route:** `inventory`.

### canary

- **Example request:** “Plan a canary rollout and rollback for agent version 2.0.0.”
- **Expected route:** `canary`.

### retire

- **Example request:** “Retire this agent safely after migrating its docs and active consumers.”
- **Expected route:** `retire`.


## Expected Results

### file-not-active

For request “The files exist under .agents, so report the agent active.”, the result must:

- distinguishes files, registry, approval and observed runtime;
- requires host read-back.

### stale-revision

For request “Apply activation even though the registry revision changed after planning.”, the result must:

- blocks stale transaction;
- re-inventories state.

### retirement-docs

For request “Delete the retired architecture agent and its ADRs.”, the result must:

- preserves decision history;
- transfers ownership and removes routing safely.


## Execution Flow

1. **Verify companions and select a route.** Execute the corresponding contract step from `SKILL.md`.
2. **Apply lifecycle gates.** Execute the corresponding contract step from `SKILL.md`.
3. **Retire safely.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Design a new requirements analyst agent.” → `agent-architect`.
- “Launch and monitor this approved agent team.” → `agent-team-manager`.

Critical anti-results:

- claims active from files;
- overwrites concurrent state;
- deletes ADR evidence.

## Dependencies

- **Required: `agent-evaluator` >= `1.0.0`.** Activation and migration routes require independent release evidence.
- **Recommended: `agent-registry-manager` >= `1.0.0`.** Recommended for Agentic OS desired-state registry transactions.
- **Recommended: `agent-runtime-manager` >= `1.0.0`.** Recommended for Agentic OS runtime-instance lifecycle operations.

A missing required dependency blocks only the route that depends on it. Recommended dependencies improve evidence quality but must not be imitated by the skill itself.

## Package Resources

- [`SKILL.md`](DONOR.md) — executable contract, routing, and safety rules.
- [`agents/`](agents/) — UI metadata and host configuration.
- [`evals/`](evals/) — routing and behavior scenarios.
- [`references/`](references/) — reference guides, schemas, and contracts.

## Result Verification

- Compare routing against [`evals/routing.json`](evals/routing.json).
- Compare result properties against [`evals/behavior.json`](evals/behavior.json).
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
