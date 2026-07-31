# Agent Documentation Contract

Every created agent declares the documents it reads, owns, produces and
verifies. The contract is part of the immutable agent definition; runtime notes
and active task state remain outside it.

The complete creation and team workflows are in the
[Onboarding Guide](../ONBOARDING.md). Concrete domain layouts are in
[worked use cases](../use-cases/README.md).

## On-demand layout

```text
docs/agents/
├── specs/       # agent cards and immutable candidate specifications
├── contexts/    # provenance-bearing design context packages
├── evals/       # plans, datasets, scorecards and release evidence
├── operations/  # runbooks, pause/resume, rollback and incidents
└── changes/     # versioned behavior and compatibility changes
```

Create a branch only when a named consumer needs an artifact. Role-owned domain
documents remain in their domain: requirements under `docs/requirements/`,
architecture under `docs/architecture/`, and ADRs under
`docs/decisions/architecture/` by default.

## Required decisions

An applicable documentation contract records:

- exact read and write roots;
- artifact type, path pattern, owner, reviewers and consumers;
- source of truth and provenance requirements;
- status, freshness and supersession rules;
- indexes or registries updated with the artifact;
- validation and code-to-docs/doc-to-code checks;
- whether a capability is inline, a private command, a private skill or a
  public skill.

A software-architecture agent normally owns architecture proposals and may
propose ADRs, but an accountable human or policy owner accepts high-impact
decisions. If ADR authoring is reusable only by that agent, prefer an
owner-private `adr-authoring` capability over a globally discoverable skill.

## Capability registration

Every created agent and every public or private skill/command must be represented
in `docs/AGENT-ASSET-REGISTRY.json`. Applied bindings belong in
`docs/AGENT-SKILLS-MAP.json`. Their Markdown counterparts are generated review
views. Registration, mapping, installation, activation, and trust are separate
states.

## Evaluation evidence

An agent candidate is not complete merely because its files exist. Store frozen
plans, cases, raw outputs, scorecards, model/tool/prompt/skill versions, release
decision, and rollback evidence under `docs/agents/evals/`. Preserve builder and
evaluator correlation and label deterministic fixtures separately from semantic
workflow observations.
