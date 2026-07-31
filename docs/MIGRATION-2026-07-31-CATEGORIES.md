# Skill category and prompt-identity migration

Status: `STAGED`

Release: `2.0.0`

Owner: `InnovationMachineTeam`; reviewer: `@stanislavus86`.

## Mapping

| Source | Target | Identity |
|---|---|---|
| `skills/metaskills/agent-{observer,policy-manager,registry-manager,runtime-manager}` | `skills/agent-os-skills/<name>` | unchanged |
| `skills/metaskills/agent-os-*` | `skills/agent-os-skills/<name>` | unchanged |
| `skills/metaskills/agent-team-*` | `skills/agent-team-skills/<name>` | unchanged |
| `skills/metaskills/agent-workspace-manager` | `skills/agent-team-skills/agent-workspace-manager` | unchanged |
| `skills/metaskills/agent-{knowledge-manager,model-selector,skill-mapper}` | `skills/agent-skills/<name>` | unchanged |
| `skills/metaskills/optimize-master-prompts` | `skills/prompts/optimize-prompts` | renamed to `optimize-prompts@2.0.0` |

All other skill-engineering capabilities remain under `skills/metaskills/`.
Categories organize ownership and discovery; names remain globally unique.

## Consumer migration

- Catalog entries now declare their canonical category.
- Registry locators and the prompt optimizer asset identity are reconciled.
- Repository tests resolve category-aware source paths.
- Marketplace generators read per-entry categories and continue producing one
  flattened, self-contained plugin per skill.
- `skill-builder`, `metaskillpack`, and `skill-best-practices` route to and
  track `optimize-prompts`.
- The old `optimize-master-prompts` plugin is removed from the active catalog.

## Acceptance gates

1. Exactly 28 globally unique skills are discovered at one category level.
2. Catalog category declarations equal the canonical filesystem layout.
3. Official skill validation passes for every canonical skill.
4. Registry identities, locators, versions and hashes match canonical sources.
5. All three marketplaces expose identical selective inventory.
6. Every individual package contains exactly one expected skill.
7. Aggregate and individual Claude Code packages pass strict validation.
8. Codex upgrades retain unchanged identities and replace the renamed prompt
   optimizer without leaving the old plugin enabled.

## Rollback

Rollback trigger: any failed discovery, routing, registry, packaging, upgrade or
host-install gate. Restore the previous known-good repository revision
`c25e6ee`, refresh `im-skills`, reinstall or re-enable
`optimize-master-prompts@1.0.0`, and rerun the `1.8.0` validation suite. The
migration changes no external data or infrastructure. Repository recovery is
owned by `InnovationMachineTeam` and reviewed by `@stanislavus86`.
