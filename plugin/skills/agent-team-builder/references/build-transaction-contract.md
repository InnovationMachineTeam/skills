# Build transaction contract

A build manifest is the immutable bridge between approved design and file
mutation. It identifies the approved spec by ID, version and digest; records
expected registry/map revisions; sets `activation: false`; and enumerates every
filesystem or registry operation.

Each operation declares path, action, asset kind, visibility, owner when private,
source spec reference and collision policy. A private operation's destination
must remain below the owning agent's directory and its consumers must equal that
owner. Marketplace/public output must never include a private operation.

The transaction also names backups, validations and rollback. Promotion from
staging is allowed only when the staged digest equals the reviewed manifest and
expected revisions still match.

Outcomes are explicit: `STAGED`, `APPLIED`, `NOOP`, `BLOCKED`, `ROLLED_BACK`.
Do not call an incomplete build successful.
