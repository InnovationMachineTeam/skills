# Agent team specification contract

The machine-readable spec contains:

```json
{
  "schema_version": 1,
  "id": "asset://project/team/delivery",
  "name": "delivery",
  "version": "1.0.0",
  "status": "candidate",
  "accountable_owner": "team-or-person",
  "goal": "observable outcome",
  "non_goals": [],
  "risk_tier": "R1",
  "roles": [
    {
      "id": "lead",
      "kind": "orchestrator",
      "mission": "own task and integration",
      "non_goals": [],
      "boundary_evidence": ["owns integration state"],
      "inputs": [],
      "outputs": [],
      "tools": [],
      "permissions": [],
      "data_classes": [],
      "model_policy_ref": "model-policy://project/delivery-lead@1.0.0",
      "write_set": [],
      "budgets": {"max_capabilities": 6},
      "stop_conditions": [],
      "escalation": [],
      "accountable_owner": "team-or-person"
    }
  ],
  "workflow": {
    "pattern": "manager",
    "stages": [
      {"id": "review", "role_ref": "lead", "depends_on": [], "artifact_outputs": []}
    ],
    "integration_owner_ref": "lead",
    "conflict_policy": "single writer",
    "cancellation": "checkpoint then stop",
    "partial_failure": "degrade or escalate"
  },
  "capability_placement": [],
  "model_policy_refs": [],
  "worktree_policy": "none",
  "human_checkpoints": [],
  "evaluation": ["representative end-to-end task"],
  "rollback": ["disable candidate team"],
  "retirement": ["verify no active runs or consumers"]
}
```

Role kinds: `orchestrator`, `specialist`, `integrator`, `verifier`, `curator`,
`operator`. Workflow patterns: `sequential`, `pipeline`, `fork-join`, `dag`,
`manager`, `handoff`, `blackboard`, `competing-hypotheses`.

Capability placement entries identify capability, decision, owner agent when
private, consumers and rationale. A candidate must not declare activation,
credentials or observed runtime state.

Version the spec by its behavioral contract: patch for documentation/evidence,
minor for compatible role/stage/capability additions, major for removed roles,
changed authority, schemas, topology or lifecycle behavior.
