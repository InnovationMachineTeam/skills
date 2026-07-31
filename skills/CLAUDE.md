# Canonical Skill Instructions

`CLAUDE.md` and `AGENTS.md` at this level are a synchronized pair. Any change to
this file must be applied to `AGENTS.md` in the same directory, and any change
to `AGENTS.md` must be applied to this file. Keep the two files byte-identical.

- This tree is canonical; generated packages are not edit targets.
- Every skill has one `SKILL.md`, accurate trigger/non-trigger boundaries, and
  `metadata.version` using SemVer.
- Keep the main instructions concise and progressively load references, scripts,
  prompts, assets, and evals only when needed.
- Scripts must be deterministic where possible, scoped, fail closed, and avoid
  hidden network or credential assumptions.
- Create routing, behavior, negative, security, and regression evaluations in
  proportion to risk.
- Owner-only capabilities belong inside their agent definition, not this public
  marketplace tree.
- Rebuild generated packages and verify registries, dependencies, hosts,
  upgrades, and rollback after a released change.
