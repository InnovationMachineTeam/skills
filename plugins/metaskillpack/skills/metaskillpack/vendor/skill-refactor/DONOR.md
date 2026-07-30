---
name: skill-refactor
description: Assesses and safely changes capability boundaries and visibility across existing SKILL.md-based agent skills by composing, merging, splitting, extracting references or subskills, promoting private skills to public, demoting unused public skills to agent-private, and creating compatibility facades. Use when a user asks whether skills should be combined, divided, extracted, shared across agents, narrowed to one agent, or migrated while preserving triggers, authority, resources, tests, consumers, registry bindings, and rollback. Produce an evidence-backed boundary decision before mutation. Do not use for read-only comparison alone, independent evaluation, ordinary optimization, new unrelated skill creation, or installation; route those to skill-harvester, skill-evaluator, skill-optimizer, skill-architect, or skill-manager.
metadata:
  version: "1.1.0"
---

# Refactor Skill Boundaries

Change skill topology only when evidence shows that current boundaries are wrong. Prefer composition, references, or explicit routing over a universal mega-skill.

## Establish scope and authority

Accept one or more exact skill folders, boundary reports, comparison reports, consumer inventories, desired outcomes, and destination roots. Determine target hosts, current consumers, compatibility requirements, allowed files, preserved behavior, and whether the user authorizes only planning or exact mutations.

If no usable targets are supplied, ask for the skill paths, desired outcome, and mutation authority. Default to read-only assessment. Do not scan broad roots or modify installed copies by assumption.

## Keep role boundaries

- Use `skill-harvester` for read-only pairwise comparison and reusable-pattern extraction.
- Use `skill-architect` when the request is a new unrelated capability.
- Use `skill-doctor` when a target is broken, unsafe, or inconsistent.
- Use `skill-optimizer` for measured improvement without changing capability topology.
- Use `skill-evaluator` for independent old/new routing, coexistence, consumer, and regression evidence.
- Use `skill-manager` for versions, installation, activation, conflicts, retirement, and rollout.
- Use `skill-builder` when comparison, topology change, creation, verification, migration, and lifecycle rollout must be orchestrated as one resumable scenario.

Refactoring may invoke `skill-architect` or `skill-optimizer` through a bounded handoff, but final topology and migration approval remain here and with the user.

## Capture a structural baseline

Run read-only analysis on exact targets:

```bash
python3 scripts/analyze_boundaries.py SKILL_DIR [SKILL_DIR ...] --output boundaries-before.json
```

Record declared identity, description, headings, files, hashes, prompts, references, scripts, evals, links, dependencies, tools, consumers, host state, and existing tests. Static structure cannot prove semantic cohesion or active host routing.

## Decide before changing

Read [references/boundary-model.md](references/boundary-model.md). Choose exactly one primary decision:

- `KEEP_SEPARATE`
- `COMPOSE`
- `MERGE`
- `SPLIT`
- `EXTRACT_REFERENCE`
- `EXTRACT_SUBSKILL`
- `CREATE_FACADE`
- `PROMOTE_PUBLIC`
- `DEMOTE_PRIVATE`

Evaluate trigger cohesion, user outcome, workflow and state, permissions, tools, resources, context architecture, evaluation criteria, ownership, release cadence, consumers, and failure blast radius.

Different permissions, users, lifecycle, or completion criteria strongly favor separation or composition. Shared wording, topic, files, or authorship is not sufficient reason to merge.

## Select one primary route

| Route | Prompt |
|---|---|
| Boundary assessment | [prompts/boundary-assessment.md](prompts/boundary-assessment.md) |
| Composition | [prompts/compose.md](prompts/compose.md) |
| Physical merge | [prompts/merge.md](prompts/merge.md) |
| Split or subskill extraction | [prompts/split-extract.md](prompts/split-extract.md) |
| Reference extraction | [prompts/reference-extraction.md](prompts/reference-extraction.md) |
| Facade and migration | [prompts/facade-migration.md](prompts/facade-migration.md) |
| Public/private visibility migration | [prompts/visibility-migration.md](prompts/visibility-migration.md) |

Read [prompts/base.md](prompts/base.md) completely, then the selected route prompt. Load relevant references:

- [references/composition-and-merge.md](references/composition-and-merge.md) before combining skills;
- [references/split-and-extract.md](references/split-and-extract.md) before dividing a skill;
- [references/compatibility-and-migration.md](references/compatibility-and-migration.md) for consumers, aliases, and rollout;
- [references/evaluation-and-acceptance.md](references/evaluation-and-acceptance.md) for before/after evidence;
- [references/output-schema.md](references/output-schema.md) for a machine-readable plan;
- [references/visibility-migration.md](references/visibility-migration.md) for owner scope, registry/map changes, and promotion/demotion gates.

Execute the combined prompt rather than returning it.

## Preview a refactor plan

Before mutation, create a plan containing exact inputs and hashes, decision, rationale, output topology, trigger ownership, resource ownership, file operations, consumer migrations, preserved invariants, tests, rollback, and approval status.

Validate it:

```bash
python3 scripts/validate_refactor_plan.py refactor-plan.json
```

Show every create, update, move, copy, keep, and delete operation. Reconfirm if targets, permissions, consumers, or effects differ from authorization. Prefer recoverable copy/stage/facade operations over destructive moves or deletion.

## Apply safely

- Preserve unrelated and concurrent user changes.
- Stage new topology outside active discovery roots when practical.
- Keep one owner for each trigger, resource, script, and mutable state.
- Do not union permissions merely because skills are merged.
- Do not duplicate changing knowledge across new skills.
- Update relative links and resource routing deterministically.
- Preserve old entry points with a facade or explicit migration when consumers may depend on them.
- Do not remove the original until replacement discovery, routing, behavior, consumers, and rollback are verified.
- Never implement promotion or demotion as a folder move alone; migrate registry and binding identities, host adapters, consumers, and owner-agent versions.

Use `skill-architect` to scaffold newly extracted skill packages when needed, then apply the approved migration plan. Use `skill-manager` for activation and retirement.

For substantial topology changes, hand immutable baseline and candidate bundles to `skill-evaluator`. Refactor owns the boundary decision and file/migration changes; evaluator owns independent catalog coexistence, old/new routing, consumer E2E, holdout, and blocking-regression verdicts.

## Verify topology and behavior

After authorized changes:

1. regenerate the structural report;
2. compare reports:

```bash
python3 scripts/compare_boundaries.py boundaries-before.json boundaries-after.json
```

3. run official validators and link/resource checks;
4. run original and new routing, behavior, security, failure, and portability cases;
5. verify consumers and actual host discovery;
6. test facade behavior and rollback;
7. forward-test substantial boundary changes with fresh context.

Filesystem success and reduced line count do not prove a successful refactor.

## Deliver

Report decision, evidence, scope, mutation authority, before/after topology, trigger and resource ownership, exact changes, consumer migration, tests, host verification, rollback, delegated work, unresolved risks, and lifecycle handoff.

Do not claim a merge, split, extraction, or migration complete until the relevant behavior and consumers are verified.
