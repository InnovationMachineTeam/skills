# Agent Builder

Orchestrates complete evidence-backed workflows for one agent or subagent across agent-scout, agent-context, agent-architect, agent-evaluator, agent-doctor, agent-optimizer, agent-refactor and agent-manager

This generated package is installable by Claude Code, Codex, and Cursor. Its canonical source lives under `skills/` in the repository root; do not edit this bundle directly.

## Bundled skills

- `agent-builder`

## Companion skill dependencies

> **DEPENDENCY WARNING:** Claude Code auto-installs the required companions from this marketplace. Codex and Cursor require the dependency-first install plan below before using affected routes.

Required:

- `agent-architect>=1.0.0` — Creation and redesign scenarios delegate individual-agent architecture.
- `agent-context>=1.0.0` — Research scenarios delegate provenance-bearing context building.
- `agent-doctor>=1.0.0` — Repair and incident scenarios delegate diagnosis and recovery.
- `agent-evaluator>=1.0.0` — All release and comparison gates require independent evaluation.
- `agent-manager>=1.0.0` — Lifecycle transitions and host verification belong to the manager.
- `agent-optimizer>=1.0.0` — Measured improvement scenarios delegate healthy-agent optimization.
- `agent-refactor>=1.0.0` — Boundary and topology scenarios delegate refactoring.
- `agent-scout>=1.0.0` — Full lifecycle begins with the agent worth and coverage gate.

Recommended:

- `agent-best-practices>=1.0.0` — Provides shared evidence for pattern and lifecycle decisions.

Codex install order:

```bash
codex plugin add agent-architect@im-skills
codex plugin add agent-context@im-skills
codex plugin add agent-doctor@im-skills
codex plugin add agent-evaluator@im-skills
codex plugin add agent-manager@im-skills
codex plugin add agent-optimizer@im-skills
codex plugin add agent-refactor@im-skills
codex plugin add agent-scout@im-skills
codex plugin add agent-builder@im-skills
```

The machine-readable declaration is in `skill-dependencies.json`.

No credentials or host-specific absolute paths are included. Review bundled scripts before execution.
