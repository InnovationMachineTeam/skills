# Agent Scout

Identifies and prioritizes justified opportunities for one agent or subagent from tasks, sessions, code, documents, incidents and recurring work, then checks whether code, a model call, workflow, existing agent, team or Agentic OS...

This generated package is installable by Claude Code, Codex, and Cursor. Its canonical source lives under `skills/` in the repository root; do not edit this bundle directly.

## Bundled skills

- `agent-scout`

## Companion skill dependencies

> **DEPENDENCY WARNING:** Claude Code auto-installs the required companions from this marketplace. Codex and Cursor require the dependency-first install plan below before using affected routes.

Required:

- None.

Recommended:

- `agent-best-practices>=1.0.0` — Provides selection, lifecycle and maintenance criteria.
- `agent-context>=1.0.0` — Recommended when the opportunity decision needs additional evidence.

Codex install order:

```bash
codex plugin add agent-scout@im-skills
```

The machine-readable declaration is in `skill-dependencies.json`.

No credentials or host-specific absolute paths are included. Review bundled scripts before execution.
