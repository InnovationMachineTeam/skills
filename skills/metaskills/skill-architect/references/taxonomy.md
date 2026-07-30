# Skill Archetype Taxonomy

## Contents

- Classification method
- Eight primary archetypes
- Hybrid and split rules
- Confidence and clarification

## Classification method

Classify by the mechanism that most determines architecture, risk, and evaluation—not by the business domain. A finance skill may be reference, tool-integration, evaluation, or workflow depending on what it must do.

Extract these signals:

| Signal | Diagnostic question |
|---|---|
| Source of value | Does value come from knowledge, procedure, tools, deterministic code, assets, judgment, or coordination? |
| Repetition | What would otherwise be rediscovered or rewritten each time? |
| Fragility | Which step becomes unsafe or inconsistent if left to free-form reasoning? |
| Side effects | Does the skill only advise, or can it mutate files, systems, or people? |
| Output | Is the output advice, an action, an artifact, a verdict, or another skill? |
| Composition | Does one agent do the work, or route/delegate to several capabilities? |

Choose the type that governs the hardest constraint. Record other signals as secondary traits.

## Eight primary archetypes

### 1. Knowledge/reference

Use when the main value is specialized, proprietary, structured, or hard-to-recall knowledge. Typical inputs include policies, schemas, glossaries, domain rules, and curated research.

Strong signals:

- answers depend on a stable corpus;
- the procedure is simple but the facts are specialized;
- progressive loading and source provenance matter more than execution.

Do not choose this type when current data must come from an API or when a fragile sequence is the main value.

### 2. Workflow/procedure

Use when the main value is a repeatable sequence with decisions, checkpoints, validation, and recovery. Typical examples include incident response, planning, migrations, or editorial workflows.

Strong signals:

- order and state transitions matter;
- the agent must branch on conditions;
- success requires more than knowing facts.

### 3. Tool integration

Use when the skill's purpose is operating a CLI, SDK, API, MCP server, database, or external service.

Strong signals:

- capability discovery, authentication, schemas, rate limits, or error classes matter;
- actions may change external state;
- current official documentation is required.

### 4. Script-backed automation

Use when repeated code, exact transformations, validation, or fragile operations should be deterministic.

Strong signals:

- the same implementation would otherwise be regenerated;
- byte-level, numeric, structural, or sequence accuracy matters;
- a stable CLI contract can encapsulate complexity.

### 5. Artifact/template production

Use when the output is a reusable document, presentation, workbook, image, code scaffold, or other formatted artifact.

Strong signals:

- assets or boilerplate are central;
- formatting preservation or render verification matters;
- the skill transforms a template into a deliverable.

### 6. Evaluation/review

Use when the primary output is a diagnosis, score, quality gate, risk finding, or accept/reject recommendation.

Strong signals:

- rubrics, fixtures, evidence, calibration, and severity matter;
- the evaluator should not silently fix the subject;
- independent or blinded judgment improves validity.

### 7. Orchestration/composition

Use when a skill coordinates multiple agents, skills, tools, or stages to achieve one outcome.

Strong signals:

- work can be decomposed into bounded independent tasks;
- ownership, fan-out/fan-in, shared state, or partial failure matter;
- no single specialist contains the full workflow.

### 8. Meta/router

Use when the skill classifies intent, selects or creates other skills, optimizes prompts, or manages the skill system itself.

Strong signals:

- the output is a route, another skill, or an improved control artifact;
- description quality and dispatch precision are first-class;
- ambiguity handling and recursion guards matter.

## Hybrid and split rules

- Keep one primary archetype and any number of secondary traits.
- Compose base behavior with one archetype-specific contract; do not concatenate every prompt.
- Split when the candidate skill has unrelated triggers, separate permissions, different resources, or incompatible completion criteria.
- Prefer a router plus focused skills over one broad skill that tries to own every domain.
- Prefer a workflow skill with a small script over a script skill when judgment and branching remain dominant.
- Prefer tool integration over workflow when external capability contracts and mutation safety dominate.
- Prefer evaluation over workflow when the observable output is a verdict rather than a changed artifact.

## Confidence and clarification

Report classification confidence as:

- **High**: one archetype clearly governs architecture and tests;
- **Medium**: primary type is likely but secondary traits are substantial;
- **Low**: multiple types imply materially different bundles or the outcome is missing.

At low confidence, ask the single question that most separates the leading candidates. Do not ask the user to choose jargon-heavy archetype names when a concrete outcome question would be easier.

