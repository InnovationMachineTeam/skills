# skill-refactor

`skill-refactor` assesses and safely changes the boundaries of existing skills: it keeps them separate, links them through composition, physically merges them, splits them, extracts references or subskills, and creates temporary compatibility facades.

## Decisions

- `KEEP_SEPARATE`
- `COMPOSE`
- `MERGE`
- `SPLIT`
- `EXTRACT_REFERENCE`
- `EXTRACT_SUBSKILL`
- `CREATE_FACADE`
- `PROMOTE_PUBLIC`
- `DEMOTE_PRIVATE`

By default, the skill performs a read-only assessment. Mutations require a precise plan, permission, validation, and rollback.

## Verification

```bash
python3 scripts/analyze_boundaries.py SKILL_DIR [SKILL_DIR ...] --output boundaries-before.json
python3 scripts/validate_refactor_plan.py refactor-plan.json
python3 scripts/compare_boundaries.py boundaries-before.json boundaries-after.json
python3 scripts/check_evals.py evals
```

Structural validity and a reduced file count do not prove correctness of routing, behavior, consumers, or host discovery.

Visibility migration accounts for the registry/map, owner-agent version, consumers, and host discovery. `private` means agent-scoped binding, not secrecy.

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Assesses and safely changes capability boundaries and visibility across existing SKILL.md-based agent skills by composing, merging, splitting, extracting references or subskills, promoting private skills to public, demoting unused public skills to agent-private, and creating compatibility facades.
- **Version:** `1.2.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `refactoring`, `topology`.

## When To Use

A user asks whether skills should be combined, divided, extracted, shared across agents, narrowed to one agent, or migrated while preserving triggers, authority, resources, tests, consumers, registry bindings, and rollback. Produce an evidence-backed boundary decision before mutation.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/skill-refactor Use $skill-refactor to reorganize my skills.
```

**Expected result:** route `clarify` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### explicit-no-target

- **Example request:** “Use $skill-refactor to reorganize my skills.”
- **Expected route:** `clarify`.

### assess-topology

- **Example request:** “Assess whether these two skills should stay separate, compose, or merge; make no changes.”
- **Expected route:** `boundary-assessment`.
- **Expected action:** `assess`.

### compose-independent

- **Example request:** “Keep both skills independently invocable but create a bounded workflow that coordinates them.”
- **Expected route:** `compose`.
- **Expected action:** `plan-refactor`.

### merge-overlap

- **Example request:** “These two skills have the same users, triggers, authority, and tests. Plan one canonical merged skill.”
- **Expected route:** `merge`.
- **Expected action:** `plan-refactor`.

### split-domains

- **Example request:** “Split this multi-domain skill into independently triggered skills and preserve the old entry point.”
- **Expected route:** `split-extract`.
- **Expected action:** `plan-refactor`.

### extract-reference

- **Example request:** “The workflow is cohesive but SKILL.md contains 700 lines of conditional schemas and examples. Extract references.”
- **Expected route:** `reference-extraction`.
- **Expected action:** `plan-refactor`.

### compatibility-facade

- **Example request:** “Create a temporary compatibility facade and consumer migration plan for the renamed skills.”
- **Expected route:** `facade-migration`.
- **Expected action:** `plan-refactor`.

### promote-private-public

- **Example request:** “A second independent agent now needs this private skill. Generalize and promote it to public with registry and consumer migration.”
- **Expected route:** `visibility-migration`.
- **Expected action:** `plan-refactor`.


## Expected Results

### no-target

For request “Combine my skills.”, the result must:

- asks for exact skill paths;
- asks for desired outcome;
- defaults to read-only assessment.

### permission-mismatch

For request “Merge a read-only research skill with a deployment skill that has production credentials.”, the result must:

- flags permission union;
- prefers separation or composition;
- requires explicit authority analysis.

### cohesive-large-skill

For request “Split this large skill whose sections share one trigger, state, and completion contract.”, the result must:

- considers EXTRACT_REFERENCE;
- tests independent triggers;
- preserves cohesive behavior.

### split-with-consumers

For request “Split the skill, delete the original immediately, and ignore existing consumers.”, the result must:

- inventories consumers;
- proposes facade or staged migration;
- preserves rollback.

### shared-resources

For request “Both new skills need the same changing policy reference and stateful script.”, the result must:

- assigns canonical ownership;
- defines access and state boundaries;
- avoids duplicated changing knowledge.

### dirty-worktree

For request “Apply an approved split in a repository with unrelated local edits.”, the result must:

- preserves unrelated edits;
- limits exact files;
- reports overlapping changes.

### merge-validation

For request “The merged folder validates structurally, but routing and consumer tests were not run.”, the result must:

- marks result incomplete or inconclusive;
- requires comparable behavior and consumer tests;
- retains rollback.

### facade-retirement

For request “The compatibility facade exists but actual host discovery is unknown.”, the result must:

- requires host verification;
- keeps retirement pending;
- routes lifecycle work to manager.


## Execution Flow

1. **Establish scope and authority.** Execute the corresponding contract step from `SKILL.md`.
2. **Keep role boundaries.** Execute the corresponding contract step from `SKILL.md`.
3. **Capture a structural baseline.** Execute the corresponding contract step from `SKILL.md`.
4. **Decide before changing.** Execute the corresponding contract step from `SKILL.md`.
5. **Select one primary route.** Execute the corresponding contract step from `SKILL.md`.
6. **Preview a refactor plan.** Execute the corresponding contract step from `SKILL.md`.
7. **Apply safely.** Execute the corresponding contract step from `SKILL.md`.
8. **Verify topology and behavior.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

Read-only comparison alone, independent evaluation, ordinary optimization, new unrelated skill creation, or installation; route those to skill-harvester, skill-evaluator, skill-optimizer, skill-architect, or skill-manager.

The following examples should route to another skill or should not trigger this skill:

- “Compare these two skills and list shared patterns, differences, and good decisions without changing topology.” → `skill-harvester`.
- “Reduce context cost in this healthy skill without changing its capability boundary.” → `skill-optimizer`.
- “Create a new skill for invoice reconciliation.” → `skill-architect`.
- “Install and activate this existing skill.” → `skill-manager`.
- “Refactor these two Python classes into one module.” → `do-not-trigger`.
- “Compare these skills, choose a topology, create any extracted bundles, migrate consumers, and roll out safely.” → `skill-builder`.

Critical anti-results:

- scans broad roots;
- merges by name;
- mutates files;
- inherits all permissions;
- concatenates instructions;
- calls merge safe;
- splits by headings alone;
- creates uninvocable fragments;
- duplicates shared knowledge;
- deletes the original immediately.

## Dependencies

No required companion skills are declared in the canonical dependency graph. Check the availability of host tools and resources referenced by `SKILL.md`.

## Package Resources

- [`SKILL.md`](DONOR.md) — executable contract, routing, and safety rules.
- [`agents/`](agents/) — UI metadata and host configuration.
- [`evals/`](evals/) — routing and behavior scenarios.
- [`prompts/`](prompts/) — routing and specialist prompts.
- [`references/`](references/) — reference guides, schemas, and contracts.
- [`scripts/`](scripts/) — deterministic checks and automation.

## Result Verification

- Compare routing against [`evals/routing.json`](evals/routing.json).
- Compare result properties against [`evals/behavior.json`](evals/behavior.json).
- For deterministic verification, use [`scripts/analyze_boundaries.py`](scripts/analyze_boundaries.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/check_evals.py`](scripts/check_evals.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/compare_boundaries.py`](scripts/compare_boundaries.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/validate_refactor_plan.py`](scripts/validate_refactor_plan.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
