# Durable runtime contract

States: `QUEUED`, `LEASED`, `RUNNING`, `WAITING_APPROVAL`, `VERIFYING`,
`SUCCEEDED`, `PARTIAL`, `FAILED`, `CANCELLED`, `COMPENSATING`, `ROLLED_BACK`,
`DEAD_LETTER`. Each transition records event ID, expected prior state, owner,
timestamp and evidence.

Mutable work requires a lease owner, expiry and fencing token. Terminal success
requires artifact hashes, acceptance evidence and verifier decision. A duplicate
event is ignored by stable event/idempotency key, not executed twice.
