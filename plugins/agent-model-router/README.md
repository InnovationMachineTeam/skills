# Agent Model Router

Designs, audits and stages policy-constrained runtime routing across a pinned multi-model pool using typed task, risk, data, tool, context, latency, cost and quality features

This generated package is installable by Claude Code, Codex, and Cursor. Its canonical source lives under `skills/` in the repository root; do not edit this bundle directly.

## Bundled skills

- `agent-model-router`

## Companion skill dependencies

> **DEPENDENCY WARNING:** Claude Code auto-installs the required companions from this marketplace. Codex and Cursor require the dependency-first install plan below before using affected routes.

Required:

- None.

Recommended:

- `agent-model-selector>=1.0.0` — Provides current evidence-backed approved-pool selection before runtime routing.
- `agent-observer>=1.0.0` — Provides route telemetry, SLO and drift evidence.
- `agent-policy-manager>=1.0.0` — Provides authorization constraints for route decisions.

Codex install order:

```bash
codex plugin add agent-model-router@im-skills
```

The machine-readable declaration is in `skill-dependencies.json`.

No credentials or host-specific absolute paths are included. Review bundled scripts before execution.
