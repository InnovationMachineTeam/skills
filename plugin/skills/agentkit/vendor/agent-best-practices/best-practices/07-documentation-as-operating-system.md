# Documentation as the Project Operating System

## Why a Project Needs `docs/`

For agentic development, `docs/` is not a post-release showcase, but the shared
long-term memory of humans and agents. It answers four questions:

1. Why does the system exist and what outcome is needed?
2. What must the system do and not do?
3. How is it designed and why were these decisions chosen?
4. How should it be built, tested, released, and operated?

Code remains the source of truth for the current implementation, the
specification for expected behavior, decision records for rationale, and
runbooks for operating procedures. You must not declare one document to be the
source of truth for all types of knowledge.

## Recommended Structure

```text
docs/
├── README.md                  # documentation map and usage rules
├── product/                   # vision, outcomes, users, roadmap, bets
├── discovery/                 # research, interviews, hypotheses, experiments
├── requirements/              # functional, quality, constraints, traceability
├── architecture/              # context, containers, interfaces, data, risks
├── decisions/                 # subject-first decision records
│   └── architecture/          # ADR/MADR by default
├── design/                    # UX, interaction, visual and service design
├── delivery/                  # plans, releases, migrations, change records
├── operations/                # runbooks, SLO, alerts, incidents, continuity
├── security/                  # threat models, data classification, controls
├── quality/                   # test strategy, evals, quality gates
├── agents/                    # agent catalog, workflows, policies, runbooks
├── reference/                 # APIs, schemas, glossary, commands
├── tutorials/                 # learning-oriented paths
├── how-to/                    # task-oriented guides
├── explanation/               # concepts and rationale
└── generated/                 # reproducible projections; do not edit manually
```

This extends Diataxis, including tutorials, how-to, reference, and explanation,
with product and agent-system lifecycle documents
([Diataxis](https://diataxis.fr/)). Do not create empty folders in advance: the
tree grows according to actual needs.

## Document Classes

Each file must belong to one of these classes:

| Class | Examples | Rule |
|---|---|---|
| Canonical | PRD, spec, API contract, policy | The single active owner of truth for that type |
| Decision | ADR, governance decision | Append-mostly; supersede, do not rewrite history |
| Operational | Runbook, rollback, incident plan | Validate through drills and production signals |
| Guidance | How-to, tutorial, explanation | Optimize for the reader's task |
| Evidence | Test report, research, eval | Immutable snapshot with provenance |
| Projection | Index, dashboard, generated API docs | Regenerate from canonical sources |
| Ephemeral | Draft, scratch analysis | TTL or explicit archival |

## Document Metadata

Canonical and operational documents SHOULD have frontmatter:

```yaml
---
id: arch-checkout
title: Checkout architecture
status: active
owner: checkout-team
reviewers: [security, platform]
version: 2.1.0
last_reviewed: 2026-07-30
review_interval: 90d
source_of_truth_for: [checkout-boundaries, checkout-data-flow]
depends_on: [prd-checkout, adr-0042]
supersedes: arch-checkout@2.0.0
sensitivity: internal
agent_access: read
---
```

For a small project, owner, status, last_reviewed, and links are enough. Do not
add metadata that nobody verifies.

## How Agents Work with Documentation

### Before the task

1. Find the nearest `AGENTS.md`/runtime instructions.
2. Read `docs/README.md` and the relevant domain index.
3. Identify canonical sources and check freshness.
4. Load only the necessary documents.
5. Report a document/code conflict rather than choosing silently.

### During the task

- refer to IDs and anchors rather than copying long fragments;
- record decisions in ADRs, not only in the conversation;
- update the spec together with any intentional behavior change;
- maintain evidence and traceability;
- do not edit generated files directly;
- follow document ownership and write-set constraints.

### After the task

- update documents affected by behavior or operations;
- run docs checks;
- mark superseded/archived materials;
- save evidence and the release/change note;
- verify links and the absence of stale statements;
- do not declare completion if the required documentation gate has not passed.

## Documentation and Code

Use bidirectional validation:

- **docs -> code**: requirements, interfaces, and ADRs are confirmed by the
  implementation;
- **code -> docs**: public interfaces, deployment, and runbooks reflect the
  current code.

GSD applies a doc verifier against the live codebase; OpenSpec recommends
proposal/spec review before code and coherence verification after
implementation; gstack generates Diataxis documents from shipped behavior. The
shared practice is that generation helps, but independent factual verification
is mandatory.

## Hierarchical Instructions

`AGENTS.md`, `CLAUDE.md`, and Cursor rules are not a replacement for `docs/`.
They are a compact operational index:

- repository map;
- build/test/verify commands;
- critical constraints;
- definition of done;
- links to detailed documents.

Instructions SHOULD be short and placed close to their scope of action. Codex
loads the chain from the global file to the current directory, with nearer rules
overriding general ones
([AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)).
Do not copy the same policy into every file: keep the canonical version and
links.

## Diagrams

For architecture, use the minimally useful C4 levels: system context and
containers are usually sufficient; component and code only where they add value
([C4](https://c4model.com/diagrams)). Each diagram must have:

- purpose and audience;
- scope and abstraction level;
- legend;
- labeled relationships;
- date/version;
- link to the source DSL;
- owner.

Do not mix different levels in one "map of boxes."

## Architectural Decisions

An ADR records one significant choice: context, decision drivers, considered
options, outcome, consequences, and how it will be confirmed. Use status
`proposed/accepted/rejected/superseded/deprecated`. MADR provides a compact
Markdown format ([MADR](https://adr.github.io/madr/)).

An agent MAY propose an ADR, but an accountable human or policy owner makes the
high-impact decision.

## Docs Quality Gates

- links and anchors are valid;
- required metadata is present;
- there are no unexplained TODOs/placeholders;
- code snippets execute or are validated;
- public API reference matches the schema;
- owner and freshness are defined;
- requirements have verification;
- diagrams render;
- glossary terms are used consistently;
- sensitive data is absent;
- generated outputs are reproducible.

## Anti-patterns

- a `docs/misc/` dumping ground with no index and owner;
- duplicating one requirement across PRD, spec, and plan without traceability;
- a huge `AGENTS.md` that tries to replace all documentation;
- auto-generated text without fact verification;
- storing live state only in the conversation;
- deleting an old decision instead of marking it `superseded`;
- a runbook that has never been executed;
- documenting internal details in a behavioral spec;
- updating docs as a separate late phase after release.
