# Operating Model and Pattern Selection

## Classify the task first

Selection does not begin with the number of agents. Evaluate eight axes:

| Axis | Low value | High value | Architectural implication |
|---|---|---|---|
| Uncertainty | Known algorithm | Path depends on evidence | Code/pipeline -> adaptive agent |
| Decomposability | Tight coupling | Independent parts | Single context -> fork-join |
| Side-effect risk | Read-only/reversible | External/irreversible | Autonomy -> approval/saga |
| Duration | Seconds | Hours/days | In-memory -> durable workflow |
| Cross-system scope | One runtime | Vendors/organizations | Local calls -> protocol/contracts |
| Required independence | Self-check is sufficient | Conflict/high stakes | Reflection -> independent verifier |
| Volatility | Stable facts/process | Dynamic environment | Snapshot -> retrieval/observe/reconcile |
| Scale | One run | Multi-tenant/high volume | Inline -> queues, quotas, SRE |

Also determine sensitivity, latency SLO, cost envelope, auditability, human
judgment, and blast radius.

## Selection ladder

```text
Can this be solved with deterministic code?
  yes -> code/tool + tests
  no  -> Is one bounded model call sufficient?
          yes -> structured generation + validation
          no  -> Is a stable sequence known?
                  yes -> workflow/pipeline
                  no  -> Are new observations and adaptation needed?
                          yes -> single agent with tools
                          no  -> reframe the problem

Do independent parts provide a proven gain?
  yes -> subagents/fork-join

Is peer coordination or split ownership needed?
  yes -> agent team

Are durable multi-tenant governance and operations needed?
  yes -> Agent OS platform patterns
```

Each transition requires eval evidence or a mandatory boundary reason:
different permissions, context isolation, ownership, concurrency, or protocol.

## Pattern recipes

### Research

```text
intent/questions
  -> router by independent topics
  -> read-only researchers (fork-join)
  -> evidence blackboard with provenance
  -> contradiction resolver
  -> synthesis
  -> source/claim verifier
```

Roles: intent owner, research planner, source specialists, synthesizer,
independent verifier. Cycle: Build-measure-learn for discovery; bounded
generate-evaluate for the report.

### Feature development

```text
intent/spec -> architect/planner -> DAG
-> worktree-per-write-set executors
-> integration owner -> automated tests/evals
-> independent verifier -> release gate -> canary -> observe
```

Roles: product/intent owner, architect, implementers, integration owner,
test/eval, security by risk, release owner, SRE. Cycle: ADLC + TDD/eval-driven;
PDCA improves the delivery process itself.

### High-risk automation

```text
map risk -> plan -> simulate/shadow -> evidence gate -> human approval
-> least-privilege execution -> postcondition -> canary/progressive
-> monitoring -> compensation/rollback
```

Add PDP/PEP, saga, immutable audit, and separation of duties. An agent cannot
expand its own envelope or treat silence as approval.

### Incident diagnosis

```text
detect -> triage/contain -> competing hypotheses
-> evidence blackboard -> falsification -> root-cause gate
-> scoped remediation -> recovery verification -> after-action review
```

OODA drives fast decisions; MAPE-K drives automated stabilizing controllers;
double-loop review checks flawed assumptions after the incident.

### Skill creation and evolution

```text
scout/duplication check -> context harvest -> skill architecture
-> atomic/composite build -> trigger + outcome evals -> security review
-> package/publish -> install/canary -> observe -> optimize/doctor
-> upgrade or deprecate/retire
```

Roles: sponsor, skill architect/author, source curator, eval designer,
security reviewer, publisher, marketplace owner, migration steward.

### Agent OS

```text
inventory/contracts -> registry -> hybrid control plane
-> sandboxed execution + durable state -> policy/evidence gates
-> telemetry/budgets -> reconciliation/incidents
-> versioned rollout -> lifecycle governance
```

Start with one workflow and shared primitives, not a universal platform. The
platform layer should be extracted after repeatable requirements appear.

## Organizational model

### Three ownership levels

1. **Asset ownership** - a specific agent, skill, workflow, tool, or dataset.
2. **Service ownership** - the end-to-end user journey and production SLO.
3. **Platform/governance ownership** - registry, runtime, policy, security, and
   portfolio lifecycle.

A locally successful agent may worsen the overall journey, so the service owner
owns the end-to-end outcome. The platform owner does not make product
decisions, but provides the paved road and guardrails.

### Federated governance

The central platform defines minimum controls, manifests, risk tiers, identity,
telemetry, and publication gates. Domain teams own capabilities, eval cases,
and on-call. Exceptions have an owner, rationale, expiry, and compensating
controls.

### Portfolio review

Periodically review the inventory:

- usage, success, safety, latency, and cost;
- duplicate/overlapping agents and skills;
- stale owners, dependencies, sources, and eval datasets;
- compatibility and unsupported runtimes;
- open incidents, exceptions, and technical debt;
- candidates for merge, split, deprecation, or retirement.

## Gates by risk tier

| Tier | Example | Before launch | During | After |
|---|---|---|---|---|
| R0 | Read-only draft | Basic validation | Budget | Sample review |
| R1 | Reversible local edit | Tests + scope | Checkpoints | Diff + verify |
| R2 | Shared repo/publish candidate | Independent eval + security | Approval at publish | Canary + audit |
| R3 | Production/data/money | Threat model + SoD + accountable approval | Strong PEP + live monitoring | Postcondition + rollback window |
| R4 | Safety/legal critical | Formal governance and domain authority | Human command, constrained automation | Independent audit and incident readiness |

The tier is determined by the maximum potential impact, not by model
confidence. A tier may be lowered only by approved control evidence.

## Metrics without metric gaming

Balanced set:

- outcome success and task completion;
- correctness/groundedness and severity-weighted failures;
- safety violations, denied/approved actions, and near misses;
- latency, queue time, handoffs, retries, and loop depth;
- token/tool/compute cost per successful outcome;
- human intervention, override, and escalation quality;
- rollback/recovery time and orphan rate;
- user/customer value and unintended impacts;
- lifecycle health: owner/source/eval freshness, deprecated dependents.

An aggregate score does not replace hard safety floors and subgroup analysis.
Bind telemetry to exact versions and intent class.

## Operating model documentation

Minimum set in `docs/`:

```text
docs/
  agents/          # contracts, cards, ownership, versions
  skills/          # capability map, trigger boundaries, donor manifests
  workflows/       # state/DAG definitions, checkpoints, recovery
  architecture/    # planes, contracts, ADRs, threat models
  operations/      # SLO, dashboards, runbooks, incidents
  assurance/       # eval plans, evidence, gates, known limitations
  governance/      # policies, risk tiers, approvals, exceptions
  lifecycle/       # inventory, deprecations, migrations, retirement
```

Each document has an owner, audience, source of truth, freshness trigger, and
consumer. Runtime state and generated evidence are not copied manually into
prose; the document links to the canonical store.

## Definition of ready and done

### Ready for a new agent/skill

- the need is proven and duplicates are checked;
- intent, users, non-goals, and risk tier are defined;
- the minimally sufficient mechanism is chosen;
- owner, verifier, operator, and retirement path are assigned;
- an eval plan, permissions, and a source/provenance plan exist.

### Done for a production capability

- the versioned contract and package are published;
- functional, negative-trigger, safety, and regression evals have passed;
- owner/SLO/telemetry/runbook/alerts are operational;
- policy, approvals, sandbox, and credentials are verified;
- rollback, deprecation, and retirement mechanisms are available;
- production observation confirms the outcome within the defined window.

## Maturity evolution

| Level | Characteristic | Next bottleneck |
|---|---|---|
| 0. Ad hoc | Prompt and manual result | Contract and reproducibility |
| 1. Repeatable | Skill/workflow, version control | Evals and ownership |
| 2. Controlled | Risk tiers, gates, independent verification | Runtime reliability |
| 3. Operated | SLO, traces, budgets, incidents | Portfolio and learning |
| 4. Adaptive | Canary, reconciliation, evidence-driven improvement | Governance of adaptation |
| 5. Federated | Paved road + domain ownership + lifecycle | Continuous simplification |

Maturity does not mean more agents. Higher maturity often removes unnecessary
agents, replaces stable steps with code, and reduces the number of routes.

## Final review checklist

- Which pattern addresses which force, and how is it measured?
- Who owns intent, state, side effects, verification, and residual risk?
- Where are the trust, security, and write boundaries?
- How are duplicates, timeouts, partial failure, and cancellation handled?
- Which cycle operates at the runtime, delivery, operations, and governance
  levels?
- When does the inner cycle escalate outward?
- Which roles must be independent for this risk tier?
- How is the run reproduced by versions, events, and artifacts?
- How is the capability updated, rolled back, deprecated, and retired?
- Can the same outcome be achieved with a simpler architecture?
