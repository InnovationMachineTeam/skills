# Master Prompt For The `agent-model-selector` Skill

Apply after [agent-skill-base.md](agent-skill-base.md). Create an evidence-based
skill for selecting the most effective models for roles and routes. It provides
a versioned policy recommendation, but it does not procure access or change provider
configuration.

## Selection procedure

1. Resolve task class, quality floor, tool/code/vision/context needs, latency,
   throughput, cost, data residency, provider and fallback constraints.
2. Fetch current authoritative model documentation and availability; record
   checked date and target host version. Never select from stale memory alone.
3. Build a minimal candidate set by capability, then benchmark representative
   and adversarial tasks with fixed prompts/tools/data.
4. Compare task success, calibrated confidence, tool reliability, safety,
   latency, token/cost efficiency and variance across repeated runs.
5. Recommend quality tiers per route: fastest model that clears the gate,
   stronger escalation for uncertainty/high risk, and independent evaluator
   chosen to reduce correlated failure.
6. Define fallback ladder, outage/degradation behavior, budgets, pinning,
   migration and re-evaluation triggers.

## Output

Return preferred model per host/role, exact assumptions and versions, measured
trade-offs, fallback policy, unsupported cases and next review date. Do not
claim one model is universally best.
