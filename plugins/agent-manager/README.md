# Agent Manager

Governs the lifecycle of one registered agent or subagent through inventory, candidate registration, approval, shadow, canary, activation, suspension, migration, rollback, deprecation and retirement with version, registry...

This generated package is installable by Claude Code, Codex, and Cursor. Its canonical source lives under `skills/` in the repository root; do not edit this bundle directly.

## Bundled skills

- `agent-manager`

## Companion skill dependencies

> **DEPENDENCY WARNING:** Claude Code auto-installs the required companions from this marketplace. Codex and Cursor require the dependency-first install plan below before using affected routes.

Required:

- `agent-evaluator>=1.0.0` — Activation and migration routes require independent release evidence.

Recommended:

- `agent-registry-manager>=1.0.0` — Recommended for Agentic OS desired-state registry transactions.
- `agent-runtime-manager>=1.0.0` — Recommended for Agentic OS runtime-instance lifecycle operations.

Codex install order:

```bash
codex plugin add agent-evaluator@im-skills
codex plugin add agent-manager@im-skills
```

The machine-readable declaration is in `skill-dependencies.json`.

No credentials or host-specific absolute paths are included. Review bundled scripts before execution.
