# Managed skills

This list declares the locally created skills that the generated modification master prompt should inspect. It is not proof that a skill is installed, active, healthy, owned, or writable. Resolve every target at runtime.

| Skill | Role | Default |
|---|---|---|
| `prompt-optimize` | Prompt creation, audit, adaptation, and evaluation | audit |
| `skill-builder` | End-to-end and resumable orchestration | audit |
| `skill-architect` | Skill classification, architecture, and creation | audit |
| `skill-doctor` | Diagnosis and recovery verification | audit |
| `skill-evaluator` | Independent eval design, execution, comparison, and release evidence | audit |
| `skill-harvester` | Evidence and reusable-component harvesting | audit |
| `skill-manager` | Versions, installation, activation, governance, retirement | audit |
| `skill-marketplace-manager` | Marketplace architecture, validation, migration, and release | audit |
| `skill-optimizer` | Measured optimization of healthy skills | audit |
| `skill-refactor` | Composition, merge, split, extraction, facade migration | audit |
| `skill-scout` | Opportunity discovery and build/no-build decisions | audit |
| `skill-best-practices` | Source refresh and practice maintenance | staged audit only |

Machine-readable contract: `managed-skills.json`.

## Update policy

- Add a target only after its identity and role are known.
- Keep exact installation state outside this intent list and verify it through `skill-manager`.
- Modify one target through the responsible specialist and preserve catalog-level regressions.
- Never let `skill-best-practices` rewrite its active installed copy; produce a sibling candidate version.
