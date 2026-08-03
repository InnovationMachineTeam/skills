# Prompt Master

Builds versioned prompt packages by reconstructing, generalizing, specializing, merging, decomposing, auditing or optimizing durable prompts

This generated package is installable by Claude Code, Codex, and Cursor. Its canonical source lives under `skills/` in the repository root; do not edit this bundle directly.

## Bundled skills

- `prompt-master`

## Companion skill dependencies

> **DEPENDENCY WARNING:** Claude Code auto-installs the required companions from this marketplace. Codex and Cursor require the dependency-first install plan below before using affected routes.

Required:

- `prompt-optimize>=3.0.0` — Core prompt audit, architecture, authority resolution, drafting, and behavioral evaluation are delegated to the existing specialist.

Recommended:

- None.

Codex install order:

```bash
codex plugin add prompt-optimize@im-skills
codex plugin add prompt-master@im-skills
```

The machine-readable declaration is in `skill-dependencies.json`.

No credentials or host-specific absolute paths are included. Review bundled scripts before execution.
