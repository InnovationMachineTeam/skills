# prompt-optimize

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Designs, audits and improves durable system, developer and agent prompts governing roles, instruction priority, tools, autonomy, safety, validation and outputs.
- **Version:** `3.0.4`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `prompts`, `optimization`.

## When To Use

Prompt creation, rewriting, consolidation, linting, evaluation, migration or conflict resolution. Not for ordinary copyediting, one-off content prompts or executing the governed task unless its controlling prompt is the requested artifact.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/prompt-optimize The scenario is described by its identifier and expected route in the eval corpus.
```

**Expected result:** route `the skill's primary route` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

- Explicitly invoke the skill to execute the primary contract from `SKILL.md`.
- Audit or planning without changing files when write authority is not granted.
- Apply allowed changes followed by result verification and rollback description.

## Expected Results

- the result matches the stated contract and clearly separates facts from assumptions;
- modified artifacts are listed, and completed checks are named without invented PASS results;
- constraints, residual risks, rollback status, and the next step are stated explicitly.

## Execution Flow

1. **Select the operation.** Execute the corresponding contract step from `SKILL.md`.
2. **Protect authority and intent.** Execute the corresponding contract step from `SKILL.md`.
3. **Load supporting guidance.** Execute the corresponding contract step from `SKILL.md`.
4. **Workflow.** Execute the corresponding contract step from `SKILL.md`.
5. **Quality gates.** Execute the corresponding contract step from `SKILL.md`.
6. **Anti-patterns.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The skill must not expand the authority it received, hide skipped checks, perform irreversible or external actions without explicit permission, or claim host state solely from the presence of files.

## Dependencies

No required companion skills are declared in the canonical dependency graph. Check the availability of host tools and resources referenced by `SKILL.md`.

## Package Resources

- [`SKILL.md`](SKILL.md) — executable contract, routing, and safety rules.
- [`agents/`](agents/) — UI metadata and host configuration.
- [`assets/`](assets/) — templates and reusable artifacts.
- [`references/`](references/) — reference guides, schemas, and contracts.
- [`scripts/`](scripts/) — deterministic checks and automation.

## Result Verification

- For deterministic verification, use [`scripts/lint_prompt.py`](scripts/lint_prompt.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
