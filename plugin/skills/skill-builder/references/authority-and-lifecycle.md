# Authority and lifecycle boundaries

## Default authority

Read-only inspection of explicitly scoped sources is the default. Creation may write only to an agreed review destination. Installed or active skill roots, external services, public repositories, consumers, and organization-wide settings require exact authority.

## Consequential gates

Before mutation present:

- exact source and target;
- current identity, hash, revision, and lifecycle state;
- operation and intended effect;
- affected hosts, users, consumers, dependencies, and credentials;
- files or external state to change;
- validation and acceptance criteria;
- rollback or compensating recovery;
- approval status.

Reconfirm if any target, effect, recipient, permission, dependency, or destination changed.

## Specialist authority

- Scout never mutates skills.
- Harvester defaults to read-only sources and separate authorized outputs.
- Creator may create a review bundle; installation is separate.
- Doctor repairs only after diagnosis and authority.
- Optimizer changes only the exact healthy target and does not deploy.
- Refactor defaults to assessment and requires an approved topology plan.
- Manager owns lifecycle application and target-host verification.
- Builder owns orchestration state, not specialist or user authority.

## Recovery

Prefer staging, copy, facade, quarantine, version pinning, and atomic or reversible operations. Preserve last-known-good artifacts. Never use broad recursive deletion. Do not retire the old version until replacement discovery, routing, behavior, consumers, and rollback are verified.
