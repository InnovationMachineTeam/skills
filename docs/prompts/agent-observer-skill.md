# Мастер-промпт навыка `agent-observer`

Применяй после [agent-os-base.md](agent-os-base.md). Создай operations skill для
observability, SLO monitoring, MAPE-K reconciliation and incident evidence. Он
не исправляет production state без separate authority.

Define trace/span/event schemas linking user task, run, agent, model, prompt,
skill, tool, policy, approval, artifact and cost versions. Specify golden
signals, task-success and safety metrics, budgets, sampling/redaction,
correlation, retention and tenant boundaries. Separate symptoms from causes and
semantic quality from mechanical availability.

Detect loops, stuck leases, retry storms, drift, retrieval poison, model
degradation and cost anomalies. Produce alerts with owner/runbook and bounded
diagnostics bundle. Test missing/duplicate/out-of-order telemetry, PII leakage,
alert storms, false confidence and observer outage.
