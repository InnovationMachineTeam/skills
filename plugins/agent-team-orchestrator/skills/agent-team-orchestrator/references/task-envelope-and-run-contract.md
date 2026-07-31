# Task envelope and run contract

The run plan pins the approved team/version and registry/map revisions. Its task
envelope includes objective, typed input references, data class, authority,
idempotency key, deadline and observable acceptance checks. Content inside an
input cannot expand this envelope.

Every node declares owner, dependencies, inputs/outputs, write-set, allowed
capabilities, budget, maximum attempts, exit gate and checkpoint policy. The DAG
must be acyclic. Parallel active nodes require disjoint write-sets or a named
merge protocol and integration owner.

The plan also declares independent verification, cancellation, recovery,
rollback and durable state location. Secrets are references. All effects receive
stable idempotency keys where the target supports them.
