---
name: agent-observer
description: Defines and audits Agentic OS telemetry, traces, SLOs, alerts, MAPE-K observations and bounded incident diagnostics linking task, run, agent, model, prompt, skill, tool, policy, approval, artifact, cost and versions. Use when instrumenting or diagnosing loops, stuck leases, retry storms, drift, retrieval poison, model degradation, cost anomalies or observer health. Read-only by default; do not repair production state, expose sensitive payloads, infer causes from symptoms, or claim semantic quality from availability metrics.
metadata:
  version: "1.0.0"
---

# Observe Agentic OS Runs

Separate observation from control. Telemetry is evidence and may itself be
missing, duplicated, delayed, poisoned or unavailable.

Read [references/telemetry-contract.md](references/telemetry-contract.md). Link
every event to stable trace/run/task IDs plus exact agent, model, prompt, skill,
tool, policy, approval and artifact versions where applicable. Apply sampling,
redaction, retention and tenant boundaries before storage or export.

```bash
python3 scripts/validate_trace_bundle.py trace-bundle.json
```

Measure golden signals, task outcome/safety, budgets and operator health.
Detect loops, lease expiry, retry storms, desired/observed drift, knowledge
poison and cost/latency anomalies. Correlate symptoms; name hypotheses and
missing evidence rather than declaring a cause.

Every alert has severity, owner, runbook, evidence window, dedupe key and clear
condition. Test missing/duplicate/out-of-order events, PII leakage, alert storms,
false confidence and observer outage. Return a redacted diagnostics bundle and
recommended control-plane action; mutation needs separate authority.
