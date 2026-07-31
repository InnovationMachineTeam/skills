# Agentkit E2E contract

## Outcome

Create reproducible tests, execute selected agentkit commands through the same
router used by users, preserve outputs and findings, and produce bounded
improvement recommendations without silently modifying donors.

## Run directory

Use an explicit new directory such as `work/agentkit-e2e/<run-id>/`. The
scaffolder creates:

- `evaluation-plan.json` — frozen scope, authority and blocking gates;
- `cases.json` — public regression cases with expected and forbidden properties;
- `run-state.json` — per-case status and output locators;
- `findings.json` — observed defects and improvement opportunities;
- `classification.json` — ownership and next-action decisions.

Raw command outputs live below `raw/`. Do not put protected holdout answers in
the candidate bundle or generated public cases.

## Execution loop

1. Run donor status and abort on lock drift.
2. Scaffold the requested scope before executing a candidate result.
3. Freeze cases and acceptance criteria.
4. Execute each case in a clean task context through `agentkit <command>`.
5. Record the donor selected, version, output, side effects and verdict.
6. Validate false completion, command coverage and artifact paths.
7. Classify findings by `agentkit`, exact donor, `environment`, or `test`.
8. Produce recommendations; do not repair during the evaluation run.

For a real workflow observation, the frozen suite may select one of the named
workflow profiles from `scripts/scaffold_e2e_run.py`. Preserve semantic command
outputs and artifact hashes, then finalize once with
`scripts/record_real_workflow.py`. The finalizer rejects synthetic router
outputs, donor drift, incomplete evidence, changed authority and donor writes.

## Donor-improvement gate

For a donor-owned finding, show:

- exact donor identity, version and hash;
- failing cases and evidence;
- defect versus healthy improvement classification;
- proposed behavior change and preserved invariants;
- staged output destination, validation and rollback;
- the process to launch.

Ask for explicit approval covering prompt creation and the staged donor process.
If approval is declined or absent, record `deferred` and finish without writing
the prompt. If approved, create the prompt from `prompts/improve-donor.md`, run
prompt lint/evals, then dispatch the appropriate `skill-builder` scenario. A
separate lifecycle decision is required to replace or publish the donor.

## Verdicts

Use `PASS`, `FAIL`, `INCONCLUSIVE`, `BLOCKED`, and `NOT_EVALUATED`. One blocking
authority, routing, false-completion or donor-integrity failure blocks the E2E
run. Synthetic E2E cases do not count as real workflow observations in the
maturity ledger.
