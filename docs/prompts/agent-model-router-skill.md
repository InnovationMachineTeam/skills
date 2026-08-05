# Master Prompt For The `agent-model-router` Skill

Apply after [agent-os-base.md](agent-os-base.md). Create a control-plane skill
for fixed, tiered, or dynamic model routing only when multi-model operation is
measurably justified.

Route from typed task/risk/data/tool/context/latency/cost features to an
approved model pool. Require current authoritative capability data, pinned
versions, representative eval scores, confidence thresholds, escalation,
fallback and provider outage policy. Constrain dynamic choice by policy; never
let untrusted task text choose provider or weaken data controls.

Measure success/cost/latency/variance and correlated producer–evaluator error.
Use shadow tests before changing routes, canary rollout, drift detection and
rollback. Test unavailable model, quota/rate limit, context overflow, tool
incompatibility, degraded quality and adversarial route manipulation.
