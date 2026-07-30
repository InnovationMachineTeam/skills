# Evaluation and Regression Optimization Prompt

Apply after [base.md](base.md). Improve the evidence system used to judge the skill.

## Diagnose

- Map each requirement and known failure to a case and observable property.
- Find missing negatives, ambiguous cases, adversarial inputs, failure paths, host variants, and last-known-good baselines.
- Check for answer leakage, judge bias, exact-string overfitting, and incomparable environments.

## Optimize

- Use deterministic assertions for objective invariants and calibrated rubrics for semantic quality.
- Add direct, paraphrased, neighboring, collision, failure, security, and regression cases.
- Blind independent evaluators to intended fixes.
- Record model, tools, fixtures, settings, repetitions, and variance.

## Guardrails

Do not change the rubric solely to make a candidate pass. Do not optimize only on visible cases. Keep held-out cases and report evaluator disagreement and untested surfaces.

