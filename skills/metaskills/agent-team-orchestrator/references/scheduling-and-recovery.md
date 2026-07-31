# Scheduling and recovery

Prefer the simplest declared topology:

- sequential for dependent work or shared writes;
- pipeline for stable typed stage boundaries;
- fork-join for independent bounded branches with one integration owner;
- DAG for non-linear dependencies;
- dynamic dispatch only within pre-approved roles, permissions and budgets.

Use leases with owner, issued/expiry timestamps and fencing token when mutable
shared state is involved. Expired ownership cannot commit results without
revalidation.

Classify failure before acting: transient, deterministic, policy/authority,
dependency, conflict, budget, cancellation or unknown. Retry only transient
failures within limits. Use compensation for already committed reversible
effects, rollback for staged changes, degradation only when acceptance criteria
permit it, and human escalation for authority or consequential ambiguity.
