# Build state and checkpoints

Use durable state for multi-phase, long-running, resumable, costly, or consequential workflows. Skip it for a one-response read-only specialist dispatch.

## Root contract

```json
{
  "schema_version": 1,
  "builder": "skill-builder",
  "build_id": "stable-id",
  "scenario": "full-lifecycle",
  "goal": "observable outcome",
  "status": "in_progress",
  "scope": ["exact target"],
  "acceptance_criteria": ["falsifiable criterion"],
  "authority": {
    "write": false,
    "external_research": false,
    "install": false,
    "publish": false,
    "retire": false
  },
  "phases": [],
  "artifacts": [],
  "approvals": [],
  "risks": [],
  "updated_at": "ISO-8601"
}
```

## Phase contract

Each phase contains `id`, `specialist`, `objective`, `status`, `dependencies`, `entry_conditions`, `required_outputs`, `exit_checks`, `authority`, and `evidence`. Use unique IDs and dependency references.

Phase statuses: `pending`, `in_progress`, `completed`, `rejected`, `inconclusive`, `waiting_approval`, `blocked`, `skipped`.

Root statuses: `planned`, `in_progress`, `waiting_approval`, `blocked`, `completed`, `aborted`.

## Checkpoint rules

- Update state after a phase result or authority decision, not after every narrative thought.
- Store locators and hashes for material artifacts.
- Never put secret values or hidden reasoning in state.
- Record approval subject, exact effect, scope, time, and whether it remains valid.
- Mark evidence stale when its input hash, revision, environment, or rubric changes materially.
- Do not set root `completed` while a required phase is pending, blocked, waiting, inconclusive, or rejected.
- Preserve rejected and skipped phases for auditability.

## Resume rules

Verify current targets before continuing. Do not repeat completed non-idempotent phases. When state conflicts with actual host state, preserve both observations, downgrade the claim to unknown, and route verification through the responsible specialist.
