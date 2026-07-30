# Источники: исследованные реализации

Снимки изучены **2026-07-30** по shallow clone default branch. Commit позволяет
повторить анализ, даже если repository изменится.

## [buildermethods/agent-os](https://github.com/buildermethods/agent-os)

- Commit: `cae8e664fb59a01869718c3151e0f45b7a06a2fb`
- Изучено: README, `discover-standards`, `index-standards`, `inject-standards`,
  `plan-product`, `shape-spec`.
- Найдено: indexed standards; context-sensitive injection; lightweight shaping;
  product mission/roadmap/stack; spec folder с plan, decisions, standards,
  references и visuals; поиск reference implementation до планирования.

## [bmad-code-org/bmad-method](https://github.com/bmad-code-org/bmad-method)

- Commit: `9b672e1e6b9c2c69e1fbb1f4700089b8a6258003`
- Изучено: agent catalog, workflow map, testing, core/BMM skills и artifacts.
- Найдено: business-readable roles; menu triggers и workflow skills; progressive
  artifact chain Analysis→Planning→Solutioning→Implementation; project context;
  lightweight QA и enterprise Test Architect; NFR/traceability/release gates.

## [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core)

- Commit: `0408276791e62f70d98ee81e189a114c199278a9`
- Изучено: README, context engineering, multi-agent orchestration, agent
  definitions, plan/execute/verify workflows, state/spec/summary/verification
  templates, hooks и workspaces.
- Найдено: thin orchestrator; fresh-context specialists; durable `.planning/`;
  waves; must-haves; task/goal distinction; adversarial goal-backward verifier;
  human-needed semantics; pause/resume и context monitoring.

## [open-gsd/gsd-pi](https://github.com/open-gsd/gsd-pi)

- Commit: `8397230a7a900d627a5afff6d7db8112c6fb6a3d`
- Изучено: vision, runtime layout, worktree safety plan, extension SDK rules и
  manifest specification.
- Найдено: extension-first core; core/bundled/community tiers; compatibility и
  provides manifests; topological load; namespaced tools; bounded output;
  cancellation; lifecycle state reconstruction; DB + Markdown projections;
  branch/worktree/lease fail-closed safety.

## [garrytan/gstack](https://github.com/garrytan/gstack)

- Commit: `a3259400a366593e0c909dd9ac3e59752efd2488`
- Изучено: router, ETHOS, skills catalog, planning/review/QA/ship/debug/docs/
  context skills, review army, templates, telemetry and safety conventions.
- Найдено: suite router; role-based specialists across product-to-operations;
  independent fan-out review; adaptive specialist gating; no-fix-before-root-
  cause; release→deploy→canary→docs loop; context recovery; host-generated skills;
  safety scope; opt-in telemetry/learnings.

## [github/spec-kit](https://github.com/github/spec-kit)

- Commit: `e916fd1b3b6d9aa72e1e210bbedc447d5c572b38`
- Изучено: README, constitution/specify/plan/tasks/implement commands, templates,
  extensions/presets/bundles.
- Найдено: project constitution; scope guard; WHAT/WHY before HOW; prioritized
  independently testable user stories; measurable success; constitution gates;
  exact-path task DAG и parallel markers; MVP slices; workflow extension model.

## [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)

- Commit: `2b3d368539132be6311e55db58899abbf5306b81`
- Изучено: concepts, workflows, writing/reviewing specs, agent contract, team
  workflow, schemas и skills.
- Найдено: current specs vs change folders; behavior-first requirements;
  delta specs; progressive rigor; fluid actions; explore-before-artifacts;
  completeness/correctness/coherence verification; review proposal/spec before
  code; one owner per change; explicit Git boundary.

## Метод анализа

- Сначала прочитаны public docs и intended workflow.
- Затем проверены реальные agent/skill/workflow/templates/manifests.
- Практика считалась переносимой, если встречалась в нескольких реализациях или
  устраняла конкретный failure mode.
- Project-specific opinions не переносились как универсальные правила без
  risk/scope qualification.
- Численные platform limits не закреплялись как invariant.

