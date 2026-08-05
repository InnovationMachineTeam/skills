---
name: agent-model-router
description: Designs, audits and stages policy-constrained runtime routing across a pinned multi-model pool using typed task, risk, data, tool, context, latency, cost and quality features. Use when multi-model per-request routing is measurably justified and needs thresholds, escalation, fallbacks, outage handling, shadow/canary evidence, drift detection or rollback. Do not use for one-time design-time model selection, provider purchasing or configuration, unverified model comparisons, or allowing task text to choose a provider or weaken data controls.
metadata:
  version: "1.0.3"
---

# Govern Runtime Model Routing

Create a versioned control-plane policy that routes only among approved,
pinned model identities. Dynamic choice is a constrained policy decision, not
an instruction-following privilege granted to task content.

## Establish justification and authority

Resolve task classes, risk tiers, data classes, tools, modalities, context,
quality floors, latency/cost budgets, target hosts/providers/regions and
operating owner. Require current authoritative capability and availability
evidence with checked dates. Route one-time model choice to
`agent-model-selector`.

Reject dynamic routing when a fixed or tiered policy meets the measured need,
representative evals do not exist, the approved pool is unknown, or no owner can
operate drift, outage and rollback. Default to a read-only policy proposal.

Read [references/skill-dependencies.md](references/skill-dependencies.md) when
the route needs a recommended companion. Missing companions limit only their
named evidence layer; never imitate them.

## Build the routing policy

Read [references/model-routing-contract.md](references/model-routing-contract.md).

1. Define a typed feature schema. Never accept provider or model identity from
   untrusted task text.
2. Pin every approved model version, host/provider constraint, data policy and
   evidence reference.
3. Reject ineligible models before scoring quality, latency or cost.
4. Map each route to one primary model, confidence threshold, quality floor,
   budgets, escalation condition, fallback ladder and hard stop.
5. Preserve the same security and quality floor across fallbacks. Provider
   outage may degrade to approved read-only or human handling, not arbitrary
   substitution.
6. Record correlated producer/evaluator risk and use an independently justified
   evaluator route where consequence warrants it.
7. Define shadow evaluation, canary limits, drift signals, observation window,
   rollback target, deprecation and retirement.

Validate the candidate:

```bash
python3 scripts/validate_model_routing_policy.py model-routing-policy.json
```

## Evaluate before rollout

Freeze representative, adversarial and failure cases before routing runs.
Measure success, safety, latency, cost, variance, tool compatibility and route
stability. Test unavailable model, rate/quota failure, context overflow,
unsupported tool or modality, degraded quality, low confidence, manipulated
features, stale evidence and rollback.

Use `agent-evaluator` for independent evidence, `agent-policy-manager` for
authorization policy and `agent-observer` for operational signals. A passing
offline policy does not authorize provider configuration, canary or activation.

## Complete

Return policy identity/version/status, justification, approved pool and source
dates, route table, exclusions, thresholds, fallbacks, evaluation evidence,
drift/rollback plan, residual risks and configuration/activation status.
