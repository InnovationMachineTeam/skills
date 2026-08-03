# Repository Scripts

Scripts build and validate deterministic projections from canonical skills,
catalog data, registries, and fixtures.

## Common tasks

| Task | Command |
|---|---|
| Validate the repository | `python3 scripts/validate_repository.py .` |
| Validate marketplace structure | `python3 scripts/validate_marketplace.py .` |
| Validate canonical documentation links | `python3 scripts/validate_documentation.py .` |
| Validate agent assets | `python3 scripts/manage_agent_assets.py validate .` |
| Validate skill dependencies | `python3 scripts/manage_skill_dependencies.py validate` |
| Audit context and hard-rule classes | `python3 scripts/audit_skill_context.py skills --format json` |
| Generate skill README usage guides | `python3 scripts/generate_skill_readmes.py .` |
| Check skill README usage guides | `python3 scripts/generate_skill_readmes.py . --check` |
| Build individual packages to staging | `python3 scripts/build_individual_plugins.py . <new-output>` |
| Build aggregate package to staging | `python3 scripts/build_aggregate.py . <new-output>` |
| Generate marketplace views | `python3 scripts/generate_marketplace.py .` |

Never point a builder at canonical `skills/` or an existing committed generated
directory. Use a new staging path, validate, compare, and promote the complete
artifact set only after review.
