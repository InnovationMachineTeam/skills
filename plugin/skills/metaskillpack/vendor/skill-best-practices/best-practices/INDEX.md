# Skill best-practices corpus

Practice-ID: BP-INDEX
Scope: mixed
Status: current
Sources: SRC-AS-001, SRC-AS-002, SRC-AS-003, SRC-AS-004, SRC-AS-005, SRC-AS-006, SRC-ANT-001, SRC-ANT-002, SRC-ANT-003, SRC-ANT-004, SRC-OAI-001, SRC-OAI-002, SRC-OAI-003, SRC-OAI-004, SRC-EX-001, SRC-EX-002, SRC-LOCAL-001, SRC-DER-001
Last-rebuilt: 2026-07-30
Revision: 2026-07-30-initial
Source-Snapshot: 2026-07-30-initial
Reconciliation: 2026-07-30-initial-reconciliation
Validation-Artifact: ../generated/practices-validation.json

This directory is a regenerated synthesis. Portable rules, platform contracts, enterprise governance, exemplar observations, and derived decisions remain explicitly scoped.

## Topics

1. [Specification and portability](01-specification-and-portability.md)
2. [Authoring and progressive disclosure](02-authoring-and-progressive-disclosure.md)
3. [Descriptions, discovery, and routing](03-descriptions-discovery-and-routing.md)
4. [Workflows, scripts, and tools](04-workflows-scripts-and-tools.md)
5. [Evaluation and optimization](05-evaluation-and-optimization.md)
6. [Security and authority](06-security-and-authority.md)
7. [Client implementation and context lifecycle](07-client-implementation.md)
8. [Enterprise lifecycle and governance](08-enterprise-lifecycle-and-governance.md)
9. [Meta-skills and orchestration](09-meta-skills-and-orchestration.md)
10. [Conflicts and unified decisions](10-conflicts-and-decisions.md)
11. [Checklists](11-checklists.md)

## Rebuild policy

Rebuild the complete directory when authoritative claims change, a new material source is accepted, a conflict or deprecation appears, corpus integrity fails, or the user explicitly requests a forced rebuild. Do not rewrite the corpus for transport-only changes.

## Current high-impact platform notes

- OpenAI hosts may truncate or omit skill descriptions from large initial catalogs; front-load differentiating use cases and test catalog-level discovery. [SRC-OAI-001]
- Anthropic API and enterprise limits, versions, retention, per-request skill counts, and distribution behavior are dynamic host facts; refresh them before implementation. [SRC-ANT-002, SRC-ANT-003]
- The open standard permits optional frontmatter fields, while a strict portable core can still choose only `name` and `description` and move host metadata to adapters. [SRC-AS-001]
