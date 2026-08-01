# Agent-master state contract

## Contents

- Root state
- Phase and component states
- Human gates
- Completion invariants

## Root state

Use schema version 2 with these required fields:

```json
{
  "schema_version": 2,
  "master": "agent-master",
  "run_id": "stable-id",
  "goal": "observable outcome",
  "status": "planned",
  "visibility": {
    "mode": "private",
    "selected_at": "ISO-8601",
    "selected_by": "user"
  },
  "execution_mode": "supervised",
  "scope": ["authorized target"],
  "acceptance_criteria": ["observable check"],
  "authority": {
    "write": true,
    "external_research": true,
    "install": false,
    "publish": false,
    "runtime_activate": false,
    "production": false,
    "destructive": false,
    "spend": false
  },
  "phases": [],
  "components": [],
  "artifacts": [],
  "decisions": [],
  "findings": [],
  "assumptions": [],
  "human_decisions": [],
  "risks": [],
  "updated_at": "ISO-8601"
}
```

## Phase and component states

Root statuses: `planned`, `in_progress`, `awaiting_human_decision`, `blocked`,
`completed`, `aborted`.

Phase statuses: `pending`, `in_progress`, `completed`, `rejected`,
`inconclusive`, `awaiting_human_decision`, `blocked`, `skipped`.

Component lifecycle:

```text
Proposed -> Researched -> Designed -> Implemented -> Testing -> Evaluated
-> Integrated -> Validated -> Stable -> Needs Improvement -> Deprecated -> Archived
```

Each phase records a unique ID, owner, objective, dependencies, entry
conditions, required outputs, exit checks, authority, retry count and evidence.
Each component records kind, owner, visibility, version, status, locator and
evidence. Package-private components allow only `agent-master` as consumer.

## Human gates

Each pending decision records an ID, operation, reason, affected resources,
proposed changes, risks, preview/dry-run result, alternatives, requested owner,
expiry when applicable and status. Root status must be
`awaiting_human_decision` while a blocking gate is open.

## Completion invariants

- Every non-skipped phase is completed.
- Every skip has a reason in its evidence.
- No blocking human decision remains open.
- No critical finding remains unresolved.
- Every `Stable` component has an owner, permissions, monitoring, documentation
  and applicable eval evidence.
- Publication, installation, activation and production claims have target-host
  read-back; otherwise their status remains false or not performed.
