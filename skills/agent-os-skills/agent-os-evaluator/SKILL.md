---
name: agent-os-evaluator
description: Independently evaluates frozen Agentic OS architecture, implementations and release evidence across plane boundaries, schemas, registry reconciliation, policy enforcement, durable execution, knowledge provenance, observability, operator readiness, security, failure recovery, lifecycle and end-to-end outcomes. Use for evaluation plans, conformance, chaos/security/load tests, release gates, comparisons or migration evidence. Do not repair the candidate during a frozen run, reveal holdouts, average away blockers, or authorize deployment.
metadata:
  version: "1.0.2"
---

# Evaluate a Frozen Agentic OS Candidate

Freeze candidate hash, configuration, fixtures, models/tools, thresholds and
environment before collecting evidence. Keep holdouts from builders and expose
producer/evaluator correlation.

Read [references/evaluation-contract.md](references/evaluation-contract.md).
Evaluate structural conformance, routing/semantic outcomes, security abuse,
repeated variance, chaos/failure, load/cost/latency, operator recovery and
lifecycle migration. Cover all six planes plus request-to-terminal E2E.

```bash
python3 scripts/validate_release_evidence.py release-evidence.json
```

Test duplicate tasks, split brain, provider/store/network outage, stale policy,
credential revocation, tenant escape, poison memory, cancellation/rollback and
disaster recovery. Preserve raw evidence and uncertainty. A blocking policy,
security, durability, provenance, recovery or operator defect cannot be offset
by aggregate score.

Return per-layer `PASS`, `FAIL`, `INCONCLUSIVE` or `WAIVED`, maximum severity,
blockers, raw evidence, uncertainty and release recommendation. Recommendation
is evidence for an accountable release owner, never deployment authority.
