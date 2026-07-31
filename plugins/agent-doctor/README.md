# Agent Doctor

Diagnoses unhealthy or broken behavior in one agent or subagent, reproduces symptoms from definitions and traces, identifies a root cause, applies an explicitly authorized minimal repair to a new candidate revision, and verifies recovery

This generated package is installable by Claude Code, Codex, and Cursor. Its canonical source lives under `skills/` in the repository root; do not edit this bundle directly.

## Bundled skills

- `agent-doctor`

## Companion skill dependencies

> **DEPENDENCY WARNING:** Claude Code auto-installs the required companions from this marketplace. Codex and Cursor require the dependency-first install plan below before using affected routes.

Required:

- None.

Recommended:

- `agent-evaluator>=1.0.0` — Provides frozen reproduction and independent recovery evidence.

Codex install order:

```bash
codex plugin add agent-doctor@im-skills
```

The machine-readable declaration is in `skill-dependencies.json`.

No credentials or host-specific absolute paths are included. Review bundled scripts before execution.
