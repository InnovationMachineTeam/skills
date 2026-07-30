---
name: skill-architect
description: Classifies skill ideas and supplied material, selects an archetype and the minimum viable placement—inline instruction, private agent command, private agent skill, or public skill—then designs, creates, registers, or updates the capability through routed master prompts. Use when the user explicitly invokes $skill-architect, asks for skill-archetype, resource, visibility, placement, or registration decisions, requests the routed master-prompt workflow, or arrives through an exact creation handoff from skill-builder, skill-scout, skill-harvester, or skill-refactor. Do not claim generic unnamed “create or update a skill” requests that need no architecture decision; leave those to the bundled skill-creator. Route independent evaluation of an existing skill to skill-evaluator, opportunity discovery to skill-scout, research extraction to skill-harvester, topology or visibility migration to skill-refactor, lifecycle changes to skill-manager, and end-to-end productionization to skill-builder.
metadata:
  version: "1.2.0"
---

# Architect Agent Skills

Convert an idea or supplied material into the smallest auditable capability that satisfies it. Classify mechanism and visibility separately, ask only material questions, then load the shared creation contract, exactly one primary archetype prompt, and the placement profile when a skill or private command is justified.

## Intake

Treat any of the following as input:

- a skill idea or desired outcome;
- example user requests or counterexamples;
- an existing skill to update;
- prompts, specifications, source code, documents, schemas, or tool descriptions;
- a repository or folder explicitly placed in scope.

If no usable input is supplied, ask the user what capability the skill should add. Start with one to three high-information questions from [references/clarification.md](references/clarification.md). Do not create files until the intended capability is sufficiently clear.

If input exists, extract the objective, trigger examples, expected outputs, target hosts, tools, side effects, risk, reusable resources, and installation intent. Ask a focused question only when a missing answer materially changes the skill boundary, architecture, authority, destination, or irreversible behavior. Otherwise state a safe assumption and proceed.

For a new capability, resolve the destination and intended consumers before scaffolding. If no location is specified, ask whether to create a reviewable project bundle, an agent-private capability, or install a public skill into the host's discoverable skills directory. A private capability requires an exact owner agent. Do not install globally, make a capability globally discoverable, or overwrite an existing asset by assumption.

## Choose the minimum capability form

Read [references/visibility-and-registry.md](references/visibility-and-registry.md). Decide before archetype scaffolding:

| Form | Use when |
|---|---|
| Inline instruction | One short, stable rule has no independent resources, tests, or lifecycle. |
| Private command | One agent needs a narrow named action or template, but not a complete skill lifecycle. |
| Private agent skill | One agent needs a reusable multi-step capability with resources, scripts, or evals. |
| Public skill | Multiple independent consumers need it, or it has an independent owner, lifecycle, and reusable contract. |
| Tool/script | The hard part is deterministic execution rather than model guidance. |
| Workflow | Durable multi-stage state and coordination dominate the capability. |

Treat `private` as agent-scoped discovery and authorization, not confidentiality. Folder placement alone is never a security boundary. A private skill remains reviewable and independently versioned. A private command inherits its owning agent's SemVer and keeps only a revision and content hash. Both are registered and subject to repository access controls.

For this repository convention, public project skills live under `skills/<category>/<skill>/` or `.agents/skills/<skill>/`; private capabilities live under `.agents/definitions/<agent-id>/skills/<skill>/` or `.agents/definitions/<agent-id>/commands/<command>.md`. Use a host adapter when the runtime requires another layout. Global discovery must exclude the canonical private roots.

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

Read [prompts/base.md](prompts/base.md) completely, then read the selected archetype prompt completely. Treat the two files as one creation contract; the archetype prompt overrides the base only within its named specialty. If the result is a public or private skill, or a private command, also read [prompts/placement-and-registration.md](prompts/placement-and-registration.md) as a visibility profile. It does not replace the primary archetype.

Load additional references only when needed:

- [references/clarification.md](references/clarification.md) for incomplete or ambiguous requests;
- [references/resource-design.md](references/resource-design.md) when deciding among scripts, references, assets, or host integrations;
- [references/quality-and-evaluation.md](references/quality-and-evaluation.md) when designing tests or reviewing a high-risk skill;
- [references/portability-and-security.md](references/portability-and-security.md) when hosts, enterprise controls, external data, credentials, or side effects matter;
- [references/visibility-and-registry.md](references/visibility-and-registry.md) for placement, owner scope, registration, promotion, or demotion.

Do not merely reproduce the master prompt. Execute its workflow to create or update the skill.

## Build the skill

1. Define concrete trigger examples, non-trigger examples, observable outputs, intended consumers, visibility, scope, and risk.
2. Plan only reusable resources that reduce repeated reasoning, improve reliability, or provide output assets.
3. For a new skill, use the host's official skill initializer when available. Generate `agents/openai.yaml` from the finished skill contract rather than inventing optional metadata.
4. Create resources before finalizing `SKILL.md`, so instructions can point to real files.
5. Keep `SKILL.md` procedural and concise. Put detailed or conditional material one level away in resources.
6. Test every added executable on representative positive and failure cases.
7. Run structural validation and behavioral checks proportional to risk.
8. Register every created skill or command as a candidate in `docs/AGENT-ASSET-REGISTRY.json` with identity, version strategy, revision, hash, visibility, scope, locator, technical owner, accountable human/team owner, consumers, provenance, trust, and lifecycle fields. Update `docs/AGENT-SKILLS-MAP.json` in the same revision-checked transaction.
9. Verify that public discovery excludes private roots and that only the owning agent can bind a private capability. A second independent consumer requires a promotion assessment, not an expanded private allow-list.
10. Forward-test complex skills with fresh context and without leaking the expected answer.
11. Iterate until blocking defects are resolved or explicitly reported.

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

For visibility-aware bundles, include negative access cases: global search must not surface private assets, another agent must not bind them, and a missing owner or failed registry transaction must fail closed. Also test private-to-public promotion with consumer inventory, a generalized owner-independent contract, independent lifecycle justification, versioning, registry/map migration, and rollback.

For substantial, high-risk, or release-bound bundles, hand the immutable candidate to `skill-evaluator` for an independent plan, holdout, layered verdict, and catalog-level evidence. The **Evaluation/review** archetype above creates a skill whose product is evaluation; it does not make architect the independent evaluator of the bundle being created.

## Deliver

Report:

1. primary classification, secondary traits, and chosen capability form;
2. visibility, scope, owner agent, allowed consumers, and discovery enforcement;
3. material assumptions or user decisions;
4. created or changed files plus registry/map entries;
5. validation, access-control, and forward-test evidence;
6. unresolved risks or required next step;
7. installation and activation status.

Do not claim that a skill is installed, portable, safe, or improved unless that property was actually verified. Do not add README, changelog, installation guide, or other auxiliary files unless the target skill format explicitly requires them.
