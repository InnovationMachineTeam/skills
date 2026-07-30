# Visibility migration

## Promote private to public

Promotion is justified when a second independent consumer exists or the
capability has a useful contract, owner, release cadence, and lifecycle outside
its original agent. First remove owner-agent assumptions from prompts,
resources, paths, permissions, and evals. Stage a public candidate, preserve a
compatibility period, migrate registry/map references and consumers, verify
global discovery plus old/new behavior, then retire the private copy.

## Demote public to private

Demotion is justified only when consumer inventory proves one owning agent is
the sole remaining consumer and public discovery creates more collision or
maintenance cost than value. Stage the private candidate, set owner and allowed
consumers, migrate bindings, verify global non-discovery and owner use, then
retire the public entry.

## Required evidence

- exact current and desired paths, identities, versions, hashes, and owners;
- consumer and dependency inventory;
- trigger and permission comparison;
- registry/map and generated-adapter diff;
- owner-agent version impact;
- coexistence, access-denial, routing, behavior, and rollback tests;
- observed target-host discovery after change.

Private is an access/discovery scope, not a confidentiality guarantee.
