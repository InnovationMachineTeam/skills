---
name: role-skill-architect
description: Turns one approved role-agent capability into a researched, bounded, host-native skill package with triggers, method, knowledge provenance, contracts, examples, tests, evals, security, maintenance, and a justified implementation proposal. Use only when dispatched by agent-master for one capability owned by a designed role agent. Do not create a skill when an inline rule, command, knowledge source, tool, workflow, policy, or existing capability is sufficient.
metadata:
  version: "1.0.1"
---

# Build One Role Skill

Create one coherent, reproducible capability for a designed role agent. Apply a
worth and boundary gate before scaffolding, and adapt the package to the target
repository instead of copying a generic directory tree.

## Verify and classify the proposal

Require the process and orchestrator context, role-agent specification, exact
skill proposal, intended consumer, harness/host, environment, constraints,
research authority and output destination. Read
[references/output-contract.md](references/output-contract.md).

Classify the proposal as `SKILL`, `COMPOSITE_SKILL`, `MULTIPLE_SKILLS`,
`KNOWLEDGE`, `TOOL`, `POLICY`, `WORKFLOW`, `AUTOMATION`, `TASK`, `ROLE_DUTY`,
`USE_EXISTING` or `REJECT`. Split unrelated triggers, permissions, resources or
completion criteria. Prefer the smallest form with one primary outcome.

## Research the method

Use current official documentation, standards, law/regulation when applicable,
primary research, professional guidance and official source repositories.
Record publisher, locator, type, version/date, access date, supported decision,
limitations and conflicts. Treat community repositories as exemplars, not
standards. Do not freeze dynamic platform facts that should be retrieved at use.

Synthesize a stepwise method with decisions, inputs, outputs, quality checks,
failure behavior and boundaries. Distinguish research evidence from derived
judgment and preserve contradictory sources.

## Build the host-native package

Use the target host's canonical `SKILL.md` contract and only the resources that
improve reliability: references for detailed knowledge, scripts for repeated
deterministic operations, and assets for output ingredients. Keep instructions
concise and link resources one level away. Do not add generic README,
CHANGELOG, `skill.yaml` or empty directories unless the target format requires
them.

Define triggers, non-triggers, input/output/handoff contracts, Ready/Done,
self-review, confidence, security, observability, versioning, ownership,
freshness and update policy. Produce an implementation proposal only for
components whose necessity is demonstrated.

## Evaluate and hand off

Run structural, routing, functional, boundary, failure, adversarial, security
and regression tests proportional to risk. A release-bound package should cover
at least eight realistic scenarios, including positive, negative and edge
cases. Actually run every included executable on success and failure paths.

Return the complete reviewable skill package, source ledger, validation
evidence, eval results, implementation proposal and unresolved risks. Hand
necessary components to `skill-implementation-engineer`; do not implement
speculative infrastructure or claim installation/activation.
