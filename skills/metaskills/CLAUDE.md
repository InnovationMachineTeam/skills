# Metaskill Instructions

`CLAUDE.md` and `AGENTS.md` at this level are a synchronized pair. Any change to
this file must be applied to `AGENTS.md` in the same directory, and any change
to `AGENTS.md` must be applied to this file. Keep the two files byte-identical.

- Keep skill opportunity, context, architecture, evaluation, repair,
  optimization, refactoring, governance, and packaging responsibilities clear.
- Prefer one specialist for a known phase and a thin orchestrator for lifecycle
  routing.
- Composite packs read version-locked donors without editing or recursively
  invoking them.
- Stage replacements, freeze evaluation, preserve rollback, and require explicit
  approval before changing canonical or installed skills.
- Do not absorb individual-agent, team, or Agentic OS responsibilities.
