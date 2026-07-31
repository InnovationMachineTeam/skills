# Catalog Instructions

`CLAUDE.md` and `AGENTS.md` at this level are a synchronized pair. Any change to
this file must be applied to `AGENTS.md` in the same directory, and any change
to `AGENTS.md` must be applied to this file. Keep the two files byte-identical.

- `entries.json`, `dependencies.json`, and `release.json` are canonical inputs.
- Skill identity and version must match `SKILL.md` metadata.
- Dependency declarations use exact names, minimum versions, reasons, and an
  acyclic install order.
- Marketplace categories are presentation metadata, not identity boundaries.
- Regenerate all host marketplaces and packages after catalog changes.
- Do not claim installation, activation, trust, or publication from catalog
  presence alone.
