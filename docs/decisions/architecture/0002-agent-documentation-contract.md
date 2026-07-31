# ADR 0002: Agent documentation contract and decision layout

- Status: Accepted
- Date: 2026-07-31
- Owners: InnovationMachineTeam
- Reviewer: @stanislavus86

## Context

Agents need durable project context, but pre-creating every possible docs folder
produces empty taxonomy and stale files. Agent definitions also lacked an exact
contract for which documents they may read, write and own.

## Decision

1. Add a validated `documentation` section to agent definitions.
2. Require exact read/write roots, artifact contracts, index updates,
   freshness rules and validation where documentation is applicable.
3. Use `docs/decisions/architecture/` as the default ADR location for new
   projects without an existing convention.
4. Keep domain artifacts in their domain and agent lifecycle artifacts under
   `docs/agents/`.
5. Create directories only for required, owned artifacts.
6. Select inline, private or public documentation capabilities through the same
   placement gate as other agent capabilities.
7. Let agents propose consequential decisions; accountable humans or policy
   owners accept them.

## Consequences

- Agent architecture, build, evaluation and lifecycle gates include docs.
- Existing projects keep their convention unless migration is explicit.
- `docs/decisions/adr/` is not used because it classifies the record format
  rather than the decision subject.
