# Insights from Agent-System Use Cases

This file records cross-domain findings discovered while turning the marketplace
capabilities into concrete onboarding examples.

## 1. Scale follows boundaries, not task size

A large artifact can still belong to one agent when mission, context,
permissions, and review are coherent. A small task may need two agents when
independent evaluation or separate authority is essential.

## 2. Most uncontrolled skill growth is a placement problem

Many procedures are reusable only inside one role. Making them owner-private
skills or commands preserves modularity without polluting public discovery.
Promotion to public should require at least two justified consumers, a stable
contract, independent evaluation, ownership, and lifecycle support.

## 3. Documentation is part of the agent interface

An agent is not fully specified until its read roots, owned artifacts, write
paths, provenance rules, reviewers, consumers, and freshness triggers are known.
The documentation contract belongs in architecture and evaluation—not as an
afterthought after the agent is generated.

## 4. Domain teams repeat a small set of control roles

Across software, education, research, innovation, and marketing, the same
separation recurs:

- accountable outcome owner;
- evidence or source owner;
- creator/producer;
- independent evaluator/challenger;
- orchestrator/runtime controller;
- policy/approval owner;
- operator/maintainer.

Domain roles should be derived from real boundaries, not copied mechanically.

## 5. Artifact completeness is domain-specific

“Create a course,” “perform research,” or “launch a campaign” is not one output.
Each is an artifact system: learner and facilitator materials, evidence and
contradictions, or claims and measurement contracts. Team architecture should
start from this artifact graph before inventing agent names.

## 6. Agentic OS begins at durable shared services

The threshold is not agent count. Agentic OS becomes justified when workflows
need shared durable queues, registry reconciliation, external policy,
observability, knowledge governance, cross-team recovery, and operator SLOs.
Until then, a team manager and project documents are simpler and safer.

## 7. Engagement is not outcome evidence

Availability is not semantic quality, course completion is not learning,
campaign engagement is not business impact, and research volume is not insight.
Every domain needs outcome-specific evaluation and explicit guardrails.

## 8. Knowledge infrastructure should be demand-driven

Markdown plus explicit links is the most portable baseline. An Obsidian vault,
LLM Wiki, graph, vector store, or GraphRAG becomes useful only when a measured
retrieval, relationship, scale, or freshness problem justifies its setup and
operations. Derived indexes must retain provenance to canonical sources.

## 9. Model selection is a policy, not a role label

Different phases need different latency, cost, context, reasoning, tool, and
independence properties. Durable assets should define those properties and pin
evaluated versions per release rather than hard-code one vendor model forever.

## 10. The safest default is staged and reversible

Design, build, register, bind, activate, publish, and deploy are distinct state
transitions. Each transition needs authority, evidence, revision checks, and a
rollback path. This principle applies equally to code, content, research,
marketing, and operational automation.
