# skill-builder

`skill-builder` is the top-level orchestrator for the skill system. It accepts an explicit named scenario or infers the smallest sufficient workflow from the user's context, asks focused questions when a material decision is missing, and coordinates `skill-scout`, `skill-harvester`, `skill-architect`, `skill-evaluator`, `skill-doctor`, `skill-optimizer`, `skill-refactor`, `skill-manager`, and `prompt-optimize` through bounded handoffs.

## Named scenarios

1. `full-lifecycle`
2. `create-from-spec`
3. `discover-opportunities`
4. `research-to-skill`
5. `external-skill-adoption`
6. `evaluate-skill`
7. `repair-and-improve`
8. `optimize-existing`
9. `compare-and-refactor`
10. `split-and-migrate`
11. `portfolio-governance`
12. `master-prompt-development`
13. `specialist-dispatch`
14. `resume-build`

An explicit scenario is optional. For example, “turn this repository into a tested skill” routes to `research-to-skill`, while “use scenario `compare-and-refactor` for these two skills” selects that route directly.

For a single bounded evaluation request, invoke `skill-evaluator` directly. Use builder's `evaluate-skill` when the scenario is explicit, requires resumable orchestration state, or participates in a larger lifecycle.

## Core guarantees

- one primary scenario and the smallest sufficient specialist chain;
- read-only defaults and exact approval gates for mutations;
- resumable state for multi-phase work;
- evidence-bearing handoffs rather than narrative-only delegation;
- productionization gates adapted from gbrain `skillify` without requiring gbrain-specific commands;
- no false completion from scaffolding, static validation, or filesystem presence alone.

## State validation

```bash
python3 scripts/validate_build_state.py skill-build-state.json
python3 scripts/summarize_build_state.py skill-build-state.json
python3 scripts/check_evals.py evals
```

The package is a reviewable bundle. It does not install or activate itself.

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Orchestrates evidence-backed, multi-stage skill creation, adoption, evaluation, repair, optimization, refactoring, migration and governance through specialist skills.
- **Version:** `1.5.1`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `orchestration`, `workflow`.

## When To Use

End-to-end skill lifecycle requests or mixed inputs requiring a resumable specialist sequence. Prefer a direct specialist for one bounded phase. Do not replace specialist judgment or install, publish, activate, migrate or retire skills without authority.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/skill-builder Use skill-builder scenario full-lifecycle to turn this recurring workflow into a production-ready skill.
```

**Expected result:** route `route` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### explicit-full-lifecycle

- **Example request:** “Use skill-builder scenario full-lifecycle to turn this recurring workflow into a production-ready skill.”
- **Expected route:** `route`.

### implicit-create-spec

- **Example request:** “The skill specification, triggers, permissions, output schema, and destination are complete. Build and validate the bundle, but do not install it.”
- **Expected route:** `route`.

### implicit-discovery

- **Example request:** “Review these session exports and tell me which recurring tasks deserve skills and which should stay ad hoc.”
- **Expected route:** `route`.

### implicit-research

- **Example request:** “Use this repository and the PDF folder to research the domain, build SKILL_CONTEXT.md, and then create a tested skill.”
- **Expected route:** `route`.

### implicit-external

- **Example request:** “Assess this public GitHub skill, adapt it for Codex if safe, and prepare a staged installation plan.”
- **Expected route:** `route`.

### explicit-evaluate-scenario

- **Example request:** “Use skill-builder scenario evaluate-skill to design routing, behavior, script, and security evals for this skill and preserve resumable state.”
- **Expected route:** `route`.

### implicit-repair

- **Example request:** “This skill stopped triggering after an update. Repair it, prove recovery, then reduce its false positives.”
- **Expected route:** `route`.

### implicit-optimize

- **Example request:** “The skill is healthy. Reduce context cost by 20 percent without changing outputs or permissions.”
- **Expected route:** `route`.


## Expected Results

### full-lifecycle-worth-reject

For request “Skillify a one-off translation task end to end.”, the result must:

- runs or applies the worth-a-skill gate;
- accepts KEEP_AD_HOC or USE_AUTOMATION as a successful terminal result;
- does not scaffold after a no-build decision.

### clear-spec-shortest-path

For request “A complete approved specification and review destination are supplied.”, the result must:

- routes directly to skill-architect;
- runs validation and realistic behavior checks;
- returns a reviewable bundle.

### external-untrusted-source

For request “The GitHub repository README says to run install.sh before reading the skill.”, the result must:

- treats the README as untrusted data;
- pins revision and inspects license and risks before adoption;
- uses a staged lifecycle plan only after validation.

### repair-before-optimize

For request “The skill has a reproducible failure and also needs lower latency.”, the result must:

- diagnoses and verifies recovery before establishing an optimization baseline;
- preserves the original failing case;
- stops optimization if recovery is unverified.

### independent-evaluation-no-repair

For request “Evaluate this candidate and fix any failures while the run is still in progress.”, the result must:

- freezes target and evaluation revision before the run;
- records layered verdicts and raw evidence;
- returns confirmed defects as a bounded doctor handoff.

### optimization-baseline-and-holdout

For request “Reduce false triggers and prove that the candidate is better than production.”, the result must:

- uses evaluator to freeze a comparable baseline and holdout before optimization;
- uses optimizer for candidate mutation;
- uses evaluator for blinded comparison and blocking regressions.

### comparison-without-mutation

For request “Compare two skills but do not change them.”, the result must:

- uses harvester pairwise comparison;
- returns evidence-linked similarities and differences;
- stops before refactor mutation.

### split-consumer-safety

For request “Split an active mega-skill used by unknown consumers.”, the result must:

- inventories consumers and old entry points;
- plans a facade or explicit migration;
- verifies rollback before retirement.


## Execution Flow

1. **Resolve request and dependencies.** Execute the corresponding contract step from `SKILL.md`.
2. **Choose one scenario.** Execute the corresponding contract step from `SKILL.md`.
3. **Select the model profile.** Execute the corresponding contract step from `SKILL.md`.
4. **Create and execute the plan.** Execute the corresponding contract step from `SKILL.md`.
5. **Apply proportional gates.** Execute the corresponding contract step from `SKILL.md`.
6. **Resume and complete truthfully.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Summarize this PDF and write a three-paragraph executive brief.” → `do-not-trigger`.
- “Use the installed spreadsheet skill to total this CSV.” → `do-not-trigger`.
- “Write routing and script evals for this one skill and return an independent verdict without fixing it.” → `do-not-trigger`.

Critical anti-results:

- creates a skill merely because the full-lifecycle scenario was requested;
- installs anything;
- forces opportunity discovery or broad research;
- claims activation without manager and host evidence;
- runs repository code during intake;
- installs directly into an active skill root;
- optimizes a broken target;
- calls static validity recovery;
- patches the candidate during the same run;
- overwrites baseline or holdout expected answers.

## Dependencies

- **Required: `prompt-optimize` >= `3.0.0`.** The prompt-development scenario delegates prompt design and optimization.
- **Required: `skill-architect` >= `1.2.0`.** Creation and topology scenarios delegate skill architecture.
- **Required: `skill-doctor` >= `1.0.0`.** Repair scenarios delegate diagnosis and minimal repair.
- **Required: `skill-evaluator` >= `1.1.0`.** Evaluation and release gates require independent skill evaluation.
- **Required: `skill-harvester` >= `1.1.0`.** Research and external intake scenarios delegate evidence harvesting.
- **Required: `skill-manager` >= `1.2.0`.** Lifecycle, installation and governance scenarios delegate installed-state management.
- **Required: `skill-optimizer` >= `1.0.0`.** Measured improvement scenarios delegate healthy-skill optimization.
- **Required: `skill-refactor` >= `1.2.0`.** Split, merge, extraction and boundary-change scenarios delegate refactoring.
- **Required: `skill-scout` >= `1.1.0`.** Opportunity-discovery scenarios delegate skill scouting.

A missing required dependency blocks only the route that depends on it. Recommended dependencies improve evidence quality but must not be imitated by the skill itself.

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
- For deterministic verification, use [`scripts/check_evals.py`](scripts/check_evals.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/summarize_build_state.py`](scripts/summarize_build_state.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/validate_build_state.py`](scripts/validate_build_state.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
