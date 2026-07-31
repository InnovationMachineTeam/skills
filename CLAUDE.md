# Repository Instructions

`CLAUDE.md` and `AGENTS.md` at this level are a synchronized pair. Any change to
this file must be applied to `AGENTS.md` in the same directory, and any change
to `AGENTS.md` must be applied to this file. Keep the two files byte-identical.

## Sources of truth

- Canonical skills live under `skills/<category>/<name>/`.
- Canonical marketplace metadata lives under `catalog/`.
- Canonical agent inventory and bindings are the JSON registries under `docs/`.
- `plugin/`, `plugins/`, and host marketplace manifests are generated; never
  edit them directly.
- Candidate assets are not installable until their promotion gate passes.

## Change discipline

- Preserve unrelated user changes.
- Use SemVer for every installed skill-content or contract change.
- Keep design, build, registration, mapping, activation, publication, and
  deployment as separate authorized transitions.
- Never embed credentials, private keys, tokens, personal local paths, or
  production endpoints.
- Prefer owner-private agent skills/commands until multiple justified consumers
  require a public marketplace skill.

## Documentation

- Start at `docs/README.md`; user onboarding is `docs/ONBOARDING.md`.
- Verify paths, commands, versions, roles, and state claims against canonical
  files before documenting them.
- Treat worked examples as blueprints unless evidence proves a real execution.
- Every created agent declares document read/write/ownership/verification roots.

## Verification

Run repository validation and the full unit suite before release. Generated
artifacts must be rebuilt in staging and compared with committed projections.
