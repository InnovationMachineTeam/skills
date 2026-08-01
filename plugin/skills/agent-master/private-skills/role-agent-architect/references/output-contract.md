# Role-agent output contract

## Contents

- Role and capability audit
- Runtime contract
- Handoff and status models
- Evaluation and package outputs

## Role and capability audit

Return:

1. role mission, primary responsibility and explicit non-responsibilities;
2. original-skill audit with `preserve|clarify|merge|split|move|exclude`;
3. gap analysis and normalized skill matrix;
4. knowledge map with sources, freshness and prohibited data;
5. tools, permissions, side effects and approval gates;
6. task map linking tasks to skills, knowledge, tools and outputs.

Each skill entry records ID, name, class, primary outcome, triggers,
non-triggers, input, output, method, evidence, dependencies, tools, risk,
evaluation criteria, owner and proposed visibility.

## Runtime contract

Specify:

- input and output schemas;
- validation, acceptance and refusal rules;
- task algorithm and branching;
- Definition of Ready and Definition of Done;
- self-review checklist and confidence calculation;
- context inputs, retained state and discard rules;
- model/tool constraints when known;
- permissions, forbidden effects, secrets and data boundaries;
- operational logs, audit events, metrics and cost/usage fields.

The output must distinguish result, evidence, assumptions, warnings, open
issues, confidence, status and recommended next action.

## Handoff and status models

Use statuses where applicable:

```text
Ready -> Working -> Self-Review -> Completed
                 -> Needs Revision
                 -> Blocked
                 -> Awaiting Human Decision
                 -> Escalated
```

Each handoff records source/target role, task and process IDs, artifact refs,
summary, decisions, assumptions, open issues, validation performed, confidence,
required action, deadline and escalation path. Pass references instead of full
unbounded context.

Human review is mandatory for work beyond authority, low-confidence high-impact
outputs, legal or policy decisions, external publication, production changes,
destructive actions, credentials, permission elevation and confidential-data
egress.

## Evaluation and package outputs

Include at least:

- direct role task;
- neighboring out-of-role task;
- incomplete and invalid inputs;
- conflicting evidence;
- unavailable tool or dependency;
- reviewer rejection and revision;
- high-risk Human-in-the-loop;
- prompt/authority injection.

Return target-native files for the candidate agent, including a machine-readable
specification, system prompt, agent card, task template, skill proposals and
eval fixtures. List every change from the orchestrator proposal and its reason.
