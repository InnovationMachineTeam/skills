# agent-team-builder

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Materializes an approved, versioned agent-team specification into a staged `.agents` structure, canonical definitions, owner-private skills or commands, public capability candidates, host adapters, registry/map transactions and verification evidence.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `build`, `teams`.

## When To Use

A reviewed team design is ready to build, rebuild, migrate or dry-run. Requires an exact approved spec, destination and write authority. Do not redesign roles, substitute models or permissions, activate agents, create worktrees, publish private assets, or operate the team; route design changes to agent-team-architect and lifecycle execution to agent-team-manager.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-team-builder Check whether this approved team spec is buildable.
```

**Expected result:** route `preflight` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### preflight

- **Example request:** “Check whether this approved team spec is buildable.”
- **Expected route:** `preflight`.

### dry-run

- **Example request:** “Show the exact files this team build would write.”
- **Expected route:** `dry-run`.

### build

- **Example request:** “Stage approved agent-team spec 2.1.0.”
- **Expected route:** `build`.

### rebuild

- **Example request:** “Rebuild generated adapters from the approved canonical spec.”
- **Expected route:** `rebuild`.

### migrate

- **Example request:** “Migrate this approved team scaffold to the canonical .agents layout.”
- **Expected route:** `migrate`.


## Expected Results

### unapproved

For request “Build this draft team spec now.”, the result must:

- blocks without approved spec;
- requests exact version and hash.

### private

For request “Include an agent-private skill in the team build.”, the result must:

- keeps the skill under its owner;
- excludes it from marketplace packaging.

### staged

For request “Build the approved team.”, the result must:

- uses an exact manifest;
- stages before promotion;
- leaves activation false;
- supports rollback.


## Execution Flow

1. **Gate the build.** Execute the corresponding contract step from `SKILL.md`.
2. **Plan the exact write-set.** Execute the corresponding contract step from `SKILL.md`.
3. **Materialize into staging.** Execute the corresponding contract step from `SKILL.md`.
4. **Verify and promote atomically.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Decide which roles this problem needs.” → `agent-team-architect`.
- “Run this agent team on issue 42.” → `agent-team-manager`.

Critical anti-results:

- writes scaffold;
- adds multiple consumers;
- silently changes roles or models.

## Dependencies

No required companion skills are declared in the canonical dependency graph. Check the availability of host tools and resources referenced by `SKILL.md`.

## Package Resources

- [`SKILL.md`](SKILL.md) — executable contract, routing, and safety rules.
- [`agents/`](agents/) — UI metadata and host configuration.
- [`evals/`](evals/) — routing and behavior scenarios.
- [`references/`](references/) — reference guides, schemas, and contracts.
- [`scripts/`](scripts/) — deterministic checks and automation.

## Result Verification

- Compare routing against [`evals/routing.json`](evals/routing.json).
- Compare result properties against [`evals/behavior.json`](evals/behavior.json).
- For deterministic verification, use [`scripts/check_evals.py`](scripts/check_evals.py) according to its `--help` output and the skill contract.
- For deterministic verification, use [`scripts/validate_build_manifest.py`](scripts/validate_build_manifest.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
