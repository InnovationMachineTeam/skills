# metaskillpack

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Provides a self-contained, explicitly invoked toolkit for creating, discovering, researching, optimizing, diagnosing, governing, harvesting, refactoring, evaluating, packaging, and orchestrating agent skills through isolated snapshots of the InnovationMachine metaskills.
- **Version:** `1.5.2`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `orchestration`, `composite`, `metaskills`.

## When To Use

Use the skill when the request matches its purpose and responsibility boundaries in `SKILL.md`.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/metaskillpack create invoice-reviewer from this approved specification
```

**Expected result:** route `the skill's primary route` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### create

- **Example request:** “create invoice-reviewer from this approved specification”
- **Expected route:** `the skill's primary route`.

### scout

- **Example request:** “scout these session exports”
- **Expected route:** `the skill's primary route`.

### research-context-build

- **Example request:** “research invoice-reviewer use docs/ and the repository”
- **Expected route:** `the skill's primary route`.

### optimize

- **Example request:** “optimize invoice-reviewer reduce false triggers”
- **Expected route:** `the skill's primary route`.

### doctor

- **Example request:** “doctor invoice-reviewer script fails on empty CSV”
- **Expected route:** `the skill's primary route`.

### manage

- **Example request:** “manage invoice-reviewer preview an upgrade”
- **Expected route:** `the skill's primary route`.

### harvest

- **Example request:** “harvest https://github.com/example/public-repo extract patterns read-only”
- **Expected route:** `the skill's primary route`.

### refactor

- **Example request:** “refactor skills/a split into two coherent skills”
- **Expected route:** `the skill's primary route`.


## Expected Results

### explicit-only-collision

For request “Optimize this healthy skill, but metaskillpack was not named.”, the result must:

- does not implicitly claim the request;
- leaves routing to the individual skill-optimizer.

### progressive-mode-loading

For request “$metaskillpack doctor broken-skill”, the result must:

- loads donors.json and only vendor/skill-doctor/DONOR.md initially;
- reports donor version and selected mode.

### research-compatibility-route

For request “$metaskillpack research invoice-reviewer from docs and repository”, the result must:

- uses skill-harvester context-build;
- does not require a nonexistent skill-context donor.

### run-workflow-gate

For request “$metaskillpack run productionize this recurring task”, the result must:

- proposes two to four workflows with one recommendation;
- waits for selection before skill-builder execution.

### upgrade-current-noop

For request “$metaskillpack upgrade when all donor versions and digests match”, the result must:

- reports an evidence-backed current status;
- writes no files.

### upgrade-same-version-drift

For request “A donor script changed but metadata.version did not.”, the result must:

- detects tree digest drift;
- marks the donor changed and flags missing version discipline.

### upgrade-missing-donor

For request “skill-evaluator cannot be found in any supplied donor root.”, the result must:

- stops before the upgrade master prompt;
- lists searched roots and asks for restoration, installation, or an explicit architecture change.

### upgrade-readonly-donors

For request “Rebuild from newer source donors.”, the result must:

- copies donor inputs into a fresh candidate;
- validates before an authorized promotion.


## Execution Flow

1. **Parse the invocation.** Execute the corresponding contract step from `SKILL.md`.
2. **Select a mode.** Execute the corresponding contract step from `SKILL.md`.
3. **Dispatch one snapshot.** Execute the corresponding contract step from `SKILL.md`.
4. **Handle native control modes.** Execute the corresponding contract step from `SKILL.md`.
5. **Treat run as an advisory gate.** Execute the corresponding contract step from `SKILL.md`.
6. **Preserve boundaries.** Execute the corresponding contract step from `SKILL.md`.
7. **Verify the pack.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The skill must not expand the authority it received, hide skipped checks, perform irreversible or external actions without explicit permission, or claim host state solely from the presence of files.

Critical anti-results:

- loads the full pack;
- claims that keyword optimize is sufficient activation;
- preloads every donor;
- uses skill-optimizer before a verified recovery;
- fabricates skill-context;
- installs an external namesake;
- starts the recommended flow immediately;
- asks the user to name internal specialists;
- rebuilds identical snapshots;
- bumps the pack version.

## Dependencies

No required companion skills are declared in the canonical dependency graph. Check the availability of host tools and resources referenced by `SKILL.md`.

## Package Resources

- [`SKILL.md`](SKILL.md) — executable contract, routing, and safety rules.
- [`agents/`](agents/) — UI metadata and host configuration.
- [`evals/`](evals/) — routing and behavior scenarios.
- [`prompts/`](prompts/) — routing and specialist prompts.
- [`references/`](references/) — reference guides, schemas, and contracts.
- [`scripts/`](scripts/) — deterministic checks and automation.
- [`vendor/`](vendor/) — pinned snapshot of dependent components.

## Result Verification

- Compare routing against [`evals/routing.json`](evals/routing.json).
- Compare result properties against [`evals/behavior.json`](evals/behavior.json).
- For deterministic verification, use [`scripts/build_snapshot.py`](scripts/build_snapshot.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/check_donors.py`](scripts/check_donors.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/check_evals.py`](scripts/check_evals.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/donor_utils.py`](scripts/donor_utils.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/route_command.py`](scripts/route_command.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
