# agent-os-architect

<!-- generated-skill-readme:start -->

## Skill Profile

- **Purpose:** Designs the minimum justified Agentic OS across experience, control, execution, knowledge, assurance and operations planes, including desired versus observed state, identities, schemas, policy points, protocols, SLOs, threat and failure models, deployment topology and staged evolution.
- **Version:** `1.0.3`.
- **Visibility:** public: canonical catalog skill; actual activation depends on the target host.
- **Catalog tags:** `agents`, `agent-os`, `architecture`.

## When To Use

A team runtime is no longer sufficient and a user needs a platform architecture, build/extend/buy comparison, bounded walking skeleton or Agentic OS ADR. Design only; do not bootstrap infrastructure, operate runs, change registries or policies, or issue release verdicts.

Before running, provide the concrete goal, source artifacts, allowed changes, constraints, and acceptance criteria. If essential information is missing, the expected first result is clarification or a safe plan, not an unverified mutation.

## Full Command Example

Illustrative full invocation; adapt the paths, constraints, and acceptance criteria to your task:

```text
/agent-os-architect Design a minimal Agentic OS for multiple durable release runs.
```

**Expected result:** route `design` is selected; the result lists the created or modified artifacts, the checks actually performed, the constraints, residual risks, and the next step. The presence of files alone is not considered proof of installation, activation, or publication.

## Usage Variants

### design

- **Example request:** “Design a minimal Agentic OS for multiple durable release runs.”
- **Expected route:** `design`.

### buy

- **Example request:** “Compare build, extend and buy for our agent control plane.”
- **Expected route:** `compare`.


## Expected Results

### reject-platform

For request “Create Agentic OS for one short task.”, the result must:

- returns simpler workflow unless platform evidence exists.

### threats

For request “Architect a multi-tenant runtime.”, the result must:

- defines six planes, trust zones, policy points, SLOs and recovery.


## Execution Flow

1. **Inventory and compare.** Execute the corresponding contract step from `SKILL.md`.
2. **Design the vertical slice.** Execute the corresponding contract step from `SKILL.md`.

## Boundaries And Unsuitable Requests

The following examples should route to another skill or should not trigger this skill:

- “Design two agents for one code review.” → `agent-team-architect`.

Critical anti-results:

- adds infrastructure by default;
- treats LLM output as enforcement.

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
- For deterministic verification, use [`scripts/validate_architecture.py`](scripts/validate_architecture.py) according to its `--help` output and the skill contract.
- For a release-bound change, also run repository validation, the full unit suite, and generated package verification.

## Completion Format

The final answer must list the selected route, actual inputs and assumptions, created or modified artifacts, checks performed, the expected scenario outcome, forbidden or skipped actions, residual risks, rollback status, and the exact next step. The presence of files alone does not prove installation, activation, publication, or production readiness.

<!-- generated-skill-readme:end -->
