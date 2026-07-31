# Agent Optimizer

Improves one healthy agent or subagent against a frozen measurable quality, cost, latency, reliability, context or documentation target while preserving mission, authority, consumers and lifecycle invariants

This generated package is installable by Claude Code, Codex, and Cursor. Its canonical source lives under `skills/` in the repository root; do not edit this bundle directly.

## Bundled skills

- `agent-optimizer`

## Companion skill dependencies

> **DEPENDENCY WARNING:** Claude Code auto-installs the required companions from this marketplace. Codex and Cursor require the dependency-first install plan below before using affected routes.

Required:

- `agent-evaluator>=1.0.0` — Optimization requires a frozen baseline and independent candidate comparison.

Recommended:

- None.

Codex install order:

```bash
codex plugin add agent-evaluator@im-skills
codex plugin add agent-optimizer@im-skills
```

The machine-readable declaration is in `skill-dependencies.json`.

No credentials or host-specific absolute paths are included. Review bundled scripts before execution.
