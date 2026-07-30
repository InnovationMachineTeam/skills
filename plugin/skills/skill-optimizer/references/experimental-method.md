# Experimental Optimization Method

## Contents

- Baseline
- Hypothesis
- Controlled comparison
- Acceptance
- Change record

## Baseline

Record the exact skill revision, host, model, tool versions, fixtures, settings, permissions, and test commands. Capture raw outputs and side effects. Use several representative runs when behavior is nondeterministic.

Do not treat a structural score as an end-to-end baseline. Measure the user-visible outcome and the failure that motivated optimization.

## Hypothesis

Use this form:

```text
Observed failure:
Root-cause hypothesis:
Minimal change:
Primary metric:
Guardrail metrics:
Disconfirming evidence:
Acceptance threshold:
```

Prefer hypotheses that can be rejected. "Make the skill better" is not testable.

## Controlled comparison

- Keep model, tools, fixtures, host, and sampling settings constant.
- Change one behavioral hypothesis at a time.
- Run the same cases before and after.
- Include held-out and adversarial cases, not only examples used to author the change.
- Inspect outputs, artifacts, traces, and errors rather than aggregate scores alone.
- Repeat noisy cases and report variance.

## Acceptance

Accept only if the primary metric crosses its threshold and guardrails remain within bounds. Reject changes that improve averages while introducing a blocking safety or authority failure.

Do not accept a candidate when only structural proxies were remeasured. If the post-change primary behavioral metric is absent or incomparable, the result is inconclusive regardless of how plausible the patch appears.

When results are statistically or operationally inconclusive, label them inconclusive. Prefer the simpler last-known-good variant when behavior is equivalent.

## Change record

Report:

- baseline identifier or hash;
- hypothesis and patch scope;
- cases and metrics;
- before/after results;
- new failures and removed failures;
- accepted, rejected, or inconclusive decision;
- remaining uncertainty.
