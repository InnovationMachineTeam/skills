# Documentation Map

`docs/` is the canonical human-reviewable memory for repository intent,
decisions, contracts, evidence and operations. Code remains authoritative for
implemented behavior; registries and schemas remain authoritative for their
machine-readable state.

## Start here

- [Onboarding Guide](ONBOARDING.md) — choose one agent, a team, or Agentic OS
- [Worked use cases](use-cases/README.md) — concrete domain blueprints
- [Getting started](GETTING-STARTED.md) — install and verify
- [Architecture](ARCHITECTURE.md)
- [Configuration](CONFIGURATION.md)
- [Development](DEVELOPMENT.md)
- [Testing](TESTING.md)
- [Agent assets registry](AGENT-ASSET-REGISTRY.md)
- [Agent-skill bindings](AGENT-SKILLS-MAP.md)
- [Decision records](decisions/README.md)
- [Agent documentation contract](agents/README.md)
- [Prompt catalogue](prompts/README.md)
- [Knowledge plane](KNOWLEDGE-PLANE.md)
- [Release process](RELEASE.md)
- [Cross-domain insights](INSIGHTS-AGENT-SYSTEM-DESIGN.md)

## Documentation domains

| Domain | Canonical contents |
|---|---|
| `agents/` | agent specs, contexts, evaluations, operations, and changes |
| `decisions/` | accepted, rejected, superseded, and proposed decision records |
| `knowledge/` | curated concepts, provenance, and retrieval guidance |
| `prompts/` | reusable creation prompts; design inputs, not active skills |
| `use-cases/` | worked examples showing roles, skills, documents, and gates |

Project-specific agent systems may add `product/`, `research/`,
`requirements/`, `design/`, `architecture/`, `delivery/`, `quality/`, and
`operations/` when a named artifact and consumer require them. The
[Onboarding Guide](ONBOARDING.md#documentation-and-memory-contract) defines the
default ownership model.

Create a directory only when an owned artifact needs it. Generated projections
belong in `docs/generated/` and must not be edited directly. Canonical and
operational documents declare an owner, status, review trigger and consumers.

Local instructions are mirrored in `docs/CLAUDE.md` and `docs/AGENTS.md`.
Changing one requires the same change in the other.
