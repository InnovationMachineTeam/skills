# Authoring and progressive disclosure

Practice-ID: BP-AUTHOR-001
Scope: mixed
Status: current
Sources: SRC-AS-002, SRC-ANT-001, SRC-OAI-001, SRC-LOCAL-001, SRC-DER-001
Last-rebuilt: 2026-07-30

## Start from evidence

Derive skills from real tasks, user corrections, runbooks, schemas, incidents, patches, traces, and recurring failures. Generic prompts tend to produce advice the model already knows. Record concrete positive triggers, near-miss negatives, observable outputs, and success criteria before scaffolding.

## Choose one coherent capability

Split when users, triggers, inputs, authority, state, side effects, owners, lifecycle, or completion criteria differ materially. Start narrow; consolidate only after coexistence and behavioral evals show no regression.

## Allocate context deliberately

Keep goal, boundary, inputs, outputs, invariants, core workflow, decisions, stop/approval gates, gotchas, resource-routing rules, and definition of done in SKILL.md. Move schemas, policies, long examples, rare variants, and detailed domain knowledge to references. Keep output templates and static reusable files in assets.

## Write for execution

- Use imperative instructions in the body.
- Give one recommended default plus a bounded exception.
- Use decision tables for material branches and checklists for long workflows.
- Explain non-obvious constraints, not common knowledge.
- Add scripts only for repeated deterministic or fragile work.
- Remove placeholders and generated clutter from release bundles.
- Never duplicate the same normative rule in multiple resources.

Match freedom to risk: high for analysis, medium for preferred patterns, low for migrations and consequential workflows, deterministic for mechanical transformations.
