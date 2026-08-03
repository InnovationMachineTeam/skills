# Agent Master

Builds a governed agent system from a process description

This generated package is installable by Claude Code, Codex, and Cursor. Its canonical source lives under `skills/` in the repository root; do not edit this bundle directly.

## Bundled skills

- `agent-master`

## Companion skill dependencies

> **DEPENDENCY WARNING:** Claude Code auto-installs the required companions from this marketplace. Codex and Cursor require the dependency-first install plan below before using affected routes.

Required:

- None.

Recommended:

- `skill-builder>=1.4.0` — Recommended for evidence-backed skill lifecycle and productionization gates.
- `skill-architect>=1.2.0` — Recommended for capability form, visibility, boundary and host-native package decisions.
- `skill-evaluator>=1.1.0` — Recommended for independent frozen skill evaluation and holdout evidence.
- `prompt-optimize>=3.0.0` — Recommended for durable orchestrator and role-agent system prompts.
- `agent-team-architect>=1.1.0` — Recommended when the process justifies multiple standalone role agents.
- `agent-model-selector>=1.0.0` — Recommended when model selection must be evidence-backed per role.
- `agent-os-architect>=1.0.0` — Recommended when durable shared runtime planes are justified.
- `agent-observer>=1.0.0` — Recommended for operational logs, traces, metrics, SLOs and incident design.
- `agent-os-bootstrapper>=1.0.0` — Recommended when an approved harness walking skeleton must be materialized.
- `agent-os-evaluator>=1.0.0` — Recommended for independent harness integration, recovery and lifecycle evidence.

Codex install order:

```bash
codex plugin add agent-master@im-skills
```

The machine-readable declaration is in `skill-dependencies.json`.

No credentials or host-specific absolute paths are included. Review bundled scripts before execution.
