# Extraction and Normalization

## Extract atomically

Split compound source material into independently testable units. Keep a workflow step separate from its rationale, a safety gate separate from its implementation, and a trigger separate from the body instructions it selects.

## Preserve two layers

1. **Observation**: what the source actually contains or demonstrates.
2. **Candidate**: the normalized reusable statement derived from that observation.

Do not edit the observation to make the candidate look stronger.

## Normalize carefully

- Replace local names with explicit variables only when meaning is preserved.
- Retain host, runtime, data, authority, and sequencing constraints.
- Separate mandatory invariants from optional implementation choices.
- Make preconditions, outputs, side effects, failure states, and recovery explicit.
- Record information lost during abstraction.

## Detect non-portability

Flag absolute paths, internal services, credentials, implicit tools, organization policy, undocumented host behavior, hidden state, environment assumptions, and coupled downstream consumers.

## Use the smallest useful unit

Too-large candidates are difficult to compare and validate. Too-small fragments lose purpose. A good unit has one outcome, recognizable inputs, bounded effects, and a falsifiable validation step.

## Avoid false novelty

Compare semantics rather than wording. A renamed checklist is not a new pattern; a shared phrase with different authority or recovery semantics may be materially different.
