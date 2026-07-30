---
name: skill-architect
description: Classifies skill ideas and supplied material, chooses among knowledge, workflow, tool-integration, script-backed, artifact-template, evaluator, orchestrator, and meta/router archetypes, then designs, creates, or updates the skill through a routed master prompt. Use when the user explicitly invokes $skill-architect, asks for skill-archetype classification or an architecture/resource decision, requests the routed master-prompt workflow, or arrives through an exact creation handoff from skill-builder, skill-scout, skill-harvester, or skill-refactor. Do not claim generic unnamed “create or update a skill” requests that need no architecture decision; leave those to the bundled skill-creator. Route independent evaluation of an existing skill to skill-evaluator, opportunity discovery to skill-scout, research extraction to skill-harvester, topology changes to skill-refactor, lifecycle changes to skill-manager, and end-to-end productionization to skill-builder.
metadata:
  version: "1.0.0"
---

# Architect Agent Skills

Convert an idea or supplied material into a minimal, installable, tested skill. Classify first, ask only material questions, then load the shared creation contract and exactly one primary archetype prompt.

## Intake

Treat any of the following as input:

- a skill idea or desired outcome;
- example user requests or counterexamples;
- an existing skill to update;
- prompts, specifications, source code, documents, schemas, or tool descriptions;
- a repository or folder explicitly placed in scope.

If no usable input is supplied, ask the user what capability the skill should add. Start with one to three high-information questions from [references/clarification.md](references/clarification.md). Do not create files until the intended capability is sufficiently clear.

If input exists, extract the objective, trigger examples, expected outputs, target hosts, tools, side effects, risk, reusable resources, and installation intent. Ask a focused question only when a missing answer materially changes the skill boundary, architecture, authority, destination, or irreversible behavior. Otherwise state a safe assumption and proceed.

For a new skill, resolve the destination before scaffolding. If no location is specified, ask whether to create a reviewable project bundle or install it into the host's discoverable skills directory. Do not install globally or overwrite an existing skill by assumption.

## Classify the skill

Read [references/taxonomy.md](references/taxonomy.md). Select one primary archetype:

| Archetype | Route |
|---|---|
| Knowledge/reference | [prompts/knowledge-reference.md](prompts/knowledge-reference.md) |
| Workflow/procedure | [prompts/workflow-procedure.md](prompts/workflow-procedure.md) |
| Tool integration | [prompts/tool-integration.md](prompts/tool-integration.md) |
| Script-backed automation | [prompts/script-automation.md](prompts/script-automation.md) |
| Artifact/template production | [prompts/artifact-template.md](prompts/artifact-template.md) |
| Evaluation/review | [prompts/evaluation-review.md](prompts/evaluation-review.md) |
| Orchestration/composition | [prompts/orchestration.md](prompts/orchestration.md) |
| Meta/router | [prompts/meta-router.md](prompts/meta-router.md) |

Record secondary traits rather than forcing every hybrid into a new type. Choose the archetype that determines the skill's hardest design constraint. Examples:

- an API workflow with fragile helper code is primarily **Tool integration**, secondarily **Script-backed**;
- a document generator with a branded file is primarily **Artifact/template**, secondarily **Workflow**;
- a dispatcher that invokes several specialists is primarily **Meta/router** or **Orchestration**, not a mega-skill containing every workflow.

Split the request into multiple cooperating skills when triggers, resources, permissions, or evaluation criteria are materially different. Ask the user before a split that changes the requested product surface.

If two primary types remain equally plausible and would produce different structures, ask one discriminating question. Otherwise continue and report the classification with a short rationale.

## Launch the routed master prompt

Read [prompts/base.md](prompts/base.md) completely, then read the selected archetype prompt completely. Treat the two files as one creation contract; the archetype prompt overrides the base only within its named specialty.

Load additional references only when needed:

- [references/clarification.md](references/clarification.md) for incomplete or ambiguous requests;
- [references/resource-design.md](references/resource-design.md) when deciding among scripts, references, assets, or host integrations;
- [references/quality-and-evaluation.md](references/quality-and-evaluation.md) when designing tests or reviewing a high-risk skill;
- [references/portability-and-security.md](references/portability-and-security.md) when hosts, enterprise controls, external data, credentials, or side effects matter.

Do not merely reproduce the master prompt. Execute its workflow to create or update the skill.

## Build the skill

1. Define concrete trigger examples, non-trigger examples, observable outputs, scope, and risk.
2. Plan only reusable resources that reduce repeated reasoning, improve reliability, or provide output assets.
3. For a new skill, use the host's official skill initializer when available. Generate `agents/openai.yaml` from the finished skill contract rather than inventing optional metadata.
4. Create resources before finalizing `SKILL.md`, so instructions can point to real files.
5. Keep `SKILL.md` procedural and concise. Put detailed or conditional material one level away in resources.
6. Test every added executable on representative positive and failure cases.
7. Run structural validation and behavioral checks proportional to risk.
8. Forward-test complex skills with fresh context and without leaking the expected answer.
9. Iterate until blocking defects are resolved or explicitly reported.

Preserve unrelated user files. Do not overwrite an existing skill until its identity and intended update scope are confirmed. Prefer a proposal or separate output bundle when authority is unclear.

## Validate

Run the host's official validator when one exists. Also run the bundled portable check:

```bash
python3 scripts/validate_skill.py path/to/skill
```

Use JSON diagnostics when integrating with automation:

```bash
python3 scripts/validate_skill.py path/to/skill --format json
```

Treat mechanical checks as a floor, not proof of behavioral quality. Use [evals/routing.json](evals/routing.json) for trigger and classification tests and [evals/behavior.json](evals/behavior.json) for functional and adversarial behavior.

For substantial, high-risk, or release-bound bundles, hand the immutable candidate to `skill-evaluator` for an independent plan, holdout, layered verdict, and catalog-level evidence. The **Evaluation/review** archetype above creates a skill whose product is evaluation; it does not make architect the independent evaluator of the bundle being created.

## Deliver

Report:

1. primary classification and secondary traits;
2. material assumptions or user decisions;
3. created or changed files;
4. validation and forward-test evidence;
5. unresolved risks or required next step;
6. installation status.

Do not claim that a skill is installed, portable, safe, or improved unless that property was actually verified. Do not add README, changelog, installation guide, or other auxiliary files unless the target skill format explicitly requires them.
