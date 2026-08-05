# Model capability profiles

Choose orchestration support from comparable evidence rather than provider or
model name. Unknown capability defaults to `constrained`.

| Evidence | Profile |
|---|---|
| Reliable scenario selection, state updates, bounded handoffs, tool recovery and gate compliance on comparable evals | `standard` |
| Unknown, inconsistent or weaker performance on any required behavior | `constrained` |
| Standard run misses a blocking phase, authority or completion assertion | retry the current phase once with `constrained` |

Record `profile`, `evidence`, `fallback`, profile changes and the affected phase
in builder state. Both profiles preserve phase ownership, permissions, frozen
evaluation, rollback and Definition of Done.
