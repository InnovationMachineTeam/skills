# Software Discovery and Delivery

This blueprint covers Web, Mobile, and Desktop products across the full product
and software lifecycle.

## One agent or a team?

Use one agent for a bounded activity such as ADR review, requirements quality,
accessibility review, test-plan review, release-note drafting, or documentation
maintenance. Use a team when research, product, design, architecture,
implementation, independent quality, and release responsibilities must interact.

## Shared lifecycle

```text
strategy -> discovery -> requirements -> solution design -> delivery planning
         -> implementation -> verification -> release -> operate -> learn
```

Each phase has explicit entry evidence, outputs, review, and exit criteria.
Discovery and Delivery share decisions and traceability instead of handing off
unstructured summaries.

## Worked team-creation sequence

1. `agent-team-manager assess` inventories the brief, repository, documents,
   data, existing agents/skills, constraints, and current lifecycle state.
2. `agent-team-architect` builds outcome, artifact, capability, dependency,
   authority, risk, and write-set graphs before naming roles.
3. `agent-model-selector` recommends current policies for routing, research,
   reasoning, coding, and independent evaluation.
4. The team spec declares roles, interactions, skills, documents, workflows,
   worktree policy, budgets, stop conditions, human checkpoints, and E2E gates.
5. After exact approval, `agent-team-builder` creates staged `.agents`
   definitions, private skills/commands, public-skill candidates, adapters, and
   registry/map transaction candidates.
6. `agent-skill-mapper` removes excessive capabilities and prepares authorized
   bindings; every asset is registered with visibility and ownership.
7. Frozen team cases test routing, handoffs, partial failure, security,
   cancellation, integration, artifact quality, and outcome completion.
8. Activation and the first orchestrated run require separate approval. Code
   worktrees are allocated only for independent bounded write-sets.

## Core team and skills

| Role | Main outputs | Example owner-private skills |
|---|---|---|
| Product/discovery lead | opportunity brief, hypotheses, decisions | opportunity-mapping, experiment-design |
| UX researcher | research plan, evidence, insights | interview-protocol, usability-analysis |
| Product analyst | functional requirements, NFRs, traceability | requirement-quality, acceptance-criteria |
| UX/UI designer | journeys, flows, prototypes, UI specs | design-critique, accessibility-design |
| Software architect | architecture views, ADR proposals | adr-authoring, nfr-tradeoff-analysis |
| Engineer(s) | reviewed increments and tests | stack-specific implementation procedures |
| QA engineer | risk-based strategy, automation, evidence | test-design, exploratory-testing |
| Security reviewer | threat model and security findings | threat-modeling, secure-review |
| Release/operations owner | release plan, rollback, runbooks | release-readiness, incident-handoff |
| Independent evaluator | frozen scorecard and verdict | product-quality-evaluation |
| Orchestrator | approved task graph and checkpoints | no authority to redefine product scope |

Promote a private skill to public only when multiple agents or projects require
the same stable contract.

## Documentation layout

```text
docs/
├── product/vision.md
├── product/strategy.md
├── product/roadmap.md
├── research/plans/
├── research/evidence/
├── research/insights/
├── requirements/functional/
├── requirements/non-functional/
├── requirements/traceability/
├── design/journeys/
├── design/prototypes/
├── design/system/
├── architecture/views/
├── decisions/architecture/
├── delivery/plans/
├── quality/strategies/
├── quality/evidence/
├── operations/runbooks/
└── operations/incidents/
```

## Web product example

**Scope:** a B2B SaaS onboarding flow.

**Specialized roles and skills:** frontend engineer with private design-system
and browser-testing skills; backend engineer with private API/domain/migration
skills; accessibility reviewer; security reviewer for identity and tenant
isolation.

**Workflow:** discovery interviews -> opportunity decision -> journey and
prototype -> functional/NFR requirements -> ADRs -> vertical slice -> contract,
component, E2E, accessibility, security, and performance evidence -> staged
release -> human release approval.

**Example request**

```text
Use agent-team-manager to assess and design a Web delivery team for the B2B
onboarding flow in this repository. Cover Discovery and Delivery, create the
minimum roles and their necessary public or owner-private skills, define docs
under product/research/requirements/design/architecture/quality/operations,
and include an independent release evaluator. Stage files only after the team
spec is approved; do not deploy.
```

## Mobile product example

**Scope:** an iOS and Android field-service application with intermittent
connectivity.

**Additional boundaries:** platform engineers may share product contracts but
need separate platform skills and workspaces. Mobile architecture must cover
offline-first data, synchronization conflicts, secure local storage, battery,
network variability, accessibility, device/OS matrix, store policy, signing,
privacy, analytics, and phased rollout.

**Artifacts:** device matrix, offline/sync ADRs, mobile threat model, analytics
taxonomy, test matrix, beta plan, store assets/checklists, crash/ANR SLOs,
rollback/kill-switch plan.

**Example request**

```text
Use agent-team-manager to design a cross-platform mobile product team for an
offline-first field-service app. Decide whether iOS and Android require separate
engineer agents and worktrees. Create private platform skills where appropriate,
shared public skills only when there are multiple consumers, and require
independent device, accessibility, privacy, security, and release evaluation.
```

## Desktop product example

**Scope:** a Windows and macOS document-processing application.

**Additional boundaries:** desktop platform/integration engineer, packaging and
update specialist, security reviewer for local file access and IPC, QA owner for
OS/version/hardware matrices.

**Artifacts:** filesystem and sandbox threat model, IPC/update ADRs, installer
and signing runbooks, migration and backup tests, crash recovery evidence,
accessibility checks, distribution-channel release plan.

**Example request**

```text
Use agent-team-manager to assess a Desktop team for Windows and macOS. Cover
local files, IPC, updates, signing, installers, migration, crash recovery,
accessibility, telemetry, and support documentation. Keep release credentials
outside agents and require explicit approval before signing or publishing.
```

## Discovery-only team

Create a smaller Discovery Team when no implementation is authorized:

- discovery lead;
- customer/UX researcher;
- product analyst;
- prototype designer;
- technical feasibility advisor;
- evidence challenger/evaluator;
- human product decision owner.

It produces an opportunity brief, assumptions, evidence plan, research,
prototype, feasibility/NFR risks, experiment results, and a proceed/pivot/stop
decision. It does not create production code or silently turn findings into a
delivery commitment.

## Delivery gates

- requirements trace to evidence, design, implementation, and tests;
- NFRs are measurable rather than adjectives;
- ADR acceptance remains with an accountable decision owner;
- code writers have non-overlapping write-sets or governed workspaces;
- evaluator cases and thresholds are frozen before candidate execution;
- security, privacy, accessibility, and operational readiness are explicit;
- release includes migration, monitoring, rollback, and support evidence;
- deployment remains separately authorized.
