# Agent Harness autopilot contract

## Contents

- Mode resolution
- Factory phases
- Harness decision
- Integration path
- Failure and improvement loop

## Mode resolution

Visibility is the first and separate decision:

| Mode | Default placement |
|---|---|
| `public` | Independent orchestrators, agents, skills, tools, versions and evals |
| `private` | One orchestrator-owned package; promote only independently valuable components |

Execution mode controls collaboration, not safety:

| Mode | Product questions | Mutations | Mandatory gates |
|---|---|---|---|
| `advisory` | Only material | None | All effects remain proposals |
| `assisted` | Material and mutation choices | After approval | Every mutation boundary |
| `supervised` | Material only | Authorized low-risk work | Architecture, risk and external effects |
| `autonomous` | Only blockers | Authorized low-risk work | Same safety gates as supervised |
| `review-only` | Only scope/evidence gaps | None | No repair by implication |

Announce both modes. If execution mode is absent, use `supervised`. If an
explicit mode conflicts with the rest of the request, ask one discriminating
question. A mid-run mode change applies from the next phase and never replays a
consequential completed action.

## Factory phases

```text
visibility -> intake -> worth/minimum-unit -> current research -> harness ADR
-> harness architecture -> process orchestrator -> role agents -> role skills
-> tools/automations -> integration/evals -> bounded improvement -> handoff
```

Each phase declares entry conditions, outputs, exit checks, authority and
dependencies. Keep authoring, independent evaluation, human approval,
publication, activation and operation as separate transitions.

The four package-private subskills own the transformations after harness design:

| Phase | Private owner | Primary output |
|---|---|---|
| Process | `process-orchestrator-architect` | Executable process and orchestrator specification |
| Roles | `role-agent-architect` | One bounded role-agent package |
| Capabilities | `role-skill-architect` | One researched, tested skill package |
| Implementation | `skill-implementation-engineer` | Necessary code, tools, hooks and automations |

## Harness decision

Research current official documentation before selecting a harness or framework.
Compare at least orchestration model, agents, durable state, pause/resume,
Human-in-the-loop, tools, modular skills, observability, evals, retry/checkpoint,
local and distributed operation, sandbox/permissions/secrets, privacy,
extensibility, provider portability, cost, maturity and lock-in.

Return `ADOPT`, `ADAPT`, `BUILD_MINIMAL` or `NO_HARNESS`, plus one fallback.
Implement only the planes justified by named requirements; a plane may be a
module rather than a service.

## Integration path

Verify the full path with raw evidence:

```text
User request -> agent-master -> process orchestrator -> role agent -> role skill
-> tool/script when needed -> role self-review -> orchestrator review
-> human gate when required -> final artifact -> monitoring -> documentation
```

Required evidence includes routing, contracts, permissions, registrations,
versions, artifact integrity, failure recovery, resume, Human-in-the-loop,
security, monitoring and a clean-install or equivalent isolated bootstrap test.

## Failure and improvement loop

- Classify failures as validation, permission, dependency, timeout, conflict,
  security, internal or external.
- Retry only transient, idempotent work and bound the retry count to one by
  default.
- Never repeat an irreversible operation after an ambiguous result.
- Record partial success and preserve the last-known-good artifact.
- After the first working version, separate fact, observation, inference,
  hypothesis and recommendation.
- Fix authorized critical/major findings, rerun affected gates, and stop when
  Definition of Done is met or further value requires an owner decision.
