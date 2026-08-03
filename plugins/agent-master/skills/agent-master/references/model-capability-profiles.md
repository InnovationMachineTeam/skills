# Model capability profiles

Choose procedural support from evidence, not a provider name or marketing tier.
The selected profile never grants authority or weakens safety gates.

## Decision table

| Evidence | Profile |
|---|---|
| Comparable evals show reliable planning, state tracking, tool recovery and contract compliance | `standard` |
| Model capability is unknown, mixed, untested or below a validated threshold | `constrained` |
| A standard run misses a blocking state, tool, authority or completion assertion | retry once with `constrained` |

Record `profile`, `evidence`, `selected_at`, `fallback`, and any profile change
in run state. Do not infer capability from model name alone.

## Invariants across profiles

- same goal, authority, data boundaries and Human gates;
- same required artifacts and Definition of Done;
- same state and rollback contract;
- same evaluation assertions;
- no hidden relaxation when context is limited.

When context is tight, load only the current phase, its inputs and its selected
profile. Summarize completed phases from validated state rather than replaying
their instructions.
