# Agentic OS architecture contract

Every design pins one bounded use case and contains all six planes. A plane
declares owner, APIs, desired and observed state, permissions, SLO, threats,
failures and lifecycle. Cross-plane flows name protocols, schemas, trust zones
and policy enforcement points.

The walking skeleton must trace one authenticated request through policy,
registry resolution, durable task/lease, bounded execution, artifact/evidence,
independent verification, telemetry and terminal state. It includes rollback
and retirement even when only staged locally.

Architecture may mark a plane `reused`, but must name the exact existing
contract. Omission is not reuse. Each new component needs a simpler-alternative
comparison and a measurable trigger for future expansion.
