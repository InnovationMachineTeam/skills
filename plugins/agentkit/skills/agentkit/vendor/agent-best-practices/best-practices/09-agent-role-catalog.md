# Catalog of Standard Agent Roles

This file lists application specializations. Role archetypes, lifecycle
accountability, human oversight, and separation of duties are described in
[21-role-patterns-and-separation-of-duties.md](21-role-patterns-and-separation-of-duties.md).

## How to use the catalog

A role is not necessarily a separate agent. First define the capability and
security boundary. Combine roles if they share tools, context, and criteria;
separate them if independence, specialization, different rights, or parallelism
are required.

For each role, define the owner, inputs, outputs, write-set, tools,
permissions, evals, and escalation rules.

## PDLC and Discovery

| Agent | Responsibility | Primary outputs |
|---|---|---|
| Opportunity scout | Gathers signals, problems, and opportunities | opportunity backlog |
| Research planner | Formulates questions, method, and evidence criteria | research plan |
| Market researcher | Market, competitors, alternatives | cited market report |
| Domain researcher | Domain rules, failure modes, regulation | domain context |
| User researcher | Interviews/observations without substituting for a human | evidence synthesis |
| JTBD analyst | Jobs, pains, gains, alternatives | jobs map |
| Hypothesis/bet steward | Maintains the bet register and resolution signals | governed bets |
| Product strategist | Outcomes, positioning, non-goals | vision/strategy |
| Product manager | Scope, priorities, PRD/spec lifecycle | product requirements |
| UX researcher | Research questions, usability evidence | UX findings |
| UX/service designer | Journeys, states, service blueprint | experience design |
| Experiment designer | Experiment protocol and decision thresholds | experiment plan |

## Requirements engineering

| Agent | Responsibility | Independent gate |
|---|---|---|
| Requirements elicitor | Identifies stakeholders, needs, constraints | coverage review |
| Requirements analyst | Makes requirements atomic and testable | ambiguity lint |
| Functional analyst | Observable capabilities, rules, scenarios | acceptance review |
| Quality-attribute analyst | Performance, reliability, security, and more | measurable NFR gate |
| Constraint/compliance analyst | Legal, organizational, technical constraints | compliance owner |
| Traceability manager | Links intent→requirement→design→test→release | orphan detection |
| Requirements verifier | Checks completeness, consistency, feasibility | read-only verdict |

## SDLC / Architecture

| Agent | Responsibility | Outputs |
|---|---|---|
| Solution architect | Boundaries, integrations, trade-offs | architecture overview |
| Enterprise architect | Portfolio/platform alignment | capability map |
| Data architect | Data model, lineage, retention | data architecture |
| API/contract architect | Interfaces, versioning, compatibility | API contracts |
| Security architect | Threat model and control design | threats/controls |
| Reliability architect | SLO, failure domains, recovery | reliability plan |
| Privacy engineer | Data minimization, purpose, consent | privacy controls |
| Cost/FinOps analyst | Cost model and budgets | cost envelope |
| ADR steward | Decision quality and lifecycle | decision log |

## Implementation

| Agent | Responsibility | Constraint |
|---|---|---|
| Planner | DAG, slices, write-sets, verification | does not implement |
| Codebase mapper | Structure, patterns, dependencies | read-only |
| Implementer | One bounded deliverable | exclusive write-set |
| Refactoring agent | Behavior-preserving changes | characterization tests |
| Migration agent | Schema/data/code migration | rollback + dry-run |
| Integration agent | Connects independently built slices | merge owner |
| Test engineer | Automated tests based on the risk model | does not confirm its own code |
| Documentation agent | Updates documents to match shipped behavior | fact verification |

## Quality and assurance

| Agent | Focus |
|---|---|
| Plan reviewer | Goal achievability and coverage |
| Code reviewer | Correctness, maintainability, defects |
| Goal verifier | Outcome against spec, not tasks |
| Security reviewer | Threat mitigations and misuse cases |
| Performance reviewer | Budgets, bottlenecks, regressions |
| Accessibility reviewer | WCAG/user flows/assistive behavior |
| Test architect | Risk-based strategy and traceability |
| Eval designer | Dataset, rubrics, graders, thresholds |
| Adversarial tester | Prompt injection, tool misuse, edge cases |
| Compliance assessor | Evidence against control requirements |
| Release gatekeeper | Consolidates evidence and policy into go/no-go |

## Delivery and Operations

| Agent | Responsibility |
|---|---|
| Release orchestrator | Versions, changelog, checks, approvals |
| Deployment agent | Promotion/canary within the approved envelope |
| Canary observer | Production signals and rollback trigger |
| SRE/reliability agent | SLO, alerts, capacity, runbooks |
| Incident triage agent | Classification, evidence, safe routing |
| Incident commander assistant | Timeline and coordination; human remains accountable |
| Root-cause investigator | Hypotheses and evidence before a fix |
| Rollback/recovery agent | Verified reversible procedure |
| Cost monitor | Spend anomalies and budget enforcement |
| Documentation drift detector | Mismatch between docs/code/runtime |

## Agent OS and governance

| Agent | Responsibility |
|---|---|
| Intent router | Chooses a workflow/capability with confidence |
| Orchestrator | DAG, dispatch, integration, verification |
| Scheduler | Dependencies, leases, retries, backpressure |
| Policy agent/service | Explains policy; enforcement remains deterministic |
| Approval broker | Collects evidence for the accountable approver |
| Context builder | Builds the minimal grounded context pack |
| Memory curator | Verifies, classifies, and expires memory |
| Knowledge indexer | Indexes and provenance |
| Agent registry steward | Versions, compatibility, lifecycle |
| Agent evaluator | Offline/online evals and regression gates |
| Trace analyst | Finds loops, routing, and tool failures |
| Agent security monitor | Behavior, privilege, and injection signals |
| Workflow doctor | Diagnoses stuck/orphan/inconsistent runs |

## Team compositions

### Discovery pod

Research planner + market/domain/user researchers + product strategist +
skeptical evaluator. The product owner accepts the bet.

### Feature delivery pod

Requirements analyst + architect + planner + scoped implementers + test
engineer + verifier + documentation agent. The orchestrator does not write the
same files.

### High-risk change pod

Feature pod + security/privacy/reliability/migration specialists + independent
release gatekeeper + accountable human.

### Incident pod

Triage + competing-hypothesis investigators + SRE + recovery agent + timeline
scribe. The incident commander remains human for high-impact decisions.

### Agent improvement pod

Trace analyst + eval designer + prompt/tool engineer + security reviewer +
canary owner. A change does not pass the production gate without regression
evidence.

## Roles that must not be merged thoughtlessly

- implementer and sole verifier;
- policy author and sole policy approver;
- deployment agent and unconditional release approver;
- memory writer and sole fact verifier;
- incident fixer and sole root-cause investigator;
- requirements author and sole stakeholder proxy.

Separation of duties is especially important for money, personal data, security,
production, and compliance.
