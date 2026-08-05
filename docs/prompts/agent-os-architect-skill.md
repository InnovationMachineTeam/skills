# Master Prompt For The `agent-os-architect` Skill

Apply after [agent-os-base.md](agent-os-base.md). Create a skill that designs
Agentic OS boundaries, contracts, and a staged roadmap. It does not bootstrap
infrastructure and does not issue a release verdict.

Inventory users, teams, runtimes, hosts, trust zones, data classes, scale, SLO,
compliance, existing schedulers/registries/knowledge systems and operator
capacity. Compare build, extend and buy alternatives. Produce plane/component
map, control/data flows, canonical schemas, identities, policy points, state
ownership, protocols, deployment topology and ADRs.

Threat-model prompt injection, confused deputy, credential leakage, tenant
escape, supply-chain artifacts, replay/duplication, unbounded loops and
evaluator collusion. Failure-model provider/network/store outage, split brain,
stale desired state, partial side effect, poison memory and operator absence.

Return minimum walking skeleton, phased evolution triggers, measurable exit
gates, cost/operability estimate, evaluation strategy and rejected complexity.
Hand approved design to `agent-os-bootstrapper`.
