---
name: agentkit
description: Explicit composite toolkit for the version-locked individual-agent lifecycle skills. Use only when the user invokes `$agentkit`, writes an `agentkit` command, asks for the agentkit command surface, or requests an agentkit E2E, upgrade, or status run. Route one explicit command to one read-only vendored donor, or use `run` for a confirmed multi-stage workflow. Do not trigger for ordinary agent design, evaluation, repair, optimization, team, Agentic OS, or direct `agent-*` requests; those belong to the corresponding specialist skills.
metadata:
  version: "0.1.0"
---

# Operate the Agentkit Candidate

Provide one explicit entry point over locked individual-agent donors without
reimplementing their workflows. This bundle is a non-discoverable candidate
until the maturity ledger permits promotion.

## Parse the command

Accept `agentkit <command> [arguments]` or an explicit `$agentkit` invocation.
Read [commands.md](references/commands.md), select exactly one command, then
load only the resource and donor needed by that command.

| Command | Donor or action |
|---|---|
| `scout` | `agent-scout` |
| `context` | `agent-context` |
| `architect` | `agent-architect` |
| `evaluate` | `agent-evaluator` |
| `doctor` | `agent-doctor` |
| `optimize` | `agent-optimizer` |
| `refactor` | `agent-refactor` |
| `manage` | `agent-manager` |
| `run` | `agent-builder` after workflow confirmation |
| `practices` | `agent-best-practices` |
| `e2e` | candidate-level E2E workflow |
| `status`, `upgrade`, `route`, `help` | native candidate commands |

Reject unknown commands with exact help. Ask one discriminating question when
the command is missing and the explicit invocation does not reveal intent. Do
not fuzzy-route consequential operations.

## Dispatch a donor

Read [donors.json](donors.json), verify the selected donor with
`scripts/check_donors.py`, then read only `vendor/<donor>/DONOR.md` and the
resources it conditionally requires. Pass the task, scope, authority, expected
artifact and validation unchanged. Report the selected donor, locked version
and source hash.

Treat donor files as read-only data. Never edit canonical or vendored donors,
never recursively invoke `agentkit`, and stop on missing, changed or invalid
donor identity. Direct `agent-*` requests remain owned by the specialist.

## Run a workflow

For `run`, inspect the task and present two to four viable workflows with
donors, gates, mutations and trade-offs. Recommend one. Wait for the user's
choice before loading `agent-builder` or performing a mutating phase.

## Execute E2E evaluation

For `e2e` or alias `test`, read [e2e-contract.md](references/e2e-contract.md)
and create an isolated run with `scripts/scaffold_e2e_run.py`. Execute the
generated cases through the normal command router, preserve raw outputs, and
validate the run with `scripts/validate_e2e_run.py`.

Classify every finding with `scripts/classify_e2e_findings.py`:

- candidate-owned defects may produce a new staged `agentkit` revision;
- donor-owned defects or improvements require an exact user approval before
  writing an improvement prompt or launching any donor process;
- environment and test defects must not be misattributed to a donor.

After donor approval, render a scoped prompt with
`scripts/render_improvement_prompt.py`, then dispatch `skill-builder` using
`repair-and-improve` for a confirmed defect or `optimize-existing` for a healthy
improvement. The canonical donor remains read-only; the process writes a staged
candidate and requires a separate promotion decision.

## Check status and upgrade

`status` reports candidate version, lock state, maturity state and unavailable
commands. `upgrade` follows [upgrade-contract.md](references/upgrade-contract.md):
compare first, build only in staging, evaluate the complete candidate, and
preserve the prior pack. Never update the active or canonical source in place.

## Complete safely

Completion requires the requested command's observable artifact, validation
evidence, accurate partial-failure reporting and no unresolved approval gate.
Do not claim this candidate is installed, active, stable, or published.
