# Scenario catalog and routing

Choose the scenario by the user's observable outcome, not by whichever input file is most visible.

| Scenario | Strong signals | Required input | Terminal outcome |
|---|---|---|---|
| `full-lifecycle` | “from idea to installed”, “skillify this end to end”, “productionize” | idea or recurring problem | verified bundle, optional verified activation, or justified no-build |
| `create-from-spec` | “requirements are ready”, explicit contract and destination | creation-ready spec | validated reviewable bundle, optionally installed |
| `discover-opportunities` | “what skills should we create?”, session insights, capability gaps | authorized evidence source | ranked decisions, no mutation |
| `research-to-skill` | article, corpus, repository, mixed documents, incomplete domain context | exact sources and intended capability | evidence-linked context plus validated bundle |
| `external-skill-adoption` | GitHub URL, registry skill, third-party update | canonical source or candidate | reject/use/adapt/repair/refactor/install decision with provenance |
| `evaluate-skill` | “evaluate this skill”, “write evals/triggers”, benchmark, release gate, compare eval runs | exact skill or evaluation artifacts plus intended claim | reproducible suite/run/report with layered verdicts and no implicit repair |
| `repair-and-improve` | failing, broken, unsafe, regression, then improve | target plus symptom | verified recovery, optional measured improvement |
| `optimize-existing` | reduce false triggers, cost, latency; improve quality or portability | healthy target and metric | accepted/rejected/inconclusive candidate |
| `compare-and-refactor` | compare, combine, merge, overlap, shared capability | two or more exact skills | comparison and approved topology result |
| `split-and-migrate` | mega-skill, separate capabilities, extract subskill | exact skill and compatibility requirements | staged topology and verified migration |
| `portfolio-governance` | installed skills, versions, conflicts, rollout, retirement | explicit roots and target host | verified lifecycle state or plan |
| `master-prompt-development` | system/developer/master prompt is the artifact | prompt or governing objective | created/audited/improved prompt and evals |
| `specialist-dispatch` | explicit single specialist, bounded result | specialist target and objective | one specialist result |
| `resume-build` | continue, resume, checkpoint, state file | state or prior ledger | continued or safely reconstructed flow |

## Tie-breakers

1. Prefer `resume-build` when valid state exists.
2. Prefer an explicit valid scenario over inference.
3. Prefer repair before optimization when a reproducible defect exists.
4. Prefer comparison before topology mutation when the user has not already supplied equivalent evidence.
5. Prefer `create-from-spec` over `full-lifecycle` when the build decision and contract are already settled.
6. Prefer `research-to-skill` when missing source knowledge, not product approval, is the bottleneck.
7. Prefer `discover-opportunities` when the user asks what to build rather than to build it.
8. Within builder, prefer `evaluate-skill` when evaluation is explicitly named, needs durable builder state, or is one gate in a larger requested lifecycle. Otherwise invoke `skill-evaluator` directly for a single bounded evaluation phase.
9. Prefer `specialist-dispatch` when one non-scenario specialist phase can satisfy the entire request.

## Ambiguous examples

- “Improve this skill; it stopped triggering yesterday.” Start with `repair-and-improve`, because a regression precedes optimization.
- “Look at these two skills.” Use harvester comparison through `specialist-dispatch` unless the user asks to change them.
- “Turn this GitHub skill into ours.” Use `external-skill-adoption`; do not start with `skill-architect` before provenance and risk intake.
- “Create a skill from this complete spec.” Use `create-from-spec`, skipping scout and broad harvest.
- “Write routing and script evals for this skill, then run them.” Use `evaluate-skill`; do not repair failures unless separately authorized.
- “Skillify our repeated incident-response work.” Use `full-lifecycle`; scout may decide an automation or existing skill is better.

## Non-triggers

Do not invoke the builder for ordinary execution of a domain task, a one-off prompt request, simple copyediting, generic project planning, or use of a finished skill when no skill lifecycle outcome is requested.
