# Practical Implementations: Comparative Analysis

Research was conducted against default branches as of 2026-07-30. Exact commits
are recorded in [sources-frameworks.md](sources-frameworks.md).

## Comparison

| Project | Primary unit | State/knowledge | Orchestration | Strongest pattern |
|---|---|---|---|---|
| Agent OS | standards + spec folder | product/standards/specs | interactive commands | relevant standards injection |
| BMAD | role agent + workflow skill | sequential artifacts | phase map + menus | progressive context by lifecycle |
| GSD Core | phase/plan/subagent | `.planning/STATE.md` + artifacts | thin orchestrator, waves | fresh-context agents + goal verification |
| GSD Pi | runtime unit/extension | DB + Markdown projections | durable runtime/worktrees | extension-first Agent OS |
| gstack | specialized skill | sessions/learnings/artifacts | router + specialist fan-out | product-to-ops role suite |
| Spec Kit | constitution/spec/plan/tasks | `.specify/` + `specs/` | command pipeline | executable spec + constitution gate |
| OpenSpec | change folder + delta spec | `specs/` + `changes/` | fluid actions | brownfield delta and progressive rigor |

## Agent OS (`buildermethods/agent-os`)

### Useful solutions

- Product context is divided into mission, roadmap, and tech stack.
- Standards are indexed and selected for the current task.
- Injection changes form depending on the conversation, skill, or plan.
- An ambiguous mode is clarified with the user.
- The spec folder keeps the plan, shaping decisions, standards, references, and
  visuals together.
- Similar implementations in the codebase are searched first.

### What to adopt

- an index with short descriptions instead of loading all standards;
- a context-sensitive format;
- links to the canonical standard are preferable to copies when portability does
  not require a self-contained artifact;
- "save the specification" as the first plan deliverable;
- lightweight shaping before implementation.

### Limitations

The reference/copy choice can create drift; dependency tracking is needed. It is
not acceptable to rely only on interactive questions in a headless workflow; an
explicit fallback policy is required.

## BMAD Method

### Useful solutions

- Roles are understandable to the business: analyst, PM, architect, developer,
  UX, writer.
- Workflow skills are separated from free-form conversational triggers.
- Analysis -> Planning -> Solutioning -> Implementation produce artifacts that
  become context for the next step.
- `project-context.md` acts as the project constitution.
- For testing there is a lightweight path and a separate enterprise-grade Test
  Architect with risk priorities, NFR, and traceability.
- A readiness gate exists before implementation.

### What to adopt

- directories of "role -> triggers -> workflows -> outputs";
- progressive context rather than one long session;
- two levels of process rigor;
- a dedicated technical writer role;
- requirements traceability and a release gate for complex domains.

### Limitations

Personas and menus improve UX, but should not replace machine contracts. A
phased process must be compressible for small changes.

## GSD Core

### Useful solutions

- A thin orchestrator holds state, while research/plan/execute/verify are
  performed by fresh-context specialized agents.
- Durable Markdown artifacts survive a session reset.
- The cycle is Discuss -> Plan -> Execute -> Verify -> Ship.
- The plan contains wave, depends_on, files_modified, and must-haves.
- Each executor receives a bounded plan; waves parallelize independent work.
- The goal-backward verifier does not trust SUMMARY and checks truths,
  artifacts, wiring, and prohibitions.
- Human-needed cases are accounted for instead of false auto-pass behavior.
- There are quick/fast paths, pause/resume, workspaces, workstreams, hooks, and
  context monitoring.

### What to adopt

- context isolation as an architectural principle;
- a mandatory structured handoff;
- the orchestrator does not duplicate the dispatched task;
- a state spine and recovery;
- outcome verification rather than task completion;
- fail-safe human judgment;
- flat orchestration that prevents deep recursion.

### Limitations

A large prompt/workflow surface increases maintenance cost. Platform adapters
and generation should be accompanied by parity tests; a rigid full loop is
excessive for simple tasks.

## GSD Pi

### Useful solutions

- Extension-first: the core is minimal, capabilities live in
  extensions/skills.
- The manifest declares ID, semver, tier, compatibility, provides, and
  dependencies.
- Three tiers: core, bundled, community.
- Topological dependency order and namespaced tools.
- Stateful extensions are restored on session start/switch/tree changes.
- Tool outputs are bounded; long operations listen for cancellation.
- `pi.exec` centralizes sandboxing, timeouts, and signals.
- Project state is stored in a DB with Markdown projections.
- Worktree safety checks root, branch, and lease in fail-closed mode.

### What to adopt

- an Agent OS registry/extension lifecycle;
- a capability manifest and compatibility check;
- canonical structured state plus reviewable projections;
- a headless/UI distinction;
- a state reconstruction contract;
- extension testing as a release requirement.

### Limitations

Manifest informational fields should be checked against the actually registered
capabilities. Missing dependencies/cycles are better blocked for a
high-assurance tier rather than only warned about.

## gstack

### Useful solutions

- A router directs planning, review, QA, debugging, security, release, and docs
  to narrow skills.
- A complete product-to-production set of roles.
- `office-hours`/CEO/engineering/design reviews separate perspectives.
- The review army selects specialists by scope and runs them independently.
- Historical finding rate can disable low-effectiveness reviewers except for
  insurance roles.
- Debugging follows "no fix without root cause".
- `/ship`, deploy, canary, and document-release form a closed delivery loop.
- Context save/restore, learnings, timeline, and opt-in telemetry.
- Templates generate host-specific skill outputs; generated files are not
  edited directly.
- Safety skills constrain destructive actions and write scope.

### What to adopt

- a router role rather than a mega-skill;
- adaptive specialist selection measured by telemetry;
- cross-model independent review;
- operational skills alongside development;
- first-run and headless fallbacks;
- a learning pipeline, but with governance.

### Limitations

A large shared preamble is expensive and can dilute the main task. Telemetry and
memory require data governance. "Boil the ocean" is useful as a product stance,
but should be bounded by a risk/cost budget.

## GitHub Spec Kit

### Useful solutions

- The constitution defines governing principles and semantic versioning of
  changes.
- A scope guard prevents the constitution command from silently starting
  implementation.
- WHAT/WHY are separated from HOW.
- The spec contains prioritized, independently testable user stories,
  Given/When/Then, FR, and measurable outcomes.
- The plan is checked against the constitution gate before and after design.
- Tasks have IDs, exact paths, dependencies, and `[P]` for safe parallelism.
- MVP-first vertical slices.
- Extensions, presets, and role bundles are separated.
- Hooks before/after stages extend the process.

### What to adopt

- a project constitution with governance/versioning;
- a scope guard and deferred intents;
- user-story-oriented tasks;
- explicit clarification markers;
- complexity violations require rationale;
- managed tooling updates are separated from evolution feature artifacts.

### Limitations

"Executable specs" do not mean the spec is automatically true. Human review,
live-code verification, and updates based on learning are still needed.
Optional tests should not remain optional for risky behavior changes.

## OpenSpec

### Useful solutions

- Current specs are separated from proposed changes.
- A change folder combines the proposal, delta specs, design, and tasks.
- ADDED/MODIFIED/REMOVED make brownfield evolution explicit.
- Specs describe behavior, not implementation.
- Progressive rigor: lite by default, full for cross-team/API/migration/
  security.
- Actions do not block returning to an earlier artifact.
- `/explore` does not write artifacts/code.
- Verification checks completeness, correctness, and coherence.
- Review order: proposal -> spec -> design/tasks -> code.
- Git ownership remains with the team; the tool does not hide version-control
  semantics.
- One change has one primary owner; parallel changes use separate folders.

### What to adopt

- a change package as the review unit;
- review intent before expensive code;
- delta specs and archive;
- the right to iteratively change design after learning;
- ceremony proportional to stakes.

### Limitations

Non-blocking verification and archive warnings are acceptable for lite mode, but
a high-assurance policy should turn critical gaps into a blocking gate.

## Synthesis

Recommended combined model:

1. OpenSpec progressive rigor and change folders.
2. Spec Kit constitution, WHAT/HOW separation, and vertical slices.
3. Agent OS indexed standards and reference discovery.
4. BMAD lifecycle roles and traceability.
5. GSD thin orchestration, fresh contexts, waves, and verification.
6. GSD Pi extension registry, durable state, and safety.
7. gstack product/quality/operations specialist suite and measured routing.
