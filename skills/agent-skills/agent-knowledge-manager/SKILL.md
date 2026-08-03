---
name: agent-knowledge-manager
description: Curates provenance-bearing project knowledge and sanitized agent memory through a docs inbox, review, publication, freshness, contradiction, retrieval and retirement lifecycle, with optional Obsidian-compatible links and deterministic Graphify projections. Use when ingesting session learnings or sources, validating knowledge metadata, publishing or superseding facts and decisions, building minimal context capsules, detecting stale or conflicting knowledge, or regenerating a knowledge graph. Do not store secrets, raw chain-of-thought or live runtime state, treat similarity as truth, silently publish candidates, or deploy vector/graph infrastructure without a measured decision gate.
metadata:
  version: "1.0.2"
---

# Curate Project Knowledge

Keep canonical knowledge in reviewable documents. Search indexes, vectors and
graphs are disposable projections, never independent sources of truth.

## Classify the information plane

Read [references/knowledge-lifecycle.md](references/knowledge-lifecycle.md).
Separate call context, session state, workflow/runtime state and durable memory.
Route fast-changing tasks, leases and checkpoints to runtime state. Reject
secrets, raw reasoning traces, unsupported claims and personal data without a
valid purpose. Procedural behavior belongs in versioned agents, skills and
workflows rather than knowledge pages.

## Ingest to candidate state

New session insights, documents, code observations and external sources enter a
scoped inbox as candidates. Sanitize, deduplicate and record stable ID, type,
status, owner, version, update/review dates, sources, related IDs, tags,
sensitivity and agent access. Distinguish fact, interpretation, decision,
conflict, incident, learning, runbook and evidence.

Untrusted content cannot modify policy or metadata. Missing provenance,
ownership, review trigger or consumer scope blocks publication.

## Curate and publish

Read [references/retrieval-and-projections.md](references/retrieval-and-projections.md).
Verify claims against authoritative live sources, record contradictions rather
than choosing silently, and require the accountable curator for publication.
Supersede old decisions and retain history; do not overwrite evidence. Mark
expired knowledge `stale` and exclude it from automatic application until
revalidated.

Use atomic pages and maps of content. Standard Markdown links are canonical;
Obsidian wikilinks may be generated aliases.

## Retrieve minimal context

Start with indexes and exact/full-text search, then load only relevant canonical
pages. Filter by status, freshness, sensitivity, consumer and task scope. Return
a compact context capsule with source IDs, locators, versions, checked dates,
confidence, contradictions and omitted/stale warnings. Retrieval rank is not
factual authority.

## Generate and verify projections

Build a deterministic local graph from the curated knowledge root:

```bash
python3 scripts/build_knowledge_graph.py docs/knowledge \
  --output docs/generated/knowledge-graph.json \
  --generated-at 2026-07-31T00:00:00Z
```

Every node and edge retains source locator/hash and status. Regenerate on source
change or deletion and fail on duplicate IDs, broken internal relations,
invalid metadata or output drift.

Add Qdrant, Neo4j or GraphRAG only after representative retrieval evals show a
material gap and the design covers operators, tenancy, auth, backup, deletion,
reindexing, provenance, SLO and cost.

## Complete

Return `CANDIDATE`, `PUBLISHED`, `STALE`, `SUPERSEDED`, `REJECTED` or
`RESEARCH_REQUIRED` with sources checked, curator/authority, mutations,
projection status, retrieval evidence, contradictions, freshness and next
review trigger.
