# Model routing policy contract

## Contents

- Policy identity
- Approved model pool
- Route decisions
- Evaluation and operations

## Policy identity

Record `schema_version`, stable policy ID, SemVer, lifecycle status, accountable
owner, target hosts, policy reference, checked date and immutable evidence refs.
Separate a policy candidate from runtime configuration and observed route state.

## Approved model pool

For every model record exact provider, pinned identifier/version, regions,
hosts, modalities, tools, context, structured output, data classes, retention,
rate/quota constraints and authoritative evidence. Unknown capability is not
supported capability.

## Route decisions

Derive typed features outside untrusted task text. Each route declares task
class, risk/data/tool constraints, primary model, confidence threshold, quality
floor, latency/cost/token budgets, escalation, approved fallback order, degraded
mode and hard stop. A fallback must not weaken policy or the quality floor.

Use fixed routing by default, tiered routing when a small explicit decision
table suffices, and dynamic routing only after comparable evidence shows a
material benefit.

## Evaluation and operations

Record frozen evaluation reference, metrics, thresholds, model/evaluator
correlation risk, shadow and canary contract, telemetry, drift signals,
observation window, circuit breaker, rollback target and review triggers.
Unavailable or stale evidence yields `INCONCLUSIVE`, never an invented route.
