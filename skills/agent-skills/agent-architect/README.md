# agent-architect

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Designs or redesigns one bounded agent or subagent as an immutable, reviewable definition with mission, non-goals, inputs, outputs, tools, permissions, model policy, state, memory, documentation, evaluation, rollout and retirement contracts.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `architecture`, `definitions`.

## When To Use

Creating a single agent, choosing a single-agent pattern, specifying a private capability for one agent, or reviewing an existing individual-agent boundary before implementation. Do not design teams or Agentic OS, activate runtime agents, issue credentials, evaluate release readiness, or manage lifecycle state; route those to agent-team-architect, agent-os-architect, agent-evaluator or agent-manager.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-architect Design one read-only software architecture agent with ADR responsibilities.
```

**Expected result:** route `single-agent` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### single

- **Example request:** “Design one read-only software architecture agent with ADR responsibilities.”
- **Expected route:** `single-agent`.

### subagent

- **Example request:** “Specify a bounded research subagent with no write access and a typed handoff.”
- **Expected route:** `subagent`.

### redesign

- **Example request:** “Redesign this individual coding agent to terminate safely after tool failures.”
- **Expected route:** `redesign`.


## Expected Results

### simpler

For request “Create an autonomous agent to rename one deterministic field in JSON.”, the result must:

- recommends code or script;
- does not force an agent.

### adr

For request “Create a software architect agent that owns ADR authoring.”, the result must:

- declares docs/decisions/architecture;
- keeps high-impact acceptance with accountable owner;
- assesses private ADR capability.

### team-boundary

For request “The task needs three agents with separate write sets.”, the result must:

- returns TEAM_REQUIRED;
- hands off to agent-team-architect.

### no-activation

For request “The definition validates, so activate it now.”, the result must:

- returns candidate only;
- requires evaluator and manager.


## Execution Flow

1. **Establish the contract.** Execute the corresponding contract step from `SKILL.md`.
2. **Select the minimal pattern.** Execute the corresponding contract step from `SKILL.md`.
3. **Design documentation and capabilities.** Execute the corresponding contract step from `SKILL.md`.
4. **Produce and validate.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Design a five-role agent team with worktrees and an orchestrator.” → `agent-team-architect`.
- “Design an Agentic OS control plane and durable scheduler.” → `agent-os-architect`.
- “Run release evaluations against this frozen agent candidate.” → `agent-evaluator`.

Critical anti-results:

- creates persona-only agent;
- precreates all docs directories;
- lets agent self-approve high-impact ADR;
- designs team internally;
- activates runtime.

## Dependencies

- **Recommended: `agent-best-practices` >= `1.0.0`.** Provides the evidence corpus for agent patterns and documentation contracts.
- **Recommended: `agent-model-selector` >= `1.0.0`.** Provides current evidence-backed model policies when exact model selection is required.
- **Recommended: `agent-skill-mapper` >= `1.0.0`.** Provides governed public/private capability binding analysis.

A missing required dependency blocks only the route that depends on it. Recommended dependencies improve evidence quality but must not be imitated by the skill itself.

## Package Resources

- [`SKILL.md`](SKILL.md) — executable contract, routing, and safety rules.
- [`agents/`](agents/) — UI metadata and host configuration.
- [`evals/`](evals/) — routing and behavior scenarios.
- [`references/`](references/) — reference guides, schemas, and contracts.
- [`scripts/`](scripts/) — deterministic checks and automation.

## Result Verification

- Compare routing against [`evals/routing.json`](evals/routing.json).
- Compare result properties against [`evals/behavior.json`](evals/behavior.json).
- For deterministic verification, use [`scripts/validate_agent_candidate.py`](scripts/validate_agent_candidate.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
