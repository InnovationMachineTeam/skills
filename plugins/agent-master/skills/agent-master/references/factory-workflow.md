# Agent-system factory workflow

Execute in dependency order and record the reason for every skipped phase.

1. Analyze scope, risks, use cases and the minimum operating unit.
2. Research current harness, workflow, observability, memory, evaluation and
   Human-in-the-loop options from authoritative sources when the decision is
   time-sensitive.
3. Choose a harness through a shortlist, build/adopt/adapt comparison, fallback
   and ADR; do not choose by popularity.
4. Design only the necessary control, execution, context, observability,
   quality and governance capabilities. Add idempotent bootstrap and doctor
   interfaces when implementation is authorized.
5. Dispatch `process-orchestrator-architect`.
6. Dispatch `role-agent-architect` once per approved role; keep one-off and
   coordination-only roles in the orchestrator.
7. Dispatch `role-skill-architect` once per approved capability; keep owner-only
   components private until an independent consumer justifies promotion.
8. Dispatch `skill-implementation-engineer` only when a contract proves that a
   script, tool, adapter, hook or automation is necessary.
9. Integrate registrations, bindings, permissions, contracts, routing, state
   recovery, Human gates, observability, clean installation and the full
   user-to-artifact path.
10. Improve once: fix authorized critical or major findings, rerun affected
    regression and end-to-end gates, and backlog lower-value work.
11. Document architecture, decisions, operations, security, onboarding,
    rollback and remaining risks.

Re-evaluate later phases after each material result. A downstream phase cannot
use an unverified upstream artifact as if it had passed.
