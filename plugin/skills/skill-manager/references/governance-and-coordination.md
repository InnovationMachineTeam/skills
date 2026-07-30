# Governance and Coordination

## Contents

- Ownership and policy
- Portfolio evidence
- Specialist routing
- Organization-wide changes

## Ownership and policy

Assign owner, review status, supported hosts, lifecycle state, source, version, risk tier, and retirement date where relevant. Define who may approve installation, permission changes, organization rollout, and deletion.

## Portfolio evidence

Maintain inventories, change manifests, validation results, routing cases, health status, provenance, and rollback references. Avoid central registries that contain secret values.

## Specialist routing

- `skill-architect`: new or substantially redesigned capability;
- evaluator: independent eval/trigger design, execution, comparison, and release evidence;
- doctor: unhealthy, broken, unsafe, or unexplained regression;
- optimizer: healthy skill with measurable improvement target;
- installer: supported source installation;
- manager: portfolio state, conflicts, lifecycle, and governance.

Give specialists bounded ownership and preserve final lifecycle approval with the manager/user. Route opportunity discovery to `skill-scout`, evidence harvesting and pairwise comparison to `skill-harvester`, new capability creation to `skill-architect`, independent evaluation to `skill-evaluator`, unhealthy behavior to `skill-doctor`, measured single-skill improvement to `skill-optimizer`, and topology changes to `skill-refactor`.

For a changed high-risk candidate, evaluator freezes target identity, suite revision, environment, blocking gates, and holdout, then returns a layered verdict. Manager may use that verdict at a release gate, but only explicit lifecycle authority and host read-back can prove activation.

Route end-to-end workflows that span several of those stages to `skill-builder`. The builder owns phase state and handoffs; the manager retains lifecycle manifests, activation evidence, version state, and rollout approval.

## Organization-wide changes

Use staged rollout, canary users, monitoring, rollback, audit logs, and explicit approval. Do not infer enterprise authority from local filesystem access.
