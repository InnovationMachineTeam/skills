# Agent Documentation Contract

Every created agent declares the documents it reads, owns, produces and
verifies. The contract is part of the immutable agent definition; runtime notes
and active task state remain outside it.

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
