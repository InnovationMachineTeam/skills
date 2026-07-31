# Prompt skill category and identity migration

Status: `CUTOVER`

Release: `3.0.0`

Owner: `InnovationMachineTeam`; reviewer: `@stanislavus86`.

## Mapping

| Source | Target | Identity |
|---|---|---|
| `skills/prompts/optimize-prompts` | `skills/prompt-skills/prompt-optimize` | renamed to `prompt-optimize@3.0.0` |

The new category makes its contents explicit as installable skills, while the
new noun-first identity aligns with the rest of the portfolio. The behavior,
permissions, resources and trigger boundary are unchanged.

## Consumer migration

- Catalog and release metadata use category `prompt-skills` and identity
  `prompt-optimize`.
- Registry identity, locator, version and content digest are reconciled.
- `skill-builder`, `metaskillpack` and `skill-best-practices` route to and
  track `prompt-optimize`.
- Marketplace packages are regenerated from the canonical category-aware
  source tree.
- Active documentation and tests reject the retired identity and location.

Historical migration records retain their original names as evidence.

## Acceptance gates

1. Exactly 28 globally unique skills are discovered at one category level.
2. `prompt-optimize@3.0.0` is the only active prompt optimizer identity.
3. Official skill validation passes for every canonical skill.
4. Registry identities, locators, versions and hashes match canonical sources.
5. Aggregate and individual packages contain the new identity and omit the old
   identity.
6. Codex installs and enables `prompt-optimize`; `optimize-prompts` is absent.
7. Canonical, marketplace and installed package trees match.

## Rollback

Rollback trigger: any failed discovery, routing, registry, packaging, upgrade
or host-install gate. Restore repository revision `e604f75`, refresh
`im-skills`, reinstall `optimize-prompts@2.0.0`, and rerun the `2.0.0`
validation suite. The migration changes no external data or infrastructure.

## Cutover evidence

Executed at `2026-07-31T10:03:45Z` from release commit `5fca721`.

- Repository suite: 37/37 tests passed.
- Official Agent Skills validator: 28/28 passed.
- Skill-local eval validators: 19/19 passed.
- Claude Code strict validation: aggregate plus 28/28 individual packages.
- Registry, generated views and three host adapters passed drift validation.
- Codex marketplace: 28/28 plugins installed and enabled.
- Updated consumers: `metaskillpack@1.3.0`, `skill-builder@1.3.0`,
  `skill-best-practices@1.2.0`, and `skill-marketplace-manager@1.2.0`.
- Prompt replacement: `prompt-optimize@3.0.0` enabled;
  `optimize-prompts` absent from installed state and active catalog.
- Delivery integrity: all 28 marketplace package trees match the canonical
  GitHub-backed marketplace clone.

The previous release remains recoverable through the rollback procedure.
