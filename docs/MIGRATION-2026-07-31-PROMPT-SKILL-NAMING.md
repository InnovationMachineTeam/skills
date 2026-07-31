# Prompt skill category and identity migration

Status: `STAGED`

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

Pending successful validation and Codex installation.
