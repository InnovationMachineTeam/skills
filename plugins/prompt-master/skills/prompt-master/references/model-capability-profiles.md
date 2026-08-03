# Model capability profiles

Select a workflow profile from comparable behavior, not a provider or model
name. Unknown capability defaults to `constrained`.

| Evidence | Profile |
|---|---|
| Reliable instruction hierarchy, entity separation, conflict resolution, structured output and self-checks on comparable evals | `standard` |
| Unknown, inconsistent or weaker performance on any of those behaviors | `constrained` |
| Standard run misses a blocking authority, evidence or output assertion | rerun once with `constrained` |

Record profile, evidence, fallback and observed failures. Both profiles retain
the same authority, output contract and blocking evaluations.
