# agent-skill-mapper

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Maps governed public and owner-private skills or commands to existing agents using mission fit, permissions, trust, context cost, evidence and capability budgets.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `skills`, `mapping`.

## When To Use

Auditing agent capabilities, reconciling agent definitions with registries or skills-lock files, recommending versioned bindings, detecting gaps or excessive tool access, or preparing a controlled mapping update. Read only by default. Do not create agents or skills, promote private capabilities, silently edit agent definitions, or operate the team; route missing capability creation to the relevant architect and team design changes to agent-team-architect.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-skill-mapper Inventory all skills available to these registered agents.
```

**Expected result:** route `inventory` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### inventory

- **Example request:** “Inventory all skills available to these registered agents.”
- **Expected route:** `inventory`.

### recommend

- **Example request:** “Which versioned skills should each agent receive?”
- **Expected route:** `recommend`.

### audit

- **Example request:** “Audit the current agent-to-skill map for excess permissions.”
- **Expected route:** `audit`.

### apply

- **Example request:** “Apply this approved mapping transaction and bump agent versions.”
- **Expected route:** `apply`.

### promote

- **Example request:** “Can this private agent skill be promoted for team use?”
- **Expected route:** `private-promotion`.


## Expected Results

### private-boundary

For request “Map agent-a's private command to agent-b.”, the result must:

- rejects cross-owner mapping;
- offers explicit promotion workflow.

### read-only

For request “Recommend capabilities for the team.”, the result must:

- does not mutate files;
- uses exact versions and evidence;
- enforces capability budgets.

### authorized-apply

For request “Apply approved map revision 7.”, the result must:

- checks expected revisions;
- bumps changed agent versions;
- supports rollback.


## Execution Flow

1. **Establish inventory and authority.** Execute the corresponding contract step from `SKILL.md`.
2. **Score candidates through hard gates.** Execute the corresponding contract step from `SKILL.md`.
3. **Decide and explain.** Execute the corresponding contract step from `SKILL.md`.
4. **Apply only an authorized transaction.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Create a new PDF extraction skill.” → `skill-architect`.
- “Design the roles for a research agent team.” → `agent-team-architect`.

Critical anti-results:

- silently copies private content;
- activates mappings;
- overwrites concurrent changes.

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
- For deterministic verification, use [`scripts/validate_mapping.py`](scripts/validate_mapping.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
