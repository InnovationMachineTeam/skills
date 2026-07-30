# Agent-system capability scenario

Use when the requested product is a skill for designing, building, mapping,
evaluating, operating, or governing agents, teams, or Agentic OS.

1. Resolve whether the target is a skill bundle or a runtime agent definition.
   Route the latter directly to the relevant agent master prompt.
2. Load `docs/prompts/agent-skill-base.md`, then exactly one team/Agentic OS
   specialist prompt. For Agentic OS also load `agent-os-base.md`.
3. Run the capability placement gate before authoring: inline, private command,
   private skill, public skill, tool/script, workflow, use-existing, or reject.
4. Have `skill-architect` create a staged candidate with exact triggers,
   non-triggers, agent artifact schemas, authority, model-selection policy,
   resources and evals.
5. Register candidate assets and bindings through one expected-revision
   transaction. Private capabilities belong only to their owner agent and never
   enter marketplace bundles.
6. Hand the frozen candidate to `skill-evaluator` for routing, behavior,
   definition/map/version parity, capability-budget, access-denial, adapter,
   security, failure and lifecycle evidence.
7. Use doctor/architect for a new revision when evaluation fails. Use manager
   only for separately authorized activation, rollout or retirement.

Completion requires the minimal form decision, immutable candidate, registry
candidate, generated host views and independent evidence. File creation alone
is not completion.
