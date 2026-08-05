# Role Patterns and Separation of Duties

## A role is not equal to an agent

A role is a set of responsibilities, authority, inputs, and verifiable outputs.
One person or agent may perform multiple roles in a low-risk process; one role
may be implemented by multiple agents. A separate agent is justified if
independent context, capability, a security boundary, parallelism, or a
different lifecycle owner is required.

For each role, record:

```yaml
role: independent-verifier
accountable_human: quality-owner
mission: confirm the outcome against the original intent
inputs: [intent_ref, artifact_ref, eval_plan_ref]
outputs: [typed_verdict, evidence_refs, gaps]
permissions: [read_artifacts, run_approved_evals]
forbidden: [edit_candidate, approve_exception]
escalates_when: [uncertain_high_impact, conflicting_evidence]
sla: 30m
```

NIST AI RMF requires documenting roles, communication lines, and human-AI
oversight throughout the lifecycle; executive leadership retains accountability
for AI risk decisions
([AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)).

## Basic role archetypes

### Sponsor / accountable owner

Defines value, risk appetite, and final accountability. May delegate work, but
not accountability. Accepts high-impact trade-offs, exceptions, and retirement
decisions.

### Intent owner

Defines the outcome, stakeholders, non-goals, constraints, and success
measures. Protects the process from local optimization of the wrong task. In
product work this is usually the product owner; in an incident, the incident
commander.

### Architect

Chooses boundaries, contracts, patterns, and quality trade-offs. Does not
dictate every execution step; records architecturally significant decisions and
consequences. Specializations: agent architect, workflow/orchestration
architect, skill architect, platform/Agent OS architect, security architect,
and data architect.

### Builder / executor

Creates a bounded deliverable within the assigned scope. Returns an artifact,
change log, tests, and evidence; does not declare the work finally accepted.

### Orchestrator / coordinator

Owns the task graph, dispatch, state, budgets, checkpoints, and synthesis. This
role is responsible for completing the process, but must not replace
independent domain, security, or approval roles.

### Verifier / evaluator

Checks outcomes, assumptions, and regressions against predefined criteria. A
verifier answers "is it proven?"; an evaluator answers "how good and how
robust?" For high risk they are read-only relative to the candidate and use
independent datasets or tools.

### Governor / approver

Applies policy and accepts residual risk. An approval broker may collect
evidence, but decision authority remains with the designated approver.
Approvals have scope, expiry, and revocation.

### Curator / steward

Maintains the quality of a long-lived asset: registry, memory, knowledge,
documentation, dataset, prompt/skill portfolio. Stewardship includes freshness,
provenance, duplication, compatibility, deprecation, and retirement.

### Operator / SRE

Owns SLO, capacity, telemetry, runbooks, recovery, and operational readiness.
This role does not have to be the agent author; production reality takes
priority over design assumptions.

### Observer / analyst

Turns traces, costs, incidents, and user outcomes into diagnostic evidence. It
does not automatically change active policy. Specializations: trace analyst,
FinOps, quality analyst, drift detector.

### Adversary / challenger

Looks for counterexamples, abuse paths, hidden assumptions, and correlated
failures. A red team does not make the final decision and does not receive
unnecessary production rights.

### Publisher / release manager

Checks package identity, version, provenance, changelog, compatibility,
signatures, gates, and promotion. The publisher is distinct from the registry
owner and the author.

### Incident roles

- commander - priorities, communication, and accountability;
- triage - severity and initial routing;
- investigator - competing hypotheses and evidence;
- containment/recovery operator - safe effectors;
- scribe - timeline and decisions;
- reviewer - post-incident learning and action tracking.

## Roles by system layer

### Agent

| Role | Responsibility |
|---|---|
| Agent product owner | Outcome, users, risk tier, lifecycle |
| Agent architect | Contract, tools, memory, autonomy, failure model |
| Prompt/context engineer | Instructions, context selection, grounding |
| Tool/integration engineer | Typed tools, adapters, errors, idempotency |
| Eval engineer | Datasets, rubrics, graders, regression gates |
| Agent security engineer | Threat model, permissions, injection controls |
| Agent operator | SLO, traces, budgets, incidents |
| Agent registry steward | Versions, compatibility, status, deprecation |

### Subagents and teams

| Role | Responsibility |
|---|---|
| Delegation designer | Task envelopes, context capsules, return schema |
| Team lead | Mission, assignments, conflict/escalation policy |
| Scheduler | Dependencies, leases, retries, backpressure |
| Specialist | Bounded domain deliverable |
| Integration owner | Contract fit, merge, end-to-end wiring |
| Communication moderator | Message schema, decision capture, loop prevention |
| Independent verifier | Outcome and cross-agent failure modes |

### Agent OS

| Role | Responsibility |
|---|---|
| Platform owner | Service strategy, roadmap, adoption, SLO |
| Runtime engineer | Scheduler, execution, checkpoints, recovery |
| Registry/capability steward | Identity, versions, discovery, revocation |
| Policy owner | Rules, risk tiers, approval matrix |
| IAM/security owner | Identities, credentials, sandbox, network policy |
| Knowledge/memory steward | Provenance, retention, retrieval, deletion |
| Observability owner | Telemetry schema, dashboards, alert quality |
| Reliability/SRE owner | Capacity, resilience, incident readiness |
| Cost/FinOps owner | Budget model, allocation, anomaly response |
| Protocol/integration owner | MCP/A2A/adapters and compatibility |
| Assurance owner | Evals, audit, release gates, evidence retention |

### Skills and marketplace

| Role | Responsibility |
|---|---|
| Skill sponsor | Need, audience, success, and retirement |
| Skill architect/author | Boundary, workflow, instructions, package |
| Trigger/eval designer | Discovery precision and outcome evaluation |
| Script maintainer | Deterministic core, portability, security |
| Source curator | Provenance, licenses, freshness, external intake |
| Skill reviewer | Structure, usability, conflicts, permissions |
| Publisher | Version, package, signatures, release evidence |
| Marketplace owner | Taxonomy, entries, policy, availability |
| Consumer/migration steward | Compatibility, adoption, upgrade/deprecation |

## Lifecycle accountability

| Lifecycle phase | Responsible roles | Accountable role | Independent input/gate |
|---|---|---|---|
| Discover need | Scout/researcher, domain expert | Intent owner | Duplication/value review |
| Design | Architect, security, evaluator | Asset owner | ADR/threat/eval review |
| Build | Author, tool/context engineers | Delivery owner | Automated checks |
| Validate | Verifier, eval, red team | Assurance owner | Independent evidence |
| Approve/publish | Release manager, publisher | Risk/release owner | Policy + provenance gate |
| Operate | SRE, observer, support | Service owner | SLO and incident signals |
| Improve/upgrade | Owner, analyst, maintainer | Asset owner | Regression + migration gate |
| Deprecate | Steward, migration owner | Portfolio owner | Dependency inventory |
| Retire | Registry/IAM/data stewards | Accountable owner | Revocation + archive proof |

## Separation of duties

### Mandatory separations for high risk

- the author is not the sole verifier;
- the policy author is not the sole exception approver;
- the deployer is not the unconditional release approver;
- the registry publisher is not the sole supply-chain/security reviewer;
- the memory writer is not the sole fact/provenance verifier;
- the eval author cannot choose only favorable production samples;
- the incident fixer does not close root cause without independent evidence
  review;
- an agent requesting expanded rights does not grant them to itself;
- a cost optimizer cannot unilaterally lower the safety/quality floor;
- retirement is executed separately from the decision that the asset is no
  longer needed.

### Temporal separation for a small team

If staffing is limited, one person MAY wear several roles, but separate phases:

1. Record the rubric and risk policy before implementation.
2. Start a new review context after implementation.
3. Use independent automated checks and immutable evidence.
4. For irreversible/high-impact action, obtain a second approver.
5. Record role switching in the audit record.

An LLM with a different prompt but the same context and data is weak
independence. Stronger independence comes from data, tools, model/runtime, and
organizational accountability.

## Human oversight patterns

| Pattern | Human role | Application |
|---|---|---|
| Human-in-the-loop | Approves before action | Money, publish, production, personal data |
| Human-on-the-loop | Observes and can stop | Reversible bounded automation |
| Human-over-the-loop | Sets policy, audits, and risk envelope | High-volume low-risk runs |
| Human-out-of-the-loop | Does not participate in the run | Only proven low-risk, reversible scope |

The oversight interface shows intent, proposed action, affected resources,
evidence, uncertainty, alternatives, reversibility, and deadline. An "approve"
button without this data creates automation bias.

## Role anti-patterns

- **Super-agent owner** - one agent sets the goal, executes, verifies, and
  approves.
- **Responsibility without authority** - a role owns the SLO but cannot stop a
  route/release.
- **Authority without evidence** - the approver sees only a summary.
- **Orchestrator as universal expert** - the coordinator replaces specialists.
- **Invisible steward** - a long-lived registry/memory/dataset has no owner.
- **Shared accountability** - "the team is responsible," but nobody decides.
- **Permanent temporary role** - an incident or migration owner never sunsets.
- **Agent anthropomorphism** - persona is treated as proof of competence.
- **Reviewer writes the answer** - the verdict is mixed with remediation and
  loses independence.

## Minimal role assignment matrix

Use DACI/RACI only as an accountability map, not as a workflow substitute.

| Asset | Driver/Responsible | Approver/Accountable | Contributors | Informed |
|---|---|---|---|---|
| Agent contract | Agent architect | Agent owner | Security, eval, domain | Operator |
| Skill release | Skill author | Publisher/portfolio owner | Reviewer, eval, security | Consumers |
| Workflow version | Orchestration engineer | Service owner | Runtime, policy, SRE | Teams |
| Policy change | Policy owner | Risk owner | Legal, security, operations | Affected owners |
| Memory corpus | Memory curator | Knowledge owner | Domain, privacy, security | Agents/users |
| Production promotion | Release manager | Release/risk owner | Eval, SRE, security | Support/users |
| Retirement | Migration steward | Portfolio owner | Registry, IAM, data, SRE | Dependents |

The matrix is stored next to the inventory and reviewed whenever the risk tier,
owner, tool permissions, audience, or deployment context changes.
