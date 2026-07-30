# Практические реализации: сравнительный разбор

Исследование выполнено по default branches на 2026-07-30. Exact commits
зафиксированы в [sources-frameworks.md](sources-frameworks.md).

## Сравнение

| Проект | Основная единица | State/knowledge | Оркестрация | Сильнейший паттерн |
|---|---|---|---|---|
| Agent OS | standards + spec folder | product/standards/specs | интерактивные commands | релевантная инъекция standards |
| BMAD | role agent + workflow skill | последовательные artifacts | фазовая карта + menus | progressive context by lifecycle |
| GSD Core | phase/plan/subagent | `.planning/STATE.md` + artifacts | thin orchestrator, waves | fresh-context agents + goal verification |
| GSD Pi | runtime unit/extension | DB + Markdown projections | durable runtime/worktrees | extension-first Agent OS |
| gstack | specialized skill | sessions/learnings/artifacts | router + specialist fan-out | product-to-ops role suite |
| Spec Kit | constitution/spec/plan/tasks | `.specify/` + `specs/` | command pipeline | executable spec + constitution gate |
| OpenSpec | change folder + delta spec | `specs/` + `changes/` | fluid actions | brownfield delta and progressive rigor |

## Agent OS (`buildermethods/agent-os`)

### Полезные решения

- Product context разделён на mission, roadmap и tech stack.
- Standards индексируются и подбираются по текущей задаче.
- Injection меняет форму в зависимости от conversation, skill или plan.
- Неопределённый режим уточняется у пользователя.
- Spec folder сохраняет plan, shaping decisions, standards, references и
  visuals вместе.
- Сначала ищутся похожие реализации в codebase.

### Что перенять

- индекс с краткими описаниями вместо загрузки всех standards;
- context-sensitive format;
- ссылки на canonical standard предпочтительнее копии, когда portability не
  требует self-contained artifact;
- «сохранить спецификацию» как первый deliverable плана;
- lightweight shaping перед implementation.

### Ограничения

Reference/copy choice может создавать drift; нужен dependency tracking. Полагаться
только на интерактивные вопросы нельзя в headless workflow — требуется явная
fallback policy.

## BMAD Method

### Полезные решения

- Роли понятны бизнесу: analyst, PM, architect, developer, UX, writer.
- Workflow skills отделены от свободных conversational triggers.
- Analysis → Planning → Solutioning → Implementation производят artifacts,
  которые становятся контекстом следующего шага.
- `project-context.md` действует как project constitution.
- Для тестирования есть лёгкий путь и отдельный enterprise-grade Test Architect
  с risk priorities, NFR и traceability.
- Readiness gate перед implementation.

### Что перенять

- каталоги «роль → triggers → workflows → outputs»;
- progressive context, а не одна длинная сессия;
- два уровня process rigor;
- самостоятельная роль technical writer;
- requirements traceability и release gate для сложных доменов.

### Ограничения

Персонажи и menus улучшают UX, но не должны заменять machine contracts.
Фазовый процесс нужно уметь сжимать для small changes.

## GSD Core

### Полезные решения

- Тонкий orchestrator держит state, а research/plan/execute/verify выполняются в
  fresh-context specialized agents.
- Durable Markdown artifacts переживают session reset.
- Цикл Discuss → Plan → Execute → Verify → Ship.
- План содержит wave, depends_on, files_modified и must-haves.
- Каждый executor получает bounded plan; waves параллелят независимое.
- Goal-backward verifier не доверяет SUMMARY и проверяет truths, artifacts,
  wiring и prohibitions.
- Учитываются human-needed cases вместо ложного auto-pass.
- Есть quick/fast paths, pause/resume, workspaces, workstreams, hooks и context
  monitoring.

### Что перенять

- context isolation как архитектурный принцип;
- обязательный structured handoff;
- orchestrator не дублирует dispatched task;
- state spine и recovery;
- outcome verification, а не task completion;
- fail-safe human judgment;
- flat orchestration, предотвращающая глубокую рекурсию.

### Ограничения

Большой prompt/workflow surface повышает maintenance cost. Platform adapters и
генерация должны сопровождаться parity tests; жёсткий full loop избыточен для
простых задач.

## GSD Pi

### Полезные решения

- Extension-first: core минимален, capabilities живут в extensions/skills.
- Manifest декларирует ID, semver, tier, compatibility, provides и dependencies.
- Три tiers: core, bundled, community.
- Topological dependency order и namespaced tools.
- Stateful extensions восстанавливаются на session start/switch/tree changes.
- Tool outputs ограничены, long operations слушают cancellation.
- `pi.exec` централизует sandbox, timeouts и signals.
- Project state хранится в DB с Markdown projections.
- Worktree safety проверяет root, branch и lease fail-closed.

### Что перенять

- Agent OS registry/extension lifecycle;
- capability manifest и compatibility check;
- canonical structured state + reviewable projections;
- headless/UI distinction;
- state reconstruction contract;
- extension testing как release requirement.

### Ограничения

Manifest informational fields должны сверяться с фактически зарегистрированными
capabilities. Missing dependencies/cycles лучше блокировать для high-assurance
tier, а не только предупреждать.

## gstack

### Полезные решения

- Router направляет planning, review, QA, debugging, security, release и docs к
  узким skills.
- Полный product-to-production набор ролей.
- `office-hours`/CEO/engineering/design reviews разделяют перспективы.
- Review army выбирает specialists по scope и запускает их независимо.
- Историческая finding rate может отключать малоэффективных reviewers, кроме
  insurance roles.
- Debugging следует «no fix without root cause».
- `/ship`, deploy, canary и document-release образуют замкнутый delivery loop.
- Context save/restore, learnings, timeline и opt-in telemetry.
- Templates генерируют host-specific skill outputs; generated files не
  редактируются напрямую.
- Safety skills ограничивают destructive actions и write scope.

### Что перенять

- роль router, а не mega-skill;
- адаптивный specialist selection, измеренный telemetry;
- cross-model independent review;
- operational skills рядом с development;
- first-run и headless fallbacks;
- learning pipeline, но с governance.

### Ограничения

Большой общий preamble дорог и может размывать основную задачу. Telemetry и
memory требуют data governance. «Boil the ocean» полезен как продуктовая
установка, но должен ограничиваться risk/cost budget.

## GitHub Spec Kit

### Полезные решения

- Constitution задаёт governing principles и semantic versioning изменений.
- Scope guard не позволяет команде constitution незаметно начать реализацию.
- WHAT/WHY отделены от HOW.
- Spec содержит prioritized, independently testable user stories,
  Given/When/Then, FR и measurable outcomes.
- Plan проверяется constitution gate до и после design.
- Tasks имеют IDs, exact paths, dependencies и `[P]` для безопасного
  параллелизма.
- MVP-first vertical slices.
- Extensions, presets и role bundles разделены.
- Hooks до/после этапов расширяют процесс.

### Что перенять

- project constitution с governance/versioning;
- scope guard и deferred intents;
- user-story-oriented tasks;
- explicit clarification markers;
- complexity violations требуют rationale;
- managed tooling updates отделены от evolution feature artifacts.

### Ограничения

«Executable specs» не означают, что spec автоматически истинна. Нужны human
review, live-code verification и обновление при learning. Optional tests не
должны оставаться optional для рискованных behavior changes.

## OpenSpec

### Полезные решения

- Current specs отделены от proposed changes.
- Change folder объединяет proposal, delta specs, design и tasks.
- ADDED/MODIFIED/REMOVED делают brownfield evolution явным.
- Specs описывают behavior, не implementation.
- Progressive rigor: lite по умолчанию, full для cross-team/API/migration/
  security.
- Actions не блокируют возвращение к раннему artifact.
- `/explore` не пишет artifacts/code.
- Verification проверяет completeness, correctness и coherence.
- Review order: proposal → spec → design/tasks → code.
- Git ownership остаётся у команды; tool не скрывает version-control semantics.
- Один change — один основной owner; parallel changes — отдельные folders.

### Что перенять

- change package как review unit;
- review intent до дорогого кода;
- delta specs и archive;
- право итеративно менять design после learning;
- ceremony пропорционально stakes.

### Ограничения

Non-blocking verification и archive warnings приемлемы для lite mode, но high
assurance policy должна превращать critical gaps в blocking gate.

## Синтез

Рекомендуемая комбинированная модель:

1. OpenSpec progressive rigor и change folders.
2. Spec Kit constitution, WHAT/HOW separation и vertical slices.
3. Agent OS indexed standards и reference discovery.
4. BMAD lifecycle roles и traceability.
5. GSD thin orchestration, fresh contexts, waves и verification.
6. GSD Pi extension registry, durable state и safety.
7. gstack product/quality/operations specialist suite и measured routing.
