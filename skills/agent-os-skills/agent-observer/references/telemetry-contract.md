# Telemetry contract

Events carry schema version, event/trace/run/task IDs, type, timestamp, sequence,
producer, component versions, data class, redaction status and evidence refs.
Duplicate event IDs are invalid; gaps and out-of-order sequences are reported.

SLOs distinguish mechanical availability/latency from task success, safety and
semantic quality. Alerts link an accountable owner and tested runbook. Sensitive
content is minimized or referenced, never copied merely for convenience.
