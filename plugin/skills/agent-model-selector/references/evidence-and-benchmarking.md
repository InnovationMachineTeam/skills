# Evidence and benchmarking

## Evidence order

1. Current official provider/host documentation and model cards.
2. Reproducible task outcome from the target host and pinned model.
3. Calibrated human or independent model rubric.
4. Transparent estimate or expert judgment with uncertainty.

Do not replace a stronger available layer with a weaker claim. Record source
scope: API availability does not prove availability in every IDE or enterprise
tenant.

## Benchmark design

Use task-local representative fixtures and include hard negatives, tool errors,
long-context cases and unsafe requests where applicable. Freeze cases and gates
before execution. Record model/provider/host versions, settings, tool surface,
repetitions, raw outputs, grader identity, latency, tokens and observable cost.

Compare blocking quality and safety first. Then compare efficiency among passing
candidates. Do not average away one severe safety or authority failure.

## Tiering

- Use a fast model for bounded, reversible, well-specified work after it clears
  the task gate.
- Use stronger reasoning for ambiguous planning, integration, high consequence
  or cross-domain synthesis.
- Escalate based on uncertainty, failed verification, risk or tool failure.
- Prefer an evaluator with different failure incentives or evidence access when
  correlated error is material.

## Re-evaluation

Trigger review on model/host deprecation, changed pricing or limits, new tool or
data requirements, quality drift, incident, provider outage, policy change or a
material workload shift. Time alone is a backstop, not proof of staleness.
