# Agent Skills Portfolio Implementation Plan

Status: approved and in progress  
Owner: InnovationMachineTeam  
Reviewer: @stanislavus86

## Outcome

Create the individual-agent lifecycle portfolio under `skills/agent-skills/`
without duplicating the existing team and Agentic OS portfolios. Every skill is
selectively installable, versioned, registered, evaluated and documentation
aware. `agentkit` remains deferred until its donor maturity gate passes.

## Capability boundaries

- `agent-*` owns one agent or subagent definition and its lifecycle.
- `agent-team-*` owns team topology, team materialization and team runs.
- `agent-os-*` owns platform planes, runtime infrastructure and reconciliation.
- `agent-context` creates design-time context; `agent-knowledge-manager` owns
  durable curated project knowledge.
- `agent-builder` orchestrates specialists; it does not reimplement them.

## Phases

1. Documentation and schema foundation.
2. `agent-best-practices`, `agent-architect`, `agent-evaluator`.
3. `agent-doctor`, `agent-manager`, `agent-builder`.
4. `agent-scout`, `agent-context`, `agent-optimizer`, `agent-refactor`.
5. Registry, dependencies, marketplace generation and release validation.
6. Two stable donor release cycles, then a separate `agentkit` decision.

## Completion gates

- every bundle has `metadata.version`, precise positive and negative routing,
  and no empty resource directory;
- official and repository structural validation passes;
- routing, behavior, authority, failure, documentation and coexistence cases
  pass or are explicitly inconclusive;
- registry, catalog, plugin and dependency views agree on identity and version;
- individual install remains available on Claude Code, Codex and Cursor;
- generated agents declare documentation read/write roots, artifact ownership,
  decision paths, freshness and verification;
- `agentkit` is not published before two consecutive stable donor releases.
