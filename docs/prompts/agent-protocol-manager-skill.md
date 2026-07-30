# Мастер-промпт навыка `agent-protocol-manager`

Применяй после [agent-os-base.md](agent-os-base.md). Создай ports-and-adapters
skill for MCP, A2A, host and provider boundaries. Он не скрывает semantic
differences behind false portability.

Inventory pinned protocol/host versions, discovery, authentication, capability
negotiation, schemas, streaming, cancellation, errors, retries and lifecycle.
Define canonical internal contracts and explicit native/generated/unsupported
adapter outcomes. Validate inputs/outputs, provenance, content type, size,
timeouts, idempotency and least-privilege credentials at every boundary.

Build conformance fixtures for success, denial, malformed data, partial stream,
disconnect, duplicate message, unsupported feature and downgrade. Record
compatibility matrix, generated-artifact drift and upgrade/rollback procedure.
