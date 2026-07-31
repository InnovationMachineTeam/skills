# Agent Skills Portfolio Implementation Plan

Status: approved and in progress  
Owner: InnovationMachineTeam  
Reviewer: @stanislavus86

## Outcome

Create the individual-agent lifecycle portfolio under `skills/agent-skills/`
without duplicating the existing team and Agentic OS portfolios. Every skill is
selectively installable, versioned, registered, evaluated and documentation
aware. `agentkit` remains outside discovery until its now-passing donor maturity
gate is converted into a separately validated stable package.

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

Progress: release `3.2.2` completed stability cycle 2 of 2. The separate stable
`agentkit` promotion is in progress.

An experimental, non-discoverable `agentkit@0.2.0` candidate now provides the
`e2e` evidence-collection command. It is not a stable cycle, catalog entry or
published skill. Three real workflows and frozen upgrade, rollback and pack
holdout contracts now permit a separate exact promotion decision.

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
- `agentkit` is not published before two consecutive stable donor releases;
  that prerequisite now passes and does not itself authorize host activation.
