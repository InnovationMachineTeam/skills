# Agent Context

Builds a provenance-bearing design-time context package for creating, evaluating or changing one agent from explicitly scoped codebases, repositories, documents, sessions, traces, incidents and authorized web research

This generated package is installable by Claude Code, Codex, and Cursor. Its canonical source lives under `skills/` in the repository root; do not edit this bundle directly.

## Bundled skills

- `agent-context`

## Companion skill dependencies

> **DEPENDENCY WARNING:** Claude Code auto-installs the required companions from this marketplace. Codex and Cursor require the dependency-first install plan below before using affected routes.

Required:

- None.

Recommended:

- `agent-best-practices>=1.0.0` — Provides the curated agent and documentation evidence corpus.
- `agent-knowledge-manager>=1.0.0` — Recommended when reviewed context must enter durable project knowledge.
- `skill-harvester>=1.1.0` — Recommended for external skill, repository, document and trace intake.

Codex install order:

```bash
codex plugin add agent-context@im-skills
```

The machine-readable declaration is in `skill-dependencies.json`.

No credentials or host-specific absolute paths are included. Review bundled scripts before execution.
