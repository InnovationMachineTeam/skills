# Scenario: full-lifecycle

Use when the user wants an end-to-end path from an idea or recurring problem to a verified, optionally activated skill.

1. Run `skill-scout` to decide `CREATE_NEW`, `EXTEND_EXISTING`, `USE_EXISTING`, `USE_AUTOMATION`, `KEEP_AD_HOC`, or `RESEARCH`.
2. Stop or reroute when the decision is not `CREATE_NEW`.
3. If context is insufficient, run `skill-harvester` with the smallest relevant research route; use `context-build` for iterative research.
4. Run `skill-architect` with the approved opportunity and research handoff.
5. Run `skill-evaluator` on the immutable candidate with routing, behavior, script/tool, security, coexistence, portability, and E2E layers proportional to risk.
6. Send reproducible failures to `skill-doctor`; after repair, evaluate the new revision against the original failure, frozen regressions, and holdout.
7. Use `skill-optimizer` only for a healthy candidate with a measurable unmet target, preserving the evaluator baseline. Let evaluator compare the candidate before acceptance.
8. Ask before installation or activation, then hand the exact evaluated bundle and layered release verdict to `skill-manager`.
9. Verify discovery, routing, E2E behavior, version, and rollback in the target host.

Do not force research, optimization, or installation when their entry conditions are absent. Evaluation may be scaled down for low-risk bundles but may not be replaced by structural validation. A `KEEP_AD_HOC` or `USE_AUTOMATION` decision is a successful terminal result.
