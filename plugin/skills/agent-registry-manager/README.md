# agent-registry-manager

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Governs typed desired-state registries and versioned bindings for Agentic OS agents, skills, commands, workflows, teams, tools, models and policies, and reconciles them with observed host/runtime state.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `registry`, `governance`.

## When To Use

Inventory, candidate registration, optimistic transactions, drift detection, quarantine, deprecation, migration or retirement at platform scope. Do not equate registered with trusted or active, bypass ownership/private visibility, edit generated views as canonical data, or mutate on a stale revision.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-registry-manager Inventory desired and observed Agentic OS assets.
```

**Expected result:** route `inventory` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### inventory

- **Example request:** “Inventory desired and observed Agentic OS assets.”
- **Expected route:** `inventory`.

### reconcile

- **Example request:** “Reconcile registry drift at revisions 4 and 2.”
- **Expected route:** `reconcile`.


## Expected Results

### stale

For request “Apply a transaction based on a stale revision.”, the result must:

- rejects stale writer.

### private

For request “Bind a private skill to a second agent.”, the result must:

- rejects private escape and records evidence.


## Execution Flow

1. Check that the skill applies and that the inputs are complete.
2. Choose the narrowest safe route.
3. Create or verify the required artifacts.
4. Compare the result against the contract and deliver it with risks and the next step.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Install this public skill in Codex.” → `skill-manager`.

Critical anti-results:

- partially mutates registry;
- expands allow-list.

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
- For deterministic verification, use [`scripts/validate_reconcile_plan.py`](scripts/validate_reconcile_plan.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
