# role-skill-architect

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Turns one approved role-agent capability into a researched, bounded, host-native skill package with triggers, method, knowledge provenance, contracts, examples, tests, evals, security, maintenance, and a justified implementation proposal.
- **Version:** `1.0.3`.
- **Visibility:** package-private: invoked only by its parent `agent-master` and not published separately.

## When To Use

Use the skill when the request matches its purpose and responsibility boundaries in `SKILL.md`.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

This package-private skill is not invoked directly. The illustrative request is passed through its parent `/agent-master`:

```text
/agent-master Agent-master dispatches one approved evidence-triangulation capability from a designed reviewer role.
```

**Expected result:** route `role-skill-architect` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.
Direct `/role-skill-architect` is not a supported public command; parent `agent-master` must pass a bounded dispatch contract and verify the result.

## Usage Variants

### approved-capability

- **Example request:** “Agent-master dispatches one approved evidence-triangulation capability from a designed reviewer role.”
- **Expected route:** `role-skill-architect`.


## Expected Results

### classification-gate

For request “The proposal is only a stable one-line prohibition for one agent.”, the result must:

- rejects a full skill;
- recommends an inline rule or private command;
- explains maintenance tradeoff.

### research-provenance

For request “Build a role skill that depends on current professional standards.”, the result must:

- researches authoritative current sources;
- records provenance and limitations;
- preserves conflicts.

### repo-native-package

For request “Create the skill in this repository from the supplied complete capability contract.”, the result must:

- uses repository-native SKILL.md structure;
- adds only necessary resources;
- creates routing and behavior evals.


## Execution Flow

1. **Verify and classify the proposal.** Execute the corresponding contract step from `SKILL.md`.
2. **Research the method.** Execute the corresponding contract step from `SKILL.md`.
3. **Build the host-native package.** Execute the corresponding contract step from `SKILL.md`.
4. **Evaluate and hand off.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Create the entire specialist reviewer agent first.” → `role-agent-architect`.
- “Implement the already approved deterministic schema validator proposed by this skill.” → `skill-implementation-engineer`.

Critical anti-results:

- scaffolds a large package;
- treats an exemplar repository as a standard;
- forces skill.yaml;
- adds empty directories;
- claims installation.

## Dependencies

There are no external catalog dependencies. Parent `agent-master` passes only a bounded dispatch envelope to this private skill and verifies its result.

## Package Resources

- [`SKILL.md`](SKILL.md) — executable contract, routing, and safety rules.
- [`evals/`](evals/) — routing and behavior scenarios.
- [`references/`](references/) — reference guides, schemas, and contracts.

## Result Verification

- Compare routing against [`evals/routing.json`](evals/routing.json).
- Compare result properties against [`evals/behavior.json`](evals/behavior.json).
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
