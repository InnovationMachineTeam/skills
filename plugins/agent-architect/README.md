# Agent Architect

Designs or redesigns one bounded agent or subagent as an immutable, reviewable definition with mission, non-goals, inputs, outputs, tools, permissions, model policy, state, memory, documentation, evaluation, rollout and retirement contracts

This generated package is installable by Claude Code, Codex, and Cursor. Its canonical source lives under `skills/` in the repository root; do not edit this bundle directly.

## Bundled skills

- `agent-architect`

## Companion skill dependencies

> **DEPENDENCY WARNING:** Claude Code auto-installs the required companions from this marketplace. Codex and Cursor require the dependency-first install plan below before using affected routes.

Required:

- None.

Recommended:

- `agent-best-practices>=1.0.0` — Provides the evidence corpus for agent patterns and documentation contracts.
- `agent-model-selector>=1.0.0` — Provides current evidence-backed model policies when exact model selection is required.
- `agent-skill-mapper>=1.0.0` — Provides governed public/private capability binding analysis.

Codex install order:

```bash
codex plugin add agent-architect@im-skills
```

The machine-readable declaration is in `skill-dependencies.json`.

No credentials or host-specific absolute paths are included. Review bundled scripts before execution.
