# Agentic OS Worked Examples

An Agentic OS is an operating layer for durable, governed work across agents or
teams. It is not a large prompt, a chat UI, or a synonym for an agent team.

## Minimum architecture

Every example below starts with one vertical slice:

```text
authenticated request
  -> policy decision and approval
  -> versioned registry resolution
  -> durable task and lease
  -> bounded agent/team execution
  -> artifact verification
  -> trace, cost, and terminal state
```

Use the platform skills in this order:

1. `agent-os-architect` compares build, extend, buy, and no-platform options.
2. `agent-os-bootstrapper` materializes only an approved staged slice.
3. `agent-os-evaluator` independently evaluates the frozen candidate.
4. `agent-policy-manager`, `agent-registry-manager`, and
   `agent-runtime-manager` govern their separate planes.
5. `agent-observer` defines and audits traces, SLOs, and incidents.

## Worked creation sequence

The same controlled sequence applies to every domain example:

1. **Assess:** ask `agent-os-architect` to compare one-agent, team, extend, buy,
   build, and no-platform alternatives. No files or infrastructure are created.
2. **Review architecture:** confirm the exact architecture ID, version, hash,
   vertical slice, plane owners, schemas, policies, SLOs, threats, costs, exit
   gates, rollback, and destination.
3. **Approve staging only:** authorize `agent-os-bootstrapper` to materialize the
   exact slice with synthetic data and credentials in a non-production target.
4. **Bootstrap:** produce reproducible definitions, schemas, registry seed,
   policy, durable task/run state, worker boundary, artifact verification,
   telemetry, and cleanup/rollback evidence.
5. **Freeze:** pin implementation/configuration hashes, model/tool/skill/prompt/
   policy versions, fixtures, thresholds, and environment.
6. **Evaluate independently:** run `agent-os-evaluator` across plane boundaries,
   authorization, registry drift, retries, cancellation, lease recovery,
   observability, security, cost, semantic outcome, and operator readiness.
7. **Resolve blockers:** create a new candidate rather than repairing the frozen
   evaluation target in place; re-run affected and regression cases.
8. **Approve rollout separately:** registration, activation, canary, scale-up,
   external publication, and production deployment each remain explicit state
   transitions with read-back and rollback.

Typical artifacts:

```text
docs/agent-os/<system>/architecture/
docs/agent-os/<system>/decisions/
docs/agent-os/<system>/schemas/
docs/agent-os/<system>/policies/
docs/agent-os/<system>/evals/
docs/agent-os/<system>/operations/
docs/agent-os/<system>/changes/
```

## Capability placement by example

| Example | Candidate shared/public capabilities | Candidate owner-private capabilities |
|---|---|---|
| Software delivery | ADR contract, requirement traceability, release evidence | framework coding, product-specific migration and design-system procedures |
| Learning production | source/citation, assessment quality, accessibility gates | course voice, case library, facilitator and LMS procedures |
| Research intelligence | provenance, contradiction handling, dated-briefing contract | client taxonomy, proprietary source intake, briefing style |
| Startup operations | assumption/experiment evidence and decision records | founder strategy, sales playbooks, investor/reporting templates |

These are candidates, not automatic public skills. Apply the placement gate,
register private and public assets, evaluate them independently, and publish
only when reuse and lifecycle ownership are proven.

## Example 1: multi-product software delivery OS

### When it is justified

Use this only when several Web, Mobile, or Desktop teams need shared queues,
policy, registries, model/tool governance, audit, release evidence, and recovery.
A single product team should normally use `agent-team-manager` without a
platform.

### Teams and capabilities

- intake and discovery team;
- product and requirements team;
- architecture and security team;
- implementation teams per product surface;
- quality and independent evaluation team;
- release and operations team;
- platform operator and human approval roles.

Public skills might include organization-wide ADR, requirements-traceability,
security-gate, and release-evidence contracts. Framework-specific coding
procedures used by one engineer-agent remain private until another consumer is
proven.

### Knowledge and documents

```text
docs/product/
docs/requirements/
docs/research/
docs/design/
docs/architecture/
docs/decisions/architecture/
docs/delivery/
docs/quality/
docs/operations/
docs/agents/
```

The registry pins teams, agents, skills, prompts, models, tools, policies, and
workflow versions. The runtime stores attempts, leases, checkpoints, artifacts,
and terminal states. Documents store human-reviewable intent and evidence.

### First walking skeleton

One approved feature request flows from intake to requirements, architecture,
one implementation workspace, tests, independent evaluation, a release
candidate, and a human release decision. It uses synthetic credentials and a
non-production target. Exit gates include successful cancellation, expired
lease recovery, denied unauthorized tool access, and deterministic rollback.

### Example request

```text
Use agent-os-architect to assess whether our Web, iOS, Android, and Desktop
delivery teams need a shared Agentic OS. Design only one non-production vertical
slice for an approved feature from intake through independent release evidence.
Compare no-platform, extend, buy, and build options. Include policy, registry,
runtime, knowledge, observability, security, cost, rollback, and human approval
contracts. Do not bootstrap until the architecture is approved.
```

## Example 2: learning-production OS

### When it is justified

Use this for a portfolio of courses, trainings, workshops, textbooks, and
localized editions with shared sources, rights, templates, assessment banks,
quality gates, instructors, and publishing channels. One course normally needs
only a team; one workshop may need one agent.

### Teams

- portfolio and audience research;
- learning architecture;
- subject-matter authoring;
- instructional design;
- assessment and psychometrics;
- media and accessibility production;
- instructor enablement;
- localization and publishing;
- independent quality evaluation.

### Platform services

- provenance-bearing source and claims store;
- learning-object registry with version and locale;
- rights and attribution policy;
- workflow state for draft, review, pilot, approved, published, retired;
- artifact pipeline for slides, workbooks, facilitator guides, LMS packages,
  print files, and assessment evidence;
- telemetry for completion, assessment validity, learner outcomes, and content
  freshness—without treating engagement alone as learning.

### First walking skeleton

One lesson travels from an approved learning objective through a source-backed
outline, lesson content, practice, assessment item, accessibility review, pilot
package, evaluator scorecard, and human publication approval.

### Example request

```text
Use agent-os-architect to design the minimum learning-production OS for a
portfolio of online courses and instructor-led trainings. The first slice is
one lesson and its slides, workbook exercise, facilitator notes, assessment,
citations, accessibility evidence, pilot feedback, and publication decision.
Keep rights, source provenance, evaluator independence, localization, and
rollback explicit. Design only; do not publish content.
```

## Example 3: research and trend-intelligence OS

### When it is justified

Use this when multiple research streams continuously collect sources, update
claims, compare trends, maintain watchlists, produce briefings, and require
freshness, provenance, contradiction handling, and reproducible retrieval.

### Teams and services

- research intake and question framing;
- source discovery and acquisition;
- evidence extraction and claim normalization;
- synthesis, scenarios, and implications;
- red-team and fact-checking;
- editorial delivery and stakeholder briefings;
- knowledge graph/vector index operators.

Canonical Markdown records remain reviewable. A graph database captures typed
relationships and a vector index supports semantic retrieval only after setup,
data classification, deletion, access, freshness, and rebuild contracts are
approved. GraphRAG is a projection, not automatically the source of truth.

### First walking skeleton

One research question produces a query plan, approved source set, extracted
claims with quotations and provenance, contradictions, synthesis, confidence,
trend implications, reviewer findings, and a dated briefing. Every answer can
trace back to its source and retrieval/index version.

### Example request

```text
Use agent-os-architect to design a trend-intelligence OS for weekly technology
and market briefings. The first slice must handle one question end to end with
source provenance, freshness, contradictory evidence, confidence, human review,
and reproducible retrieval. Compare Markdown-only, Obsidian/LLM Wiki, GraphRAG,
and Neo4j plus Qdrant options. Do not add databases without a measured need and
an approved operating model.
```

## Example 4: startup operating OS

### When it is justified

Use this only after a startup operates several persistent loops—customer
discovery, experiments, product delivery, marketing, sales, finance, and
investor reporting—and needs shared policies, metrics, evidence, and task state.
At idea stage, use one agent or a small Discovery Team.

### Loops

- opportunity and customer discovery;
- assumption and experiment management;
- product discovery and delivery;
- growth and campaign execution;
- pipeline and customer-success tracking;
- financial runway and scenario monitoring;
- governance, risk, and decision records.

### First walking skeleton

One strategic assumption becomes an evidence plan, approved customer research,
findings, an experiment, metrics, a decision, backlog change, and a business-
tracking update. Consent, PII, spending, external communication, and production
changes require external policy and human approval.

### Example request

```text
Use agent-os-architect to assess a shared operating system for our startup's
Discovery, Delivery, Marketing, Sales, and business-tracking loops. Start with
one assumption-to-decision slice. Define decision rights, data classifications,
budgets, approvals, registries, durable workflow state, evidence, telemetry,
recovery, and the criteria for staying with ordinary team workflows instead.
```

## Agentic OS release gates

- the no-platform alternative was evaluated honestly;
- the vertical slice proves a user outcome across all required planes;
- policy is enforced outside model prompts;
- desired registry state and observed runtime state are distinct;
- tasks use idempotency, leases, fencing, budgets, cancellation, and recovery;
- knowledge outputs carry provenance, freshness, and deletion rules;
- telemetry links task, run, agent, model, prompt, skill, tool, policy, cost, and
  artifact versions;
- evaluators are independent enough for the release risk;
- incident, rollback, and operator intervention paths are exercised;
- production rollout remains a separate human decision.
