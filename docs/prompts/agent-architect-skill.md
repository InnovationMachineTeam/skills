# Master Prompt For The `agent-architect` Skill

Apply after [agent-skill-base.md](agent-skill-base.md). Create a skill that
classifies the need, chooses the minimal agent pattern, and creates a
reviewable immutable agent-system candidate. It does not activate a runtime
agent and does not issue a release verdict.

## Architecture routes

Classify the target as one primary route:

- single bounded agent;
- tool-using or retrieval-grounded agent;
- planner–executor;
- bounded subagent definition;
- single-agent tool-using, retrieval, planner-executor or verifier pattern;
- redesign existing agent definition.

Send team topology to `agent-team-architect`, and platform/Agent OS
architecture to `agent-os-architect`. Do not duplicate their contracts.

If code, a model call, or a deterministic workflow is sufficient, return the
simpler solution. Do not create a separate agent only for a persona, a nice
name, or a single role without a separate state/tools/permissions boundary.

After the role/capability graph, run
[agent-capability-placement.md](agent-capability-placement.md) for each new
capability. Do not create a public skill if the capability is needed by only
one agent and can live inline, as a private command, or as a private skill. In
the agent definition, record private roots, commands, and allowed capability
refs; do not expand global
discovery.

## Pattern selection

Assess uncertainty, coupling, parallelism, duration, side effects, reversibility,
independence, scale, and cross-boundary protocols. Choose patterns and explicitly record
forces/consequences:

- ReAct or plan-execute;
- router, manager-as-tools, or handoff;
- pipeline, state machine, DAG, or dynamic orchestrator;
- fork–join, blackboard, competing hypotheses;
- evaluator–optimizer, independent verifier, human checkpoint;
- saga, idempotency, lease, circuit breaker, bulkhead, reconciliation;
- shadow/canary and policy PDP/PEP.

Do not use the pattern catalogue as a checklist.

## Agent contract

Create the applicable artifacts:

- agent card and accountable ownership;
- mission, non-goals, user/stakeholder map;
- input/output/tool/handoff schemas;
- task envelope and context capsule;
- model/tool selection and fallback ladder;
- permissions, identities, data/network/secret policy;
- state/memory ownership, provenance, TTL, and deletion;
- runtime cycle, budgets, stop conditions, and escalation;
- human-in/on/over-the-loop model;
- failure model, retries, compensation, and recovery;
- telemetry/SLO/runbook requirements;
- evaluation contract and release thresholds;
- public/private skill bindings, private commands, and registry/map references;
- version, compatibility, migration, and retirement.

For a team, add a mission charter, lead, write-sets, shared artifacts,
communication schema, task/lease ownership, merge/integration owner, and conflict
resolution. For Agent OS, separate control, execution, knowledge, assurance, and
operations planes.

## Decision records

Record alternatives, decision drivers, the chosen pattern, rejected options,
risks, consequences, and confirmation evidence. Do not turn the generated plan
into authority: runtime/policy validates capabilities and side effects.

## Documentation contract

Apply [agent-documentation-contract.md](agent-documentation-contract.md).
Determine documents from the agent's mission and risk. For a software architect,
this usually requires an architecture overview and ADRs in
`docs/decisions/architecture/`; acceptance of a high-impact ADR remains with the
accountable human/policy owner. Choose inline, private command, private skill,
or public skill for documentation capability.

## Evaluation design

Before finalizing the candidate, define claims and cases for:

- mission/outcome;
- routing and scope exclusions;
- tool success/denial/failure;
- delegation, partial failure, and conflicting result;
- loop termination and budgets;
- memory/state resume and poisoning;
- human approval and an unavailable approver;
- adversarial inputs;
- observability/recovery;
- compatibility, rollout, and retirement.

## Output and handoff

Return the versioned candidate bundle, diagrams only where they clarify
boundaries, the decision record, threat model, eval plan, and unresolved risks.
Hand the candidate to `agent-evaluator`. Do not repair evaluation results
within the same revision.
