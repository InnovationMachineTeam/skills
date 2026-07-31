# Agent Team Manager

>-

This generated package is installable by Claude Code, Codex, and Cursor. Its canonical source lives under `skills/` in the repository root; do not edit this bundle directly.

## Bundled skills

- `agent-team-manager`

## Companion skill dependencies

> **DEPENDENCY WARNING:** Claude Code auto-installs the required companions from this marketplace. Codex and Cursor require the dependency-first install plan below before using affected routes.

Required:

- `agent-model-selector>=1.0.0` — The design route delegates current model selection and evidence.
- `agent-skill-mapper>=1.0.0` — The map-capabilities route delegates governed agent-skill bindings.
- `agent-team-architect>=1.0.0` — The design route delegates team architecture.
- `agent-team-builder>=1.0.0` — The build route delegates staged team materialization.
- `agent-team-orchestrator>=1.0.0` — The operate route delegates runtime task orchestration.

Recommended:

- `agent-workspace-manager>=1.0.0` — Recommended when an operation needs isolated worktrees or workspace lifecycle management.

Codex install order:

```bash
codex plugin add agent-model-selector@im-skills
codex plugin add agent-skill-mapper@im-skills
codex plugin add agent-team-architect@im-skills
codex plugin add agent-team-builder@im-skills
codex plugin add agent-team-orchestrator@im-skills
codex plugin add agent-team-manager@im-skills
```

The machine-readable declaration is in `skill-dependencies.json`.

No credentials or host-specific absolute paths are included. Review bundled scripts before execution.
