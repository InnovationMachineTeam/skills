# Evals and Regressions Diagnostic Prompt

Apply after [base.md](base.md).

Verify the failing case, baseline, fixtures, model, tools, settings, judge, rubric, and environment. Check stale expectations, exact-string overfitting, answer leakage, missing negatives, biased judges, nondeterminism, and incomparable before/after runs.

Determine whether the skill regressed or the evaluation is defective. Do not modify the rubric merely to make the candidate pass.

Repair the confirmed fixture, assertion, rubric, or skill path separately. Add a regression for the original failure and keep a held-out case. Rerun comparable evaluation before assigning recovery.

