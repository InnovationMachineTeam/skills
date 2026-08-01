---
name: agent-registry-manager
description: Governs typed desired-state registries and versioned bindings for Agentic OS agents, skills, commands, workflows, teams, tools, models and policies, and reconciles them with observed host/runtime state. Use for inventory, candidate registration, optimistic transactions, drift detection, quarantine, deprecation, migration or retirement at platform scope. Do not equate registered with trusted or active, bypass ownership/private visibility, edit generated views as canonical data, or mutate on a stale revision.
metadata:
  version: "1.0.1"
---

# Reconcile Agentic OS Registries

Treat the typed registry as desired inventory, bindings as relationships and
observed host/runtime state as separate evidence. Stable IDs do not depend on
paths. Record kind, SemVer/revision, hash, locator, provenance, trust,
compatibility, lifecycle, owner and replacement.

Read [references/reconciliation-contract.md](references/reconciliation-contract.md).
Inventory first. Unknown, stale, hash-drifted or unauthorized assets become
candidate/quarantined observations, never trusted or activated automatically.

Every mutation requires expected registry/binding revisions, authorization,
schema and reference checks, exact candidate diff, private-owner enforcement,
audit event, atomic application and rollback. Validate the plan:

```bash
python3 scripts/validate_reconcile_plan.py reconcile-plan.json
```

Reconcile desired and observed states as `IN_SYNC`, `MISSING`, `UNKNOWN`,
`DRIFTED`, `INCOMPATIBLE` or `QUARANTINED`. Generated Markdown/search/graph
views are projections. Test duplicate IDs, missing refs, cycles, stale writers,
partial transactions, private escape, deprecation and retirement.

Return revisions, classified drift, transaction/diff, audit evidence,
quarantines, rollback and verified lifecycle state. Registration is not trust,
installation or activation.
