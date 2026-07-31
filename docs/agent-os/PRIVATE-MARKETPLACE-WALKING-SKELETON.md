# Private marketplace Agentic OS walking skeleton

Bounded use case: one authenticated release request for this private skill
marketplace is evaluated against pinned policy and registry state, represented
as a durable run, verified against synthetic build evidence, observed through a
redacted trace and independently evaluated. The fixture never pushes, activates
production infrastructure or uses real credentials.

## Reused planes

- experience: existing CLI/user approval surfaces;
- knowledge: `agent-knowledge-manager` and curated `docs/`;
- team execution: `agent-team-orchestrator` where a run dispatches agents;
- marketplace packaging: existing deterministic build/validation scripts.

## New platform boundaries

- `agent-os-architect`: plane and vertical-slice design only;
- `agent-os-bootstrapper`: staged materialization only;
- `agent-registry-manager`: desired/observed reconciliation;
- `agent-runtime-manager`: durable platform run state;
- `agent-policy-manager`: decision and approval records, not action execution;
- `agent-observer`: read-only telemetry and alerts;
- `agent-os-evaluator`: frozen independent release evidence.

Fixtures under `tests/fixtures/agent-os-marketplace-release/` form a synthetic
request-to-terminal evidence chain. They are contracts and test data, not an
active service.
