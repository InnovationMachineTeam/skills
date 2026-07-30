# skill-best-practices

`skill-best-practices` maintains a source-backed corpus of practices for agent skills. It checks canonical sources for updates, compares snapshots, reconciles claims, conditionally rebuilds the full thematic practice directory, and generates a master prompt for auditing or modifying a declared set of skills.

## Routes

1. `query-practices`
2. `source-audit`
3. `refresh-sources`
4. `reconcile-practices`
5. `rebuild-practices`
6. `generate-modification-prompt`
7. `apply-practices`
8. `full-refresh`

## Important files

- `sources/resources.md` — readable source inventory;
- `sources/registry.json` — machine-readable source registry;
- `sources/baseline-snapshot.json` — initial semantic comparison point;
- `sources/reconciliation-status.json` — claim-decision state bound to the current revision;
- `sources/*.md` — thematic source summaries;
- `best-practices/` — regenerated thematic guidance;
- `best-practices/claims.json` — section-level provenance and drift hashes;
- `managed-skills.md` and `managed-skills.json` — declared audit/update targets;
- `generated/modify-managed-skills.md` — current modification master prompt;
- `generated/practices-validation.json` — corpus/registry validation binding;
- `evals/` — routing and behavioral regression cases.

## Safety model

The skill defaults to read-only source checking. Rebuilds happen in staging. Active installed skills are never rewritten by assumption, and portfolio changes are delegated through the appropriate creator, doctor, optimizer, refactor, builder, and manager workflows.

The package is a reviewable bundle and does not install or activate itself.
