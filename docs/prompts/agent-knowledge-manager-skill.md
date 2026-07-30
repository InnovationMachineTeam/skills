# Мастер-промпт навыка `agent-knowledge-manager`

Применяй после [agent-skill-base.md](agent-skill-base.md). Создай skill для
curated project knowledge и agent memory через `docs/`, LLM Wiki, optional
Obsidian views и generated Graphify/GraphRAG projections. Он не хранит raw
chain-of-thought, secrets или rapidly changing runtime state.

## Knowledge contract

Use stable document IDs, type/status/owner/version/updated/sources/related/tags
frontmatter, atomic pages and maps of content. Separate facts, interpretations,
decisions, conflicts, incidents and learnings. New material enters inbox,
receives provenance/trust/freshness checks, then an accountable curator
publishes or rejects it. Supersede rather than silently overwrite.

## Retrieval and projections

Start with Markdown + exact/BM25 search. Generate graph nodes/typed edges with
source locator, hash, confidence and timestamp. Add vector DB, Neo4j/Qdrant or
GraphRAG only after measured retrieval failures justify setup, operators,
tenancy, auth, backup, deletion propagation, reindex and SLO costs. Generated
indexes are disposable projections; docs/registries remain canonical.

## Agent use

Produce minimal provenance-bearing context capsules, respect data class and
consumer scope, record retrieval evidence, detect contradictions and enforce
freshness/TTL. Test poisoning, stale sources, deletion, access denial, missing
provenance, index drift and recovery.
