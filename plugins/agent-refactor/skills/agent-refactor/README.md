# agent-refactor

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Assesses and safely changes the capability, ownership or topology boundaries of existing individual agents through merge, split, extraction, composition, promotion to a team, or public/private capability and documentation migration.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `refactoring`, `topology`.

## When To Use

An agent has mixed missions, duplicated roles, unsafe authority coupling, excessive context, changing consumers, or needs a versioned topology migration. Do not tune a healthy agent, repair a local defect, design a new agent from scratch, silently rewrite teams or Agentic OS, move folders without consumer migration, or activate the result.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-refactor This agent has unrelated analyst and deployer missions with different permissions; assess a split.
```

**Expected result:** route `split` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### split

- **Example request:** “This agent has unrelated analyst and deployer missions with different permissions; assess a split.”
- **Expected route:** `split`.

### merge

- **Example request:** “Compare these duplicate reviewer agents and plan a safe merge with consumer migration.”
- **Expected route:** `merge`.

### team

- **Example request:** “Assess migration of this registered overloaded single agent into a team, but do not design the team yet.”
- **Expected route:** `promote-to-team`.


## Expected Results

### folder-only

For request “Move the agent folder and call the split complete.”, the result must:

- requires consumer and registry migration;
- requires coexistence and rollback.

### private-promotion

For request “A second agent wants a private capability; add it to the allow-list.”, the result must:

- rejects multi-owner private access;
- assesses public promotion.

### docs-migration

For request “Split the architecture agent but leave ADR ownership and indexes unchanged.”, the result must:

- migrates document ownership and links;
- blocks incomplete split.


## Execution Flow

1. **Assess the boundary.** Execute the corresponding contract step from `SKILL.md`.
2. **Plan a recoverable migration.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “A new delivery problem may need multiple agents; assess and design the minimal team.” → `agent-team-architect`.
- “Reduce this healthy agent's latency without changing boundaries.” → `agent-optimizer`.
- “Fix one malformed tool response regression.” → `agent-doctor`.

Critical anti-results:

- treats folder move as complete;
- expands private allow-list;
- orphaned documents.

## Dependencies

- **Required: `agent-architect` >= `1.0.0`.** New individual-agent boundaries require a validated definition contract.
- **Required: `agent-evaluator` >= `1.0.0`.** Old/new topology and consumer migrations require independent evaluation.
- **Required: `agent-manager` >= `1.0.0`.** Lifecycle migration, rollout and retirement belong to the manager.
- **Recommended: `agent-team-architect` >= `1.1.0`.** Recommended after an existing-agent migration decision promotes the asset into a team.

A missing required dependency blocks only the route that depends on it. Recommended dependencies improve evidence quality but must not be imitated by the skill itself.

## Package Resources

- [`SKILL.md`](SKILL.md) — executable contract, routing, and safety rules.
- [`agents/`](agents/) — UI metadata and host configuration.
- [`evals/`](evals/) — routing and behavior scenarios.
- [`references/`](references/) — reference guides, schemas, and contracts.

## Result Verification

- Compare routing against [`evals/routing.json`](evals/routing.json).
- Compare result properties against [`evals/behavior.json`](evals/behavior.json).
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
