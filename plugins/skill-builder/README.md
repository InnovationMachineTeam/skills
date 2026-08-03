# Skill Builder

Orchestrates evidence-backed, multi-stage skill creation, adoption, evaluation, repair, optimization, refactoring, migration and governance through specialist skills

This generated package is installable by Claude Code, Codex, and Cursor. Its canonical source lives under `skills/` in the repository root; do not edit this bundle directly.

## Bundled skills

- `skill-builder`

## Companion skill dependencies

> **DEPENDENCY WARNING:** Claude Code auto-installs the required companions from this marketplace. Codex and Cursor require the dependency-first install plan below before using affected routes.

Required:

- `prompt-optimize>=3.0.0` — The prompt-development scenario delegates prompt design and optimization.
- `skill-architect>=1.2.0` — Creation and topology scenarios delegate skill architecture.
- `skill-doctor>=1.0.0` — Repair scenarios delegate diagnosis and minimal repair.
- `skill-evaluator>=1.1.0` — Evaluation and release gates require independent skill evaluation.
- `skill-harvester>=1.1.0` — Research and external intake scenarios delegate evidence harvesting.
- `skill-manager>=1.2.0` — Lifecycle, installation and governance scenarios delegate installed-state management.
- `skill-optimizer>=1.0.0` — Measured improvement scenarios delegate healthy-skill optimization.
- `skill-refactor>=1.2.0` — Split, merge, extraction and boundary-change scenarios delegate refactoring.
- `skill-scout>=1.1.0` — Opportunity-discovery scenarios delegate skill scouting.

Recommended:

- None.

Codex install order:

```bash
codex plugin add prompt-optimize@im-skills
codex plugin add skill-architect@im-skills
codex plugin add skill-doctor@im-skills
codex plugin add skill-evaluator@im-skills
codex plugin add skill-harvester@im-skills
codex plugin add skill-manager@im-skills
codex plugin add skill-optimizer@im-skills
codex plugin add skill-refactor@im-skills
codex plugin add skill-scout@im-skills
codex plugin add skill-builder@im-skills
```

The machine-readable declaration is in `skill-dependencies.json`.

No credentials or host-specific absolute paths are included. Review bundled scripts before execution.
