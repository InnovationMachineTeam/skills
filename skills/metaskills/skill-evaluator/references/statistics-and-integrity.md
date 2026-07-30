# Statistics and evaluation integrity

## Comparable runs

Hold target-independent variables stable: cases, split, model, host, tools, runtime, grader, temperature or equivalent controls, repetitions, time window, and budget. If they differ materially, classify the comparison as adjusted or incomparable.

## Sampling and repetition

Use one run for deterministic behavior only after determinism is demonstrated. Repeat stochastic cases enough to support the decision risk; record all trials and failures. Prefer confidence intervals or raw numerator/denominator counts to unexplained point estimates. Do not claim significance or confidence when assumptions and sample size do not support it.

## Splits and leakage

- train/iteration: visible during development;
- validation: used for bounded selection decisions;
- holdout: untouched until the frozen candidate and acceptance gates are ready.

Answer-bearing cases committed inside a distributed skill package are public regression cases, not a protected holdout. Keep release holdout externally access-controlled, record its exposure policy, and never label visible expected answers as hidden evidence.

Prevent duplicate lineage across splits. Do not paste expected answers, suspected bugs, ideal routes, or previous scores into independent forward tests. Rotate or retire holdout after exposure and record the event.

## Baselines

Choose the baseline that answers the claim: no skill for incremental value, previous release for regression, control prompt for architecture value, neighboring skill for routing collision, or production trace for external validity. A candidate without a comparable baseline may still receive an absolute verdict, but not an improvement claim.

## Pareto decisions

Track quality, routing, safety, tokens, latency, tool calls, retries, cost, and complexity separately. Define blocking regressions. Do not compress the decision into one weighted score unless weights, normalization, and non-compensable failures are explicit.
