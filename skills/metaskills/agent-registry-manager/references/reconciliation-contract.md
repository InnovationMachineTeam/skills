# Registry reconciliation contract

Desired assets and bindings are versioned separately. Observed state records
host, discovery, installed/active version, hash and observation time. A
reconcile plan pins all input revisions and never edits projections directly.

Private capabilities require one owner, that owner as sole consumer and an
owner-scoped locator. Retirement requires consumer inventory, replacement or
explicit absence, observed deactivation and rollback evidence.
