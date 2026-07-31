# Agent Refactor

Assesses and safely changes the capability, ownership or topology boundaries of existing individual agents through merge, split, extraction, composition, promotion to a team, or public/private capability and documentation migration

This generated package is installable by Claude Code, Codex, and Cursor. Its canonical source lives under `skills/` in the repository root; do not edit this bundle directly.

## Bundled skills

- `agent-refactor`

## Companion skill dependencies

> **DEPENDENCY WARNING:** Claude Code auto-installs the required companions from this marketplace. Codex and Cursor require the dependency-first install plan below before using affected routes.

Required:

- `agent-architect>=1.0.0` — New individual-agent boundaries require a validated definition contract.
- `agent-evaluator>=1.0.0` — Old/new topology and consumer migrations require independent evaluation.
- `agent-manager>=1.0.0` — Lifecycle migration, rollout and retirement belong to the manager.

Recommended:

- `agent-team-architect>=1.1.0` — Recommended after an existing-agent migration decision promotes the asset into a team.

Codex install order:

```bash
codex plugin add agent-architect@im-skills
codex plugin add agent-evaluator@im-skills
codex plugin add agent-manager@im-skills
codex plugin add agent-refactor@im-skills
```

The machine-readable declaration is in `skill-dependencies.json`.

No credentials or host-specific absolute paths are included. Review bundled scripts before execution.
