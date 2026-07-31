# Model selection contract

## Decisions

- `RECOMMEND`: observed evidence clears all blocking gates.
- `CONDITIONAL`: fit depends on a named environment, limit or unresolved low-risk
  assumption.
- `RESEARCH_REQUIRED`: current authoritative facts or representative tests are
  missing.
- `INCONCLUSIVE`: available evidence cannot distinguish candidates reliably.
- `REJECT`: a blocking requirement is violated.

## Policy shape

```json
{
  "schema_version": 1,
  "policy_id": "model-policy://project/code-review-team",
  "version": "1.0.0",
  "checked_at": "2026-07-31T00:00:00Z",
  "target_hosts": ["codex"],
  "constraints": {
    "providers": [],
    "regions": [],
    "data_classes": [],
    "monthly_budget": null
  },
  "roles": [
    {
      "id": "reviewer",
      "risk_tier": "R1",
      "task_classes": ["code-review"],
      "requirements": ["tool-use", "structured-output"],
      "decision": "RECOMMEND",
      "preferred": "provider/model-id",
      "fallback": ["provider/model-id"],
      "escalate_when": ["confidence below threshold"],
      "stop_when": ["no approved model is available"],
      "evidence_refs": ["evidence://official/model-card"],
      "benchmark_refs": ["benchmark://review-suite/run-1"]
    }
  ],
  "sources": [
    {
      "id": "evidence://official/model-card",
      "url": "https://provider.example/model-card",
      "authority": "official",
      "checked_at": "2026-07-31T00:00:00Z",
      "claims": ["tool-use is supported"]
    }
  ],
  "re_evaluate_on": ["model deprecation", "host upgrade"],
  "next_review_at": "2026-10-31T00:00:00Z",
  "accountable_owner": "team-or-person"
}
```

Exact identifiers remain data, not normative examples. A `RECOMMEND` decision
requires at least one authoritative evidence reference and one benchmark
reference. Other decisions may omit benchmarks only when the reason is explicit
in their stop or escalation conditions.

## Versioning

- patch: evidence refresh without changed decisions;
- minor: backward-compatible candidate, fallback or threshold change;
- major: changed provider/data boundary, removed fallback, quality gate or role
  contract.
