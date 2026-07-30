# Context and Resource Architecture Optimization Prompt

Apply after [base.md](base.md). Reduce irrelevant context and improve discoverability without losing required knowledge.

## Diagnose

- Measure actual `SKILL.md` size and conditionally loaded resources.
- Find duplication, deeply nested references, stale scaffolding, frozen dynamic facts, and resources with no route.
- Distinguish bundle size from context loaded per task.

## Optimize

- Keep discovery in frontmatter and core procedure in `SKILL.md`.
- Move conditional detail to one-level references.
- Move deterministic repetition to tested scripts and output ingredients to assets.
- Put trigger and behavioral cases in `evals/` and reusable routed prompts in `prompts/`.
- Add contents and search guidance to large references.

## Guardrails

Prove removed content is redundant or intentionally deprecated. Verify every moved link and path. Do not save tokens by deleting safety, recovery, verification, or necessary domain constraints.

