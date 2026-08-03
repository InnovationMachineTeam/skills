# Release 3.9.0 — capability-aware context profiles

Status: candidate  
Owner: InnovationMachineTeam  
Required reviewer: @stanislavus86  
Date: 2026-08-03

## Scope

This release introduces capability-based `standard` and `constrained` execution
profiles for `agent-master`, `prompt-master`, and `skill-builder`. Unknown or
unvalidated models default to explicit one-phase-at-a-time execution. Comparable
evaluation evidence is required before selecting the compact standard profile.

It also shortens high-cost discovery descriptions, adds a read-only hard-rule
audit, and registers Anthropic Claude 5 context-engineering guidance as a
platform-specific source rather than a portable standard.

## Preserved invariants

- public/private placement and package-private ownership;
- permissions, Human gates, secrets and data-boundary rules;
- frozen evaluation and holdout separation;
- state, recovery, rollback and truthful completion;
- no implicit installation, publication or activation.

## Verification contract

Release validation must include canonical documentation and repository checks,
marketplace and agent-asset validation, README determinism, capability-profile
unit coverage, all repository unit tests, staged individual packages, staged
aggregate package, and byte-level review of generated projections.

Behavioral model comparison remains `INCONCLUSIVE` until the same capability
suite is executed on declared strong and simple target models. Static context
reduction is not a behavioral release claim.

## Rollback

Restore release `3.8.0` and the previous individual skill versions, rebuild all
generated projections from canonical sources, and rerun the complete validation
suite. Do not retire or overwrite installed copies without separate lifecycle
authority and host read-back.
