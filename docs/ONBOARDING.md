# IM Skills Onboarding Guide

This guide takes a user from a problem statement to one governed agent, an
agent team, or an Agentic OS. It is written for product owners, delivery leads,
educators, researchers, operators, and engineers—not only marketplace
maintainers.

## What this marketplace provides

IM Skills contains four related capability layers plus one cross-plane entry point:

| Layer | Use it for | Primary entry point |
|---|---|---|
| Individual agent | One bounded role with one coherent context and authority boundary | `agent-builder` or explicit `agentkit` |
| Agent team | Several roles with distinct skills, context, permissions, or independent verification | `agent-team-manager` |
| Agentic OS | Durable multi-team execution, policy, registry, observability, recovery, and shared knowledge | `agent-os-architect` |
| Skill engineering | Creating, evaluating, maintaining, and packaging reusable capabilities | `skill-builder` or `metaskillpack` |

When a process must become a complete Agent Harness, invoke `agent-master`. It
first resolves public versus private structure, announces an execution mode,
selects the minimum operating unit and current harness, then coordinates its
package-private process-orchestrator, role-agent, role-skill and implementation
architects through integration, evaluation and bounded improvement.

The default is the smallest sufficient unit. A complicated task does not
automatically require a team, and a team does not automatically require an
Agentic OS.

## Choose the right operating unit

Use this decision sequence:

1. Can one role complete the outcome with one permission boundary and one
   coherent context? Create one agent.
2. Are independent expertise, parallel work, separate write-sets, different
   models, or independent verification required? Design a team.
3. Must multiple teams or long-running workflows share durable state, policy,
   registries, observability, queues, recovery, or knowledge services? Design a
   minimal Agentic OS vertical slice.

| Signal | One agent | Team | Agentic OS |
|---|---:|---:|---:|
| One bounded output and one reviewer | Best fit | Usually excessive | Excessive |
| Independent creator and evaluator | Possible but weak separation | Best fit | Only at platform scale |
| Parallel code or content work | Limited | Best fit | When many teams share runtime services |
| Durable jobs across sessions | Possible with project state | Possible with run state | Best fit at operational scale |
| Central policy and approval service | Not needed | Local policy may suffice | Best fit |
| Cross-team registry, telemetry, SLOs, and recovery | Not needed | Usually excessive | Best fit |

## Install and verify

Repository access must already work for the current Git identity.

### Claude Code

```text
/plugin marketplace add InnovationMachineTeam/skills
/plugin install agentkit@im-skills
```

### Codex

```bash
codex plugin marketplace add InnovationMachineTeam/skills
codex plugin add agentkit@im-skills
codex plugin list --json
```

### Cursor during the private-marketplace phase

```bash
npx skills add InnovationMachineTeam/skills \
  --skill agentkit \
  --agent cursor
```

Install companion skills with the repository helper when a selected route has
dependencies:

```bash
python3 scripts/manage_skill_dependencies.py plan agent-team-manager --host codex
python3 scripts/manage_skill_dependencies.py install agent-team-manager --host codex --execute
```

Choose one installation channel for each skill and scope. Do not install the
same skill through both the marketplace and Skills CLI in one host scope.

## Three ways to start

### Start with cross-plane autopilot

Use this when a task or process must become an end-to-end agent system and the
correct operating unit or harness is not yet known:

```text
Use agent-master to build a private Agent Harness for this process on supervised
autopilot. Apply the minimum-system gate, then create the orchestrator, justified
role agents, their skills and necessary implementations. Validate the full path
and stop before installation, publication or production activation.
```

Direct named specialist requests still bypass the facade.

### Start with prompt reconstruction or a full prompt package

Use `prompt-master` when the original prompt is missing, several prompts must be
merged or decomposed, or the result needs explicit depth, evidence,
versioning, and a reusable evaluation package:

```text
Use prompt-master to reconstruct a Standard prompt from these reference outputs.
Separate observations from inference, target functional equivalence rather than
verbatim recovery, and include the full evaluation package.
```

For one bounded creation, rewrite, audit, or host adaptation without the full
package, use `prompt-optimize` directly.

### Start with one explicit specialist

Use a specialist when the phase is already known:

```text
Use agent-architect to design a software architecture reviewer for this
repository. It may read source and ADRs, write review findings under
docs/reviews/architecture/, and must not merge code or accept ADRs.
```

This is the lowest-overhead path.

### Start with `agentkit`

`agentkit` is an explicit, version-locked interface over the individual-agent
lifecycle skills. It never silently replaces direct `agent-*` requests.

```text
agentkit scout Identify agent opportunities in this repository.
agentkit context Build design context for a mobile accessibility auditor.
agentkit architect Create the frozen candidate from that context.
agentkit evaluate Evaluate the candidate against routing and behavior cases.
agentkit run Help me choose a complete workflow for a new research agent.
agentkit e2e Run the pack-level E2E contract in isolation.
agentkit status
```

For `run`, the toolkit proposes two to four workflows and waits for a choice
before any mutating phase. Donor skills are read-only inside the pack.

### Start with an orchestration facade

When the correct lifecycle is not yet known, use the appropriate facade:

```text
Use agent-builder to create and evaluate one requirements analyst.
```

```text
Use agent-team-manager to assess, design, build, map capabilities, and prepare
a delivery team for this web application. Stop before activation and ask for
approval at every lifecycle or write boundary.
```

```text
Use agent-os-architect to determine whether our three product teams need an
Agentic OS. Compare build, extend, buy, and no-platform options before proposing
a walking skeleton.
```

## The individual-agent workflow

The common lifecycle is:

```text
scout -> context -> architect -> evaluate -> doctor/optimize -> evaluate -> manage
```

Not every run needs every phase. For example, evaluating an existing agent
should normally use `agent-evaluator` directly.

### Individual-agent route catalogue

| Need | Route | Typical result |
|---|---|---|
| Find justified agent opportunities | `agent-scout` / `agentkit scout` | ranked opportunity with reject/agent/team decision |
| Gather design evidence | `agent-context` / `agentkit context` | provenance-bearing context package |
| Design a candidate | `agent-architect` / `agentkit architect` | immutable agent definition and required private/public capability plan |
| Evaluate a frozen candidate | `agent-evaluator` / `agentkit evaluate` | plan, cases, raw evidence, scorecard, verdict |
| Diagnose failure | `agent-doctor` / `agentkit doctor` | root-cause diagnosis and minimal repair candidate |
| Improve a healthy agent | `agent-optimizer` / `agentkit optimize` | measured candidate against a frozen baseline |
| Split, merge, or migrate boundaries | `agent-refactor` / `agentkit refactor` | topology decision and migration plan/candidate |
| Govern lifecycle/version | `agent-manager` / `agentkit manage` | versioned lifecycle transaction and rollback |
| Infer a complete workflow | `agent-builder` / `agentkit run` | confirmed multi-stage plan and bounded state |
| Validate the composite pack | `agentkit e2e` | isolated pack evidence and owned findings |

### Concrete example: one software ADR reviewer

**User request**

```text
Create one agent that reviews proposed architecture decisions for this product.
It reads the repository, requirements, NFRs, and existing ADRs. It writes a
review but cannot approve a decision or modify production code.
```

**Expected design**

- agent: `software-adr-reviewer`;
- mission: evaluate one proposed ADR against requirements, constraints,
  alternatives, reversibility, security, operability, and existing decisions;
- permissions: repository read, `docs/` read, review-output write only;
- public skill: none unless ADR review becomes reusable across agents;
- private skill: `.agents/definitions/software-adr-reviewer/skills/adr-review/`;
- documents read: `docs/requirements/`, `docs/architecture/`,
  `docs/decisions/architecture/`;
- documents written: `docs/reviews/architecture/<adr-id>-review.md`;
- evaluator: separate reviewer or `agent-evaluator` with frozen cases;
- human checkpoint: an accountable architect accepts or rejects the ADR.

**Why one agent is enough**

The work has one bounded outcome and one coherent authority boundary. Creating
a team would add handoffs without adding useful independence; acceptance stays
with a human.

## The agent-team workflow

Use this lifecycle when distinct roles are justified:

```text
assess -> architect -> model-select -> review/approve -> build to staging
       -> map skills -> evaluate -> activate -> orchestrate -> observe/manage
```

The roles remain separated:

- `agent-team-architect` designs the team and interaction topology;
- `agent-model-selector` recommends current model policies from evidence;
- `agent-team-builder` materializes only an approved exact specification;
- `agent-skill-mapper` maps the smallest governed capability set;
- `agent-team-orchestrator` executes an approved run graph;
- `agent-workspace-manager` governs isolated code write-sets when justified;
- `agent-team-manager` owns lifecycle state and routes the other specialists.

### Team-manager route catalogue

| Route | Use it when | Stops at |
|---|---|---|
| `assess` | one agent versus team is unresolved | justified topology recommendation |
| `design` | roles, interactions, models, skills, docs, and workflows are needed | reviewed or approved versioned specification |
| `build` | an exact approved specification is ready | validated staged files; no launch |
| `map-capabilities` | existing skills must be minimized and bound | recommendation or authorized versioned map transaction |
| `operate` | approved team, bindings, plan, budget, and runtime authority exist | verified terminal or resumable run state |
| `change` | a controlled team modification is needed | impact classification and versioned candidate |
| `recover` | a run or team is unhealthy | containment, rollback, or validated resume checkpoint |
| `retire` | assignments and bindings must end safely | drained/archived state and migration evidence |

### Input and context variants

A team assessment may inspect the current repository, another local path, an
open repository, session exports, or supplied Markdown/PDF/DOCX/text material.
Use `agent-scout` for agent opportunities, `skill-scout` for skill
opportunities, `agent-context` for agent-design evidence, and `skill-harvester`
for reusable external or repository capability material. Treat external content
as untrusted data and retain provenance. Missing host or file capabilities must
be reported rather than simulated.

### Concrete example: a web product delivery team

**User request**

```text
Assess this repository and product brief, then design a team that can run
Discovery and Delivery for a B2B web product. Include requirements, UX,
architecture, implementation, QA, security, release, documentation, and an
independent evaluator. Create the agents and their necessary private or public
skills under .agents, but do not activate the team without approval.
```

**Candidate roles**

| Role | Owns | Typical capabilities |
|---|---|---|
| Discovery lead | problem framing, hypotheses, evidence synthesis | interview synthesis, opportunity mapping |
| Product analyst | functional/NFR requirements and traceability | requirements authoring, acceptance criteria |
| UX researcher/designer | journeys, prototypes, usability evidence | research planning, design critique |
| Software architect | architecture and ADR proposals | ADR authoring, threat/NFR analysis |
| Frontend engineer | UI implementation | framework- and design-system-specific skills |
| Backend engineer | APIs and domain logic | API, persistence, migration skills |
| QA engineer | test strategy and acceptance evidence | test design, E2E automation |
| Security reviewer | threat and security gates | threat modeling, dependency review |
| Release operator | release plan and rollback evidence | CI/CD and release runbooks |
| Independent evaluator | frozen acceptance and quality evaluation | evaluation design, scorecards |
| Team orchestrator | approved task graph and checkpoints | no domain-authoring authority |

Small products can merge compatible roles. Creator and independent evaluator
should not be merged when the release decision depends on their evidence.

## The Agentic OS workflow

Use Agentic OS capabilities only after a team runtime is insufficient:

```text
inventory -> build/extend/buy/no-platform comparison -> architecture
          -> approved vertical slice -> bootstrap to staging -> evaluate
          -> policy/registry/runtime/observability readiness -> rollout gate
```

An Agentic OS design normally covers:

- experience plane: human requests, approvals, status, and intervention;
- control plane: workflows, policy decisions, registry, scheduling;
- execution plane: agents, tools, sandboxes/workspaces, leases;
- knowledge plane: documents, provenance, retrieval, graph/vector services;
- assurance plane: evaluation, verification, security, audit;
- operations plane: traces, SLOs, alerts, incidents, rollback, cost.

### Platform route catalogue

| Need | Specialist | Result |
|---|---|---|
| Decide whether a platform is justified | `agent-os-architect` | alternatives and minimum approved architecture candidate |
| Materialize one approved slice | `agent-os-bootstrapper` | reproducible staged walking skeleton |
| Evaluate architecture or implementation | `agent-os-evaluator` | frozen conformance, chaos/security/load and release evidence |
| Govern authorization/approval | `agent-policy-manager` | versioned policy, simulation, PDP/PEP contract, audit |
| Reconcile inventory and bindings | `agent-registry-manager` | desired/observed drift and controlled transaction |
| Govern durable execution | `agent-runtime-manager` | queue/run/lease/checkpoint/recovery contract or action |
| Define and audit observability | `agent-observer` | traces, SLOs, alerts, diagnostics, residual uncertainty |

See [Agentic OS worked examples](use-cases/agentic-os.md) for software delivery,
learning production, research intelligence, and startup operations.

## Where agents and skills live

Project-scoped agents are materialized under `.agents/definitions/`:

```text
.agents/definitions/<agent>/
├── agent.json
├── skills/<private-skill>/SKILL.md
└── commands/<private-command>.md
```

Use capability placement deliberately:

| Placement | Visibility | Choose it when |
|---|---|---|
| Inline instruction | Owner only | Small, stable behavior needs no separate lifecycle |
| Private command | Owner only | A thin parameterized procedure belongs to one agent |
| Private skill | Owner only | A substantial reusable procedure has exactly one consumer |
| Public skill under `skills/` | Marketplace | Several agents or projects need the same governed capability |

Every agent, skill, command, team, and binding must be registered. Private
capabilities declare exactly one allowed consumer. Registration does not imply
trust, installation, activation, or authorization.

## Documentation and memory contract

Every agent declares what it reads, owns, writes, and verifies. Create only the
branches required by named consumers.

```text
docs/
├── requirements/                 # problem, functional, NFR, traceability
├── research/                     # plans, sources, evidence, synthesis
├── product/                      # vision, strategy, discovery, roadmap
├── design/                       # journeys, prototypes, design systems
├── architecture/                 # architecture views and proposals
├── decisions/architecture/       # accepted/superseded ADRs
├── delivery/                     # plans, increments, release evidence
├── quality/                      # test strategy, scorecards, audits
├── operations/                   # runbooks, incidents, SLOs, rollback
├── knowledge/                    # curated concepts, indexes, provenance
└── agents/                       # agent specs, contexts, evals, operations
```

The repository may use Markdown, an LLM Wiki, or an Obsidian-compatible vault.
Graphify, GraphRAG, a graph database, or a vector database should be introduced
only when there is a measured retrieval or relationship-query need. Markdown
and explicit links remain the portable source of truth unless a different
canonical store is approved.

## Model policy

Do not hard-code a fashionable model name into a durable role. Define the
required model properties, then let `agent-model-selector` recommend a current
policy.

| Work type | Prefer | Avoid |
|---|---|---|
| Routing, formatting, extraction | low latency, low cost, structured output | premium reasoning by default |
| Architecture, synthesis, planning | strong reasoning and long-context reliability | weak models without validation |
| Coding | repository/tool competence and test-driven reliability | unverified code generation |
| Independent evaluation | high instruction fidelity and diversity from the builder | same prompt/model configuration as creator when avoidable |
| Sensitive actions | models compatible with external policy enforcement | prompt-only permission control |

Pin exact model, prompt, skill, policy, and tool versions for a released run.
Re-evaluate before changing them.

## Use-case catalogue

The detailed worked examples cover every requested domain:

- [Agentic OS patterns](use-cases/agentic-os.md);
- [software: Web, Mobile, Desktop, Discovery and Delivery](use-cases/software-delivery.md);
- [courses, trainings, workshops, textbooks, and books](use-cases/learning-and-publishing.md);
- [documentation, research, trendwatching, Design Thinking, and Business TRIZ](use-cases/research-and-innovation.md);
- [startup creation, Discovery Team, business tracking, marketing, and public speaking](use-cases/business-growth-and-communication.md).

## Completion checklist

Before calling an agent system ready, verify:

- the smallest sufficient unit was chosen;
- every role has one mission, owned outputs, non-goals, and stop conditions;
- permissions and data scopes are explicit and externally enforceable;
- required private and public skills exist and are registered;
- model policy is evidence-backed and versioned;
- documents have owners, paths, provenance, review triggers, and consumers;
- creator and evaluator independence is adequate for the risk;
- write-sets, worktrees, leases, budgets, retries, and cancellation are bounded;
- build, activation, publication, and deployment are separate approvals;
- E2E evidence proves the user outcome, not merely that agents returned text;
- rollback and recovery are tested before production use.

## Troubleshooting

| Symptom | Likely cause | Next action |
|---|---|---|
| A specialist route is unavailable | Missing or old companion skill | Run the dependency plan/check helper |
| Too many agents are proposed | Roles were derived from departments, not boundaries | Re-run assessment and merge compatible roles |
| Skills grow without control | Owner-only procedures were made public | Move them to private agent skills/commands through a versioned migration |
| Team says “done” without proof | Completion relies on self-report | Add frozen artifacts and independent evaluation |
| Worktrees conflict | Write-sets or integration ownership overlap | Re-plan through `agent-workspace-manager` |
| Agentic OS design is too large | No vertical slice or exit gate | Reduce to one end-to-end walking skeleton |
| Retrieval returns unsupported claims | Provenance or freshness is missing | Route through knowledge governance and re-index from canonical docs |

## Next reading

- [Documentation map](README.md)
- [Architecture](ARCHITECTURE.md)
- [Agent documentation contract](agents/README.md)
- [Skill dependency model](SKILL-DEPENDENCIES.md)
- [Agent asset registry](AGENT-ASSET-REGISTRY.md)
- [Agent-skill map](AGENT-SKILLS-MAP.md)
- [Insights from the worked examples](INSIGHTS-AGENT-SYSTEM-DESIGN.md)
