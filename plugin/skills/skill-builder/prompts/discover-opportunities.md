# Scenario: discover-opportunities

Use when the user wants ideas, prioritization, or a build/no-build decision rather than immediate creation.

1. Invoke `skill-scout` on the explicitly authorized session, corpus, history, repository, or portfolio.
2. Require existing-coverage analysis before `CREATE_NEW`.
3. Preserve `RESEARCH`, `USE_AUTOMATION`, `KEEP_AD_HOC`, and reuse decisions; do not bias toward skill creation.
4. Rank by evidence, leverage, stable triggers, evalability, context cost, maintenance, risk, and coverage.
5. Return the opportunity manifest and proposed downstream scenario for each accepted candidate.

Do not automatically continue into research or creation. Continue only when the user requested end-to-end execution or approves a proposed candidate.
