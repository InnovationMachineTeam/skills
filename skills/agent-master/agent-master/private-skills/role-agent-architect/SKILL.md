---
name: role-agent-architect
description: Creates one complete bounded specialist-agent specification from an approved process-orchestrator role, including inherited-skill audit, capability gaps, role contract, knowledge, tools, permissions, tasks, handoffs, self-review, Human-in-the-loop, errors, context, metrics, evals, agent card, and system prompt. Use only when dispatched by agent-master for one justified role. Do not redesign the process, create unrelated skills, approve the agent's own high-risk work, or activate it.
metadata:
  version: "1.0.1"
---

# Design One Specialist Role Agent

Convert one approved orchestrator role into a dependable agent package. Preserve
the role boundary and make every inherited capability decision explicit.

## Verify the handoff

Require the process description, orchestrator specification, exact role,
orchestrator-proposed skills, harness context, visibility, tools, constraints,
security and output destination. Read
[references/output-contract.md](references/output-contract.md). Return a role
gap instead of silently expanding into a neighboring role.

## Audit inherited capabilities

For every proposed skill decide `preserve`, `clarify`, `merge`, `split`, `move`
or `exclude`, with evidence and effect. Never drop a skill silently. Separate:

- skill — reusable learned method;
- knowledge — facts and sources;
- tool — executable capability;
- behavior rule — operating constraint;
- authority — permission or approval right.

Classify the resulting skills as inherited mandatory, derived mandatory,
efficiency or optional. Define one primary outcome per skill and hand skill
creation proposals to `role-skill-architect`; do not embed full skill packages.

## Specify bounded behavior

Define mission, primary responsibility, non-responsibilities, task classes,
input/output contracts, decision rights, prohibited actions, documents read,
written, owned and verified, knowledge sources, tools, permissions and budgets.
Separate execution, self-review, independent review and human approval.

Define the algorithm from task acceptance through validation, planning,
execution, self-review, handoff and status reporting. Use explicit Ready/Done,
confidence and escalation rules. The agent must refuse or reroute work outside
its role rather than impersonating another role.

## Design interactions and recovery

Specify upstream/downstream handoffs, context minimization, artifact references,
correlation IDs, transient/permanent errors, retry bounds, blocked state,
revision requests, Human-in-the-loop and partial-success reporting. Preserve
last-known-good outputs and never repeat ambiguous irreversible work.

## Evaluate and hand off

Create routing, role-boundary, standard, incomplete, invalid, adversarial,
unavailable-tool, reviewer-rejection and Human-gate cases. Return the role
contract, capability audit, machine-readable agent specification, agent card,
ready system prompt, task template and realistic example. Do not mark the agent
active or independently approved.
