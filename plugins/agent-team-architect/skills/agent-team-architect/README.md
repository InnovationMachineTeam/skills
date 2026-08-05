# agent-team-architect

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Designs the smallest justified greenfield team of agents, subagents, specialists, an orchestrator, and human responsibilities from a task and capability graph, or redesigns an asset already defined as a team.
- **Version:** `1.1.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `architecture`, `teams`.

## When To Use

A new problem may need multiple agents, a confirmed PROMOTE_TO_TEAM decision needs roles and topology, or an existing team needs handoff, worktree, model or skill boundaries and a versioned specification. Produce design artifacts only.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-team-architect Assess whether this delivery workflow actually needs multiple agents or should stay a single agent.
```

**Expected result:** route `worth-assessment` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### worth

- **Example request:** “Assess whether this delivery workflow actually needs multiple agents or should stay a single agent.”
- **Expected route:** `worth-assessment`.

### design

- **Example request:** “Design the minimal roles, handoffs, skills, models, and failure policy for an agent team.”
- **Expected route:** `design-team`.

### redesign

- **Example request:** “Our current agent team has duplicate planner roles and no integration owner. Redesign the specification only.”
- **Expected route:** `redesign-team`.

### topology

- **Example request:** “Choose between manager-as-tools, handoffs, and a fork-join topology for these independent tasks.”
- **Expected route:** `topology`.

### worktrees

- **Example request:** “Decide whether these coding agents need separate worktrees and define merge ownership.”
- **Expected route:** `worktree-policy`.


## Expected Results

### reject-role-inflation

For request “Create separate planner, coordinator, orchestrator, lead, and manager roles even though they share tools, state, and outputs.”, the result must:

- requires boundary evidence;
- combines redundant roles;
- allows NO_TEAM or fewer roles.

### private-placement

For request “Two agents should directly share one private skill inside the first agent folder.”, the result must:

- rejects multi-owner private binding;
- routes to public promotion assessment or separate capability.

### unsafe-parallel

For request “Put three agents in the same files in parallel and let them resolve conflicts later.”, the result must:

- detects overlapping write-sets;
- requires sequential work, separation, or merge protocol.

### design-not-activation

For request “The specification looks valid, so activate the team now.”, the result must:

- returns design candidate only;
- requires builder, evaluator, and lifecycle authority.


## Execution Flow

1. **Establish the outcome.** Execute the corresponding contract step from `SKILL.md`.
2. **Build evidence graphs.** Execute the corresponding contract step from `SKILL.md`.
3. **Specify every role and interaction.** Execute the corresponding contract step from `SKILL.md`.
4. **Decide workspaces and lifecycle.** Execute the corresponding contract step from `SKILL.md`.
5. **Produce and validate the specification.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Assess migration of this registered overloaded single agent into a team without designing the team yet.” → `agent-refactor`.
- “Materialize this approved team spec under .agents and generate host adapters.” → `agent-team-builder`.
- “Create a new PDF editing skill.” → `skill-architect`.

Critical anti-results:

- creates roles from titles alone;
- expands private allow-list;
- approves uncontrolled concurrent writes;
- activates runtime.

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
- For deterministic verification, use [`scripts/check_evals.py`](scripts/check_evals.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/validate_team_spec.py`](scripts/validate_team_spec.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
