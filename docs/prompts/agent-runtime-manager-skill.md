# Master Prompt For The `agent-runtime-manager` Skill

Apply after [agent-os-base.md](agent-os-base.md). Create an execution-plane skill
for the durable task/run lifecycle, not team design or agent authoring.

Define typed task envelope and state machine; queue semantics; leases,
heartbeats and fencing; idempotency/deduplication; attempts, checkpoints,
cancellation, deadlines and backpressure; scoped sandbox/tool credentials;
artifact/evidence commits; saga compensation and dead-letter handling. Pin exact
agent/workflow/model/policy versions for each run.

Separate scheduler, executor, policy and verifier responsibilities. Enforce
budgets and stop conditions outside model prompts. Test duplicate/out-of-order
delivery, worker loss, lease expiry, store/network/provider outage, partial side
effect, cancellation races, resume and poison task. Return run APIs, state
diagram, SLOs, metrics, recovery runbook and compatibility policy.
