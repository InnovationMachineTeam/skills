# Marketplace Catalog

The catalog is canonical input to marketplace generation.

| File | Responsibility |
|---|---|
| `entries.json` | globally unique skill entries, categories, and tags |
| `dependencies.json` | required/recommended companion graph and reasons |
| `release.json` | marketplace identity, publisher, categories, and aggregate release |

Skill name and version come from each canonical `SKILL.md`. After a catalog
change, regenerate all host marketplace manifests and packages, validate
dependency order and drift, and review the complete output. Catalog presence
does not imply installation, activation, trust, or production approval.
