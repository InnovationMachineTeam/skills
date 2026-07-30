# Routing and trigger evaluation

## Case families

- explicit skill invocation;
- direct capability request;
- indirect outcome request;
- incomplete relevant request needing clarification;
- paraphrase, conversational wording, typo, abbreviation, and language variant;
- hard negative near-miss;
- ambiguous collision with a neighboring or built-in skill;
- common multi-skill composition;
- catalog truncation, omission, precedence, or alias behavior.

## Dataset contract

Every case has a stable ID, input, expected trigger, expected route/specialist where relevant, catalog composition, host, tags, split, and rationale. Keep examples realistic; synthetic templates should not dominate held-out evidence. Track copied lineage so repeated wording is not mistaken for independent coverage.

## Metrics

From expected versus observed trigger decisions compute true/false positives and negatives, precision, recall, specificity, accuracy, F1, and false-positive/negative rates when denominators exist. For repeated stochastic routing, preserve each trial and report trigger probability or an interval rather than only majority vote.

Measure catalog recall and collision rate separately from isolated-skill routing. Optimize one routing hypothesis at a time and rerun neighboring and catalog-level regressions.

## Trigger authoring boundary

The evaluator may write trigger fixtures, non-trigger fixtures, expected-route assertions, and proposed metadata alternatives. It does not silently apply a description change. Route a healthy tuning proposal to `skill-optimizer` and a capability/architecture change to `skill-architect`.
