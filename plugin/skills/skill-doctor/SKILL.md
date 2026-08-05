---
name: skill-doctor
description: Diagnoses unhealthy, unsafe or inconsistent skills and verifies minimal repairs. Use for loading, routing, resource, script, tool, permission, recovery, validation, portability or regression failures, and for health or root-cause reports. Require a target, symptom and repair authority. Route independent evaluation to skill-evaluator and healthy performance or quality improvements to skill-optimizer.
metadata:
  version: "1.0.4"
---

# Diagnose Agent Skills

Identify the smallest confirmed root cause of a skill failure, assign a health state, and repair only within explicit authority. Preserve evidence and known-good behavior.

## Select the mode

- **Check-up**: run read-only structural and behavioral health checks.
- **Diagnose**: reproduce a symptom and determine root cause without editing.
- **Repair**: apply the smallest safe correction after diagnosis and authorization.
- **Verify recovery**: rerun the original reproduction and relevant regressions after a repair.

Default to **Diagnose** when the user says only "doctor", "check", or "find what is wrong". Do not infer permission to edit, install, publish, upgrade dependencies, or change external systems.

Route a requested multi-stage repair → optimization → rollout workflow through `skill-builder`; retain diagnosis and recovery authority here.

## Intake

Accept a skill folder, `SKILL.md`, archive contents, repository path, validator output, logs, traces, failing requests, host error, or a description of changed behavior.

If no usable target is supplied, ask one to three questions:

1. Which skill or path should be examined?
2. What symptom occurs, and what was expected instead?
3. Is the request diagnose-only, or may confirmed defects be repaired? Which behavior and hosts must remain unchanged?

When input exists, discover answers from the supplied scope before asking. Ask only when missing information changes the target, repair authority, supported host, side effects, or meaning of recovery.

## Preserve evidence

Before editing:

1. Resolve the exact skill and instruction channels.
2. Record the target revision or hash, host, runtime, model, tools, permissions, dependencies, and installation state.
3. Preserve unrelated user changes and the original failing artifact or trace.
4. Identify the last-known-good version and recent changes when available.
5. Run the read-only doctor:

```bash
python3 scripts/doctor_skill.py path/to/skill --format json --output health-before.json
```

6. Reproduce the reported symptom with the smallest safe case. Do not mutate production or contact external systems merely to reproduce a failure.

Static findings are evidence, not proof of the reported root cause.

## Assign health and severity

Use the highest applicable health state:

- **UNSAFE**: the skill can expand authority, follow untrusted instructions, expose sensitive data, or perform uncontrolled consequential actions.
- **BROKEN**: the skill cannot be discovered, loaded, executed, or verified for its core outcome.
- **DEGRADED**: the skill works but has a confirmed non-blocking defect, unstable path, incomplete coverage, or unsupported claim.
- **HEALTHY**: no material defect was confirmed under the tested scope.

Rank findings as `BLOCK`, `HIGH`, `MEDIUM`, or `LOW`. Do not average away an unsafe or broken core path. A healthy result is scoped to the tested hosts and cases, not a universal guarantee.

## Classify the diagnostic domain

Read [references/diagnostic-taxonomy.md](references/diagnostic-taxonomy.md). Choose one primary domain:

| Domain | Prompt |
|---|---|
| Metadata and discovery | [prompts/metadata-discovery.md](prompts/metadata-discovery.md) |
| Context and resources | [prompts/context-resources.md](prompts/context-resources.md) |
| Scripts and dependencies | [prompts/scripts-dependencies.md](prompts/scripts-dependencies.md) |
| Tools and environment | [prompts/tools-environment.md](prompts/tools-environment.md) |
| Workflow, state, and recovery | [prompts/workflow-state.md](prompts/workflow-state.md) |
| Security and authority | [prompts/security-authority.md](prompts/security-authority.md) |
| Evals and regressions | [prompts/evals-regressions.md](prompts/evals-regressions.md) |
| Packaging and portability | [prompts/packaging-portability.md](prompts/packaging-portability.md) |

Choose the domain that explains the symptom, not merely the file containing it. Record secondary domains and test cheaper, safer hypotheses first. When evidence cannot distinguish causes, ask one discriminating question or run one bounded diagnostic.

## Launch the diagnostic prompt

Read [prompts/base.md](prompts/base.md) completely and then the primary domain prompt completely. Load references conditionally:

- [references/triage-and-root-cause.md](references/triage-and-root-cause.md) for reproduction and differential diagnosis;
- [references/repair-safety.md](references/repair-safety.md) before any edit;
- [references/verification-and-recovery.md](references/verification-and-recovery.md) for recovery and regression evidence;
- [references/environment-and-portability.md](references/environment-and-portability.md) for client, OS, runtime, dependency, or installation failures.

Execute the combined prompt; do not return it instead of diagnosing.

## Diagnose before repair

Use this evidence chain:

```text
symptom → minimal reproduction → candidate causes → discriminating checks → root cause → repair → same reproduction → regressions
```

Separate:

- symptom from root cause;
- correlation from causation;
- code defect from environment, permission, data, or host mismatch;
- transient failure from permanent failure;
- skill failure from model, tool, or evaluator failure.

Stop investigation when one cause explains the evidence and alternatives are reasonably excluded. Do not keep adding speculative findings.

## Repair safely

Repair only when the user explicitly authorizes edits or the current request clearly includes fixing the confirmed defect.

- Apply the smallest coherent patch to the exact target.
- Do not reinitialize over an existing skill.
- Do not broaden triggers, permissions, dependencies, hosts, or side effects as a repair shortcut.
- Do not upgrade dependencies unless incompatibility is confirmed and the change is approved.
- Do not delete evidence, user work, resources, or last-known-good artifacts.
- Prefer reversible edits and preserve rollback information.
- Stop and ask before destructive, public, external, regulated, or irreversible changes.

If the skill is healthy and the request is about efficiency, elegance, or incremental quality, report the healthy diagnosis and route to `skill-optimizer`.

## Verify recovery

Run the same reproduction under comparable conditions, then relevant regressions and the host's official validator. Generate a post-repair report:

```bash
python3 scripts/doctor_skill.py path/to/skill --format json --output health-after.json
python3 scripts/compare_health_reports.py health-before.json health-after.json
python3 scripts/check_evals.py evals
```

Do not report recovery when the original symptom was not retested. Structural validity cannot substitute for functional recovery. Classify untested or incomparable results as **UNVERIFIED**.

Forward-test substantial repairs with fresh context and without revealing the suspected defect or intended fix. Inspect raw artifacts and side effects.

When recovery evidence will support release, portfolio rollout, or a substantial behavior claim, hand the repaired immutable revision plus the original reproduction to `skill-evaluator`. Doctor owns root cause and minimal repair; evaluator owns the independent affected-regression, holdout, comparison, and layered release verdict.

## Deliver

Report:

1. mode, health state, and highest severity;
2. exact target and tested environment;
3. symptom and minimal reproduction;
4. root cause with evidence and excluded alternatives;
5. repair and changed files, if authorized;
6. preserved invariants and rollback information;
7. before/after recovery and regression evidence;
8. unresolved risks and required next step;
9. installation or deployment status.

Do not call the skill healthy, repaired, or recovered beyond the evidence actually obtained.
