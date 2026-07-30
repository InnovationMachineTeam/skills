# Descriptions, discovery, and routing

Practice-ID: BP-ROUTE-001
Scope: mixed
Status: current
Sources: SRC-AS-003, SRC-AS-006, SRC-ANT-002, SRC-OAI-001, SRC-OAI-004, SRC-EX-002
Last-rebuilt: 2026-07-30

## Description contract

Treat `description` as the primary routing interface because the body is not loaded during initial selection. Front-load the differentiating use case, output, domain terms, and important input formats. State realistic usage conditions and neighboring boundaries without narrating the internal workflow.

OpenAI catalogs may shorten descriptions or omit skills when the initial metadata budget is crowded. Therefore the first clause must remain useful after truncation, and catalog-level recall must be measured as the portfolio grows. This is an OpenAI host behavior, not a portable syntax rule.

## Routing dataset

Cover:

- direct explicit requests;
- indirect outcome-oriented requests;
- incomplete but relevant requests requiring clarification;
- hard negative near-misses;
- ambiguous collisions with neighboring skills;
- formal, conversational, typo, and abbreviated language.

Use a small 3–5-case set as an early approval smoke test and a larger repeated dataset for production routing. Split train, validation, and untouched holdout. Do not edit against holdout failures.

## Metrics and change control

Measure precision, recall, false positives, false negatives, stochastic trigger rate, ambiguity, neighboring-skill collisions, and catalog recall. Change one routing hypothesis at a time, preserve raw runs and environment, and optimize routing separately from behavioral instructions.

Disable implicit activation or require explicit invocation when the skill is dangerous, costly, intentionally manual, or too ambiguous for reliable automatic selection.
