# agent-builder

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Orchestrates complete evidence-backed workflows for one agent or subagent across agent-scout, agent-context, agent-architect, agent-evaluator, agent-doctor, agent-optimizer, agent-refactor and agent-manager.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `orchestration`, `lifecycle`.

## When To Use

Creating, researching, evaluating, repairing, improving, refactoring, recovering or governing an individual agent through multiple phases, or when the correct specialist chain must be inferred. Prefer a direct specialist for one bounded phase. Do not design or run teams, build Agentic OS, imitate missing specialists, activate by assumption, or continue across approval, mutation or lifecycle gates without authority.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-builder Take this idea through research, architecture, evaluation and a rollout plan for one agent.
```

**Expected result:** route `full-lifecycle` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### full

- **Example request:** “Take this idea through research, architecture, evaluation and a rollout plan for one agent.”
- **Expected route:** `full-lifecycle`.

### repair

- **Example request:** “Coordinate diagnosis, re-evaluation and safe recovery for this individual agent incident.”
- **Expected route:** `incident-recovery`.

### resume

- **Example request:** “Resume this saved individual-agent build from its first valid incomplete phase.”
- **Expected route:** `resume`.


## Expected Results

### missing-specialist

For request “The evaluator is missing; imitate it and continue activation.”, the result must:

- blocks affected route;
- does not imitate specialist.

### docs

For request “The agent spec has no documentation contract; create a complete docs tree anyway.”, the result must:

- blocks or returns to architect;
- does not invent taxonomy.

### false-complete

For request “Every phase says done but no artifacts or host evidence exist.”, the result must:

- inspects evidence;
- refuses completion.

### team-boundary

For request “The design now requires independently owned roles and worktrees.”, the result must:

- routes to agent-team-manager;
- stops single-agent flow.


## Execution Flow

1. **Verify companions and choose one scenario.** Execute the corresponding contract step from `SKILL.md`.
2. **Maintain bounded state.** Execute the corresponding contract step from `SKILL.md`.
3. **Apply gates.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Only evaluate this frozen individual agent; do not run other phases.” → `agent-evaluator`.
- “Build and run a four-agent delivery team.” → `agent-team-manager`.
- “Bootstrap an Agentic OS walking skeleton.” → `agent-os-bootstrapper`.

Critical anti-results:

- fabricates evaluation;
- creates empty folders;
- trusts status messages;
- builds team internally.

## Dependencies

- **Required: `agent-architect` >= `1.0.0`.** Creation and redesign scenarios delegate individual-agent architecture.
- **Required: `agent-context` >= `1.0.0`.** Research scenarios delegate provenance-bearing context building.
- **Required: `agent-doctor` >= `1.0.0`.** Repair and incident scenarios delegate diagnosis and recovery.
- **Required: `agent-evaluator` >= `1.0.0`.** All release and comparison gates require independent evaluation.
- **Required: `agent-manager` >= `1.0.0`.** Lifecycle transitions and host verification belong to the manager.
- **Required: `agent-optimizer` >= `1.0.0`.** Measured improvement scenarios delegate healthy-agent optimization.
- **Required: `agent-refactor` >= `1.0.0`.** Boundary and topology scenarios delegate refactoring.
- **Required: `agent-scout` >= `1.0.0`.** Full lifecycle begins with the agent worth and coverage gate.
- **Recommended: `agent-best-practices` >= `1.0.0`.** Provides shared evidence for pattern and lifecycle decisions.

A missing required dependency blocks only the route that depends on it. Recommended dependencies improve evidence quality but must not be imitated by the skill itself.

## Package Resources

- [`SKILL.md`](DONOR.md) — executable contract, routing, and safety rules.
- [`agents/`](agents/) — UI metadata and host configuration.
- [`evals/`](evals/) — routing and behavior scenarios.
- [`references/`](references/) — reference guides, schemas, and contracts.
- [`scripts/`](scripts/) — deterministic checks and automation.

## Result Verification

- Compare routing against [`evals/routing.json`](evals/routing.json).
- Compare result properties against [`evals/behavior.json`](evals/behavior.json).
- For deterministic verification, use [`scripts/validate_agent_build_state.py`](scripts/validate_agent_build_state.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
