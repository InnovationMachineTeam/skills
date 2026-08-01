# Agent Protocol Manager

Designs, audits and stages explicit ports-and-adapters contracts for MCP, A2A, agent hosts and model/tool providers, including pinned versions, discovery, authentication, capability negotiation, schemas, streaming, cancellation...

This generated package is installable by Claude Code, Codex, and Cursor. Its canonical source lives under `skills/` in the repository root; do not edit this bundle directly.

## Bundled skills

- `agent-protocol-manager`

## Companion skill dependencies

> **DEPENDENCY WARNING:** Claude Code auto-installs the required companions from this marketplace. Codex and Cursor require the dependency-first install plan below before using affected routes.

Required:

- None.

Recommended:

- `agent-os-evaluator>=1.0.0` — Provides independent protocol conformance and platform release evidence.
- `agent-policy-manager>=1.0.0` — Provides cross-boundary authorization and approval policy.

Codex install order:

```bash
codex plugin add agent-protocol-manager@im-skills
```

The machine-readable declaration is in `skill-dependencies.json`.

No credentials or host-specific absolute paths are included. Review bundled scripts before execution.
