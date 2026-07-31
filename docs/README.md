# Documentation Map

`docs/` is the canonical human-reviewable memory for repository intent,
decisions, contracts, evidence and operations. Code remains authoritative for
implemented behavior; registries and schemas remain authoritative for their
machine-readable state.

## Start here

- [Architecture](ARCHITECTURE.md)
- [Agent assets registry](AGENT-ASSET-REGISTRY.md)
- [Agent-skill bindings](AGENT-SKILLS-MAP.md)
- [Decision records](decisions/README.md)
- [Agent documentation contract](agents/README.md)
- [Prompt catalogue](prompts/README.md)
- [Knowledge plane](KNOWLEDGE-PLANE.md)
- [Release process](RELEASE.md)

Create a directory only when an owned artifact needs it. Generated projections
belong in `docs/generated/` and must not be edited directly. Canonical and
operational documents declare an owner, status, review trigger and consumers.
