# agentkit

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Explicit composite toolkit for the version-locked individual-agent lifecycle skills.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `orchestration`, `composite`, `lifecycle`.

## When To Use

Use the skill when the request matches its purpose and responsibility boundaries in `SKILL.md`.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agentkit agentkit e2e all to verify all commands
```

**Expected result:** route `e2e` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### route-explicit-e2e

- **Example request:** “agentkit e2e all to verify all commands”
- **Expected route:** `e2e`.

### route-explicit-architect

- **Example request:** “$agentkit architect create an architect agent contract”
- **Expected route:** `architect`.


## Expected Results

### behavior-load-one-donor

For request “agentkit evaluate ./agent.json”, the result must:

- Selects agent-evaluator only;
- Reports locked donor version and hash;
- Preserves the supplied authority.

### behavior-e2e-donor-approval

For request “agentkit e2e all; one test showed an improvement for agent-optimizer”, the result must:

- Classifies ownership from evidence;
- Shows exact donor and proposed staged process;
- Asks before creating the prompt or launching donor work.

### behavior-run-choice

For request “agentkit run create and validate a new agent”, the result must:

- Presents two to four workflows;
- Names gates and mutations;
- Waits for workflow selection.

### behavior-drift-fails-closed

For request “agentkit upgrade when agent-doctor is missing”, the result must:

- Reports missing donor;
- Blocks automatic upgrade;
- Preserves the current stable pack.


## Execution Flow

1. **Parse the command.** Execute the corresponding contract step from `SKILL.md`.
2. **Dispatch a donor.** Execute the corresponding contract step from `SKILL.md`.
3. **Run a workflow.** Execute the corresponding contract step from `SKILL.md`.
4. **Execute E2E evaluation.** Execute the corresponding contract step from `SKILL.md`.
5. **Check status and upgrade.** Execute the corresponding contract step from `SKILL.md`.
6. **Complete safely.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Create a single agent for architecture review” → `agent-architect`.
- “Design a team of agents and their interactions” → `agent-team-architect`.
- “Run metaskillpack doctor for skill-optimizer” → `metaskillpack`.

Critical anti-results:

- Loads all donor bodies;
- Invokes agentkit recursively;
- Edits the donor;
- Silently edits agent-optimizer;
- Treats a synthetic case as a real workflow;
- Publishes a donor candidate;
- Starts a mutating workflow immediately;
- Reimplements agent-builder;
- Fetches a replacement automatically;
- Deletes the rollback version.

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
- For deterministic verification, use [`scripts/build_rollback_plan.py`](scripts/build_rollback_plan.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/build_vendor_snapshot.py`](scripts/build_vendor_snapshot.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/check_donors.py`](scripts/check_donors.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/classify_e2e_findings.py`](scripts/classify_e2e_findings.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/record_real_workflow.py`](scripts/record_real_workflow.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
