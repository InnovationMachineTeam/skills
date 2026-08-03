---
name: agentkit
description: Explicit composite toolkit for the version-locked individual-agent lifecycle skills. Use only when the user invokes `$agentkit`, writes an `agentkit` command, asks for the agentkit command surface, or requests an agentkit E2E, upgrade, or status run. Route one explicit command to one read-only vendored donor, or use `run` for a confirmed multi-stage workflow. Do not trigger for ordinary agent design, evaluation, repair, optimization, team, Agentic OS, or direct `agent-*` requests; those belong to the corresponding specialist skills.
metadata:
  version: "1.0.2"
---

# Operate Agentkit

Provide one explicit entry point over locked individual-agent donors without
reimplementing their workflows. This stable bundle remains opt-in: direct
`agent-*`, team and Agentic OS requests keep their specialist routes.

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
| `e2e` | pack-level E2E workflow |
| `status`, `upgrade`, `route`, `help` | native pack commands |

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

For semantic runs, finalize the frozen evidence with
`scripts/record_real_workflow.py`; never relabel a deterministic router fixture
as a real observation. Classify every finding with
`scripts/classify_e2e_findings.py`:

- pack-owned defects may produce a new staged `agentkit` revision;
- donor-owned defects or improvements require an exact user approval before
  writing an improvement prompt or launching any donor process;
- environment and test defects must not be misattributed to a donor.

After donor approval, render a scoped prompt with
`scripts/render_improvement_prompt.py`, then dispatch `skill-builder` using
`repair-and-improve` for a confirmed defect or `optimize-existing` for a healthy
improvement. The canonical donor remains read-only; the process writes a staged
donor candidate and requires a separate donor promotion decision.

## Check status and upgrade

`status` reports pack version, lock state, release state and unavailable
commands. `upgrade` follows [upgrade-contract.md](references/upgrade-contract.md):
compare first, build only in staging, evaluate the complete replacement, and
preserve the prior pack. Never update the active or canonical source in place.
Use [rollback-contract.md](references/rollback-contract.md) and
`scripts/build_rollback_plan.py` for a read-only recovery plan. Verify frozen
upgrade, rollback and external holdout hashes before a release decision.

## Complete safely

Completion requires the requested command's observable artifact, validation
evidence, accurate partial-failure reporting and no unresolved approval gate.
Do not claim this skill is installed or active without target-host read-back.
