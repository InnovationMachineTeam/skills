# Release 3.2.0: Individual-Agent Lifecycle Skills

Status: validated release candidate

## Scope

Adds ten selectively installable skills under `skills/agent-skills/`:
`agent-architect`, `agent-best-practices`, `agent-builder`, `agent-context`,
`agent-doctor`, `agent-evaluator`, `agent-manager`, `agent-optimizer`,
`agent-refactor` and `agent-scout`.

The release also adds an agent documentation contract, uses
`docs/decisions/architecture/` as the default ADR location for new projects,
and separates individual-agent routes from `agent-team-*` and `agent-os-*`.

## Compatibility

- Existing team and Agentic OS skills keep their identities and versions.
- Existing project docs conventions are preserved unless explicitly migrated.
- New dependencies use native Claude Code plugin dependencies and portable
  warnings/plans for Codex, Cursor and generic Agent Skills clients.
- `agentkit` is intentionally absent from the marketplace.

## Acceptance

- official and repository validators pass;
- deterministic script and fixture tests pass;
- routing and behavior eval datasets include positive, negative and collision
  cases;
- registry, catalog, dependency and generated plugin views have no drift;
- all entries remain selectively installable;
- maturity evidence is recorded before any later `agentkit` release.

## Validation evidence

- official `quick_validate.py`: PASS for all ten new bundles;
- repository portable structure: PASS, 38 skills;
- repository integrity: PASS, three marketplaces and 38 individual plugins;
- Python suite: PASS, 49 tests;
- deterministic negative controls verified invalid docs roots and incomplete
  evaluation acceptance as failures;
- independent fresh-context forward review: PASS after rejecting traversal,
  false-completion and ambiguous team-migration behavior in the first candidate;
- executable eval-fixture contract: PASS for all ten donors; bundled cases are
  public regression fixtures and protected holdout remains external;
- `agentkit` has no skill directory, catalog entry or generated plugin.
