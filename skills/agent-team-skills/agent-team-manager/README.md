# agent-team-manager

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** >-.
- **Version:** `1.2.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `orchestration`, `lifecycle`.

## When To Use

Use the skill when the request matches its purpose and responsibility boundaries in `SKILL.md`.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-team-manager Do we need a team of agents for this repository migration?
```

**Expected result:** route `assess` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### assess

- **Example request:** “Do we need a team of agents for this repository migration?”
- **Expected route:** `assess`.

### design

- **Example request:** “Coordinate the design of a new agent team.”
- **Expected route:** `design`.

### build

- **Example request:** “Take this approved team spec through the build phase.”
- **Expected route:** `build`.

### map

- **Example request:** “Reconcile skills and agents before launch.”
- **Expected route:** `map-capabilities`.

### operate

- **Example request:** “Launch and monitor the approved team run.”
- **Expected route:** `operate`.

### change

- **Example request:** “Change the active team topology safely.”
- **Expected route:** `change`.

### recover

- **Example request:** “Recover a partially failed team run.”
- **Expected route:** `recover`.

### retire

- **Example request:** “Retire this team and preserve its evidence.”
- **Expected route:** `retire`.


## Expected Results

### thin-facade

For request “Design, build and run a team.”, the result must:

- delegates design, build and runtime execution to owning specialists;
- routes worktrees to agent-workspace-manager;
- maintains typed handoffs and run state.

### authority

For request “Run the team and publish whatever it creates.”, the result must:

- separates operation from publication authority;
- records human checkpoints.

### recovery

For request “The build failed after some writes.”, the result must:

- contains writes;
- preserves evidence;
- selects rollback or validated resume.


## Execution Flow

1. **Verify companion skills.** Execute the corresponding contract step from `SKILL.md`.
2. **Assess and route.** Execute the corresponding contract step from `SKILL.md`.
3. **Maintain durable state.** Execute the corresponding contract step from `SKILL.md`.
4. **Coordinate execution.** Execute the corresponding contract step from `SKILL.md`.
5. **Verify and close.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Optimize this one SKILL.md.” → `skill-optimizer`.

Critical anti-results:

- reimplements specialist contracts;
- infers destructive or external authority;
- loops indefinitely.

## Dependencies

- **Required: `agent-model-selector` >= `1.0.0`.** The design route delegates current model selection and evidence.
- **Required: `agent-skill-mapper` >= `1.0.0`.** The map-capabilities route delegates governed agent-skill bindings.
- **Required: `agent-team-architect` >= `1.1.0`.** The design route delegates team architecture.
- **Required: `agent-team-builder` >= `1.0.0`.** The build route delegates staged team materialization.
- **Required: `agent-team-orchestrator` >= `1.0.0`.** The operate route delegates runtime task orchestration.
- **Recommended: `agent-workspace-manager` >= `1.0.0`.** Recommended when an operation needs isolated worktrees or workspace lifecycle management.

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
- For deterministic verification, use [`scripts/check_evals.py`](scripts/check_evals.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/validate_run_state.py`](scripts/validate_run_state.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
