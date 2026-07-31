---
name: agent-os-architect
description: Designs the minimum justified Agentic OS across experience, control, execution, knowledge, assurance and operations planes, including desired versus observed state, identities, schemas, policy points, protocols, SLOs, threat and failure models, deployment topology and staged evolution. Use when a team runtime is no longer sufficient and a user needs a platform architecture, build/extend/buy comparison, bounded walking skeleton or Agentic OS ADR. Design only; do not bootstrap infrastructure, operate runs, change registries or policies, or issue release verdicts.
metadata:
  version: "1.0.0"
---

# Architect a Minimal Agentic OS

Reject platform construction when one workflow or agent team can meet the
outcome. Require a bounded use case, scale/reliability evidence, operators and
measurable exit gates before introducing Agentic OS.

## Inventory and compare

Inventory users, teams, hosts, trust zones, data classes, load, SLO/compliance,
existing registries, schedulers, policy, knowledge and telemetry, plus operator
capacity. Compare build, extend and buy against cost, portability and recovery.

Read [references/architecture-contract.md](references/architecture-contract.md).
Separate six planes: experience, control, execution, knowledge, assurance and
operations. For each declare API/schema, owner, source of truth, permissions,
SLO, threat/failure model and lifecycle. Model desired versus observed state and
reconciliation; LLM output remains an untrusted proposal.

## Design the vertical slice

Define stable/versioned identities for agents, skills, workflows, models,
policies and runs; PDP/PEP and scoped credentials; durable idempotent execution;
provenance; telemetry; evaluation and recovery. Threat-model injection,
confused deputy, credential leakage, tenant escape, replay, supply chain,
unbounded loops and evaluator collusion. Failure-model store/provider/network
outage, split brain, stale desired state, partial effects, poison memory and
operator absence.

Choose one request-to-terminal-state flow. Reject databases, service mesh,
GraphRAG or dynamic routing not required by measured exit criteria.

Validate the design candidate:

```bash
python3 scripts/validate_architecture.py agent-os-architecture.json
```

Return `JUSTIFIED`, `SIMPLER_WORKFLOW`, `RESEARCH_REQUIRED` or `REJECT` with
plane map, contracts, ADRs, walking skeleton, stages, costs, evals, rollback,
retirement and handoff to `agent-os-bootstrapper`. A design is not deployment.
