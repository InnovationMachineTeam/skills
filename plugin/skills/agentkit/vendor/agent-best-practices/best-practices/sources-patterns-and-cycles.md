# Источники: паттерны, циклы и operating model

Проверено: **2026-07-30**.

## Каталоги и reference architectures

### [Agent Design Pattern Catalogue](https://arxiv.org/abs/2405.10467)

Академический каталог из 18 архитектурных паттернов foundation-model agents.
Полезен прежде всего единым шаблоном pattern description: context, forces,
solution, consequences и relations, а не как обязательный checklist.

### [Taxonomy of Architecture Options for Foundation Model-based Agents](https://arxiv.org/abs/2408.02920)

Таксономия design-time и run-time решений и decision model. Помогает отличить
архитектурный выбор от конкретной реализации или vendor feature.

### [System-Theoretic Agentic Design Patterns](https://arxiv.org/abs/2601.19752)

Рассматривает patterns как взаимодействие пяти подсистем: reasoning/world
model, perception/grounding, action, learning/adaptation и inter-agent
communication. Используется как дополнительная современная перспектива;
практические правила сверяются с официальными runtime и security sources.

### [Responsible GenAI agent reference architecture](https://arxiv.org/abs/2311.13148)

Reference architecture для foundation-model agents с responsible AI concerns.
Полезна для separation of concerns и связи технических компонентов с assurance.

## Базовые agent/workflow patterns

### [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

Различает workflows и autonomous agents; описывает prompt chaining, routing,
parallelization, orchestrator–workers и evaluator–optimizer. Основной принцип —
начинать с минимально достаточной сложности и измерять улучшение.

### [OpenAI Agents SDK — Orchestrating multiple agents](https://openai.github.io/openai-agents-python/multi_agent/)

Разделяет LLM-driven и code-driven orchestration, manager/agents-as-tools и
handoffs. Даёт практические формы chains, loops, parallel execution и routing.

### [Microsoft Azure — AI agent design patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)

Описывает выбор single/multi-agent patterns и подчёркивает, что многоагентная
система наследует failure modes распределённых систем.

### [Microsoft — Multi-agent patterns](https://learn.microsoft.com/en-us/agents/architecture/multi-agent-patterns)

Практические topology, communication, MCP/A2A, security и human oversight.
Platform-specific детали не переносятся в универсальные MUST без адаптации.

### [Google ADK — Workflow agents](https://adk.dev/agents/workflow-agents/)

Детерминированные sequential, parallel и loop workflows, а также граница между
workflow и adaptive agent orchestration.

## Циклы

### [ASQ — PDCA cycle](https://asq.org/quality-resources/pdca-cycle)

Официальное профессиональное описание Plan–Do–Check–Act как повторяемого метода
изменений и continuous improvement. В агентных системах применяется к process и
release improvement, а не вместо runtime control loop.

### [Air University — OODA loop](https://www.airuniversity.af.edu/AFCLC/News/Article-Display/Article/1777083/cultural-ksas-skill-development-using-the-ooda-loop/)

Observe–Orient–Decide–Act для решений в меняющейся среде. Источник подчёркивает,
что orientation и ранний анализ нельзя механически сжимать ради скорости.

### [IBM — MAPE-K control loop](https://dominoweb.draco.res.ibm.com/reports/h-0219.pdf)

Monitor, Analyze, Plan и Execute используют общую Knowledge; autonomic manager
связан с managed element через sensors/effectors. База для self-management,
reconciliation и Agent OS operations.

### [Lean Startup principles](https://theleanstartup.com/principles)

Build–Measure–Learn проверяет гипотезы через минимальный продукт/эксперимент,
измеряет фактическую реакцию и приводит к pivot/persevere. Полезен для discovery
необходимости agent/skill и проверки ценности.

### [Chris Argyris — Double Loop Learning in Organizations](https://hbr.org/1977/09/double-loop-learning-in-organizations)

Различает коррекцию действий внутри существующих норм и пересмотр самих целей,
правил и предположений. Применяется при системных повторяющихся failures и metric
gaming; изменение intent/policy остаётся ответственностью человека.

### [ADLC](https://www.adlc.io/)

Intent, Generate, Validate, Govern, Deploy и Observe — concurrent modes для
agentic delivery. Соединяет экспериментальную генерацию, постоянную validation,
human governance, deployment и production learning.

## Risk, delivery и operations

### [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)

Govern является сквозной функцией, Map, Measure и Manage применяются итеративно
на всём lifecycle. Включает inventory, роли, independent review, monitoring и
safe decommissioning; это risk framework, не последовательный checklist.

### [DORA — Continuous delivery](https://dora.dev/capabilities/continuous-delivery/)

Связывает low-risk delivery с deployable state, test/deployment automation,
small batches, fast feedback, security и observability. Используется для
release/eval loops и operational metrics агентов, skills и workflows.

### [DORA — Continuous integration](https://dora.dev/capabilities/continuous-integration/)

Быстрые tests на каждом небольшом change и немедленное исправление regression.
Поддерживает script/tool development и сокращает feedback cycle.

### [Google SRE — Monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/)

Latency, traffic, errors и saturation — системная база; Agent OS добавляет
outcome, routing, tool, approval, safety, cost и lifecycle signals.

## Протоколы

### [Model Context Protocol](https://modelcontextprotocol.io/specification/latest)

Стандартизирует подключение tools/data/prompts. Discovery capability не
означает permission; authorization, validation и isolation остаются за host.

### [A2A Protocol](https://a2a-protocol.org/latest/specification/)

Межагентные discovery, tasks, messages и artifacts для независимых систем.
Полезен на организационных/runtime boundaries; локальные субагенты не обязаны
использовать сетевой протокол.

## Политика применения источников

1. Стандарт или official current documentation задаёт платформенные факты.
2. Official engineering guidance задаёт проверенную практическую эвристику.
3. Peer-reviewed/preprint catalogue даёт pattern language и alternatives.
4. Реализация подтверждает feasibility, но не превращает локальный выбор в MUST.
5. Любой pattern проходит локальные risk assessment и evals.

Если источник описывает trade-off, документ сохраняет условия выбора. Если
источники конфликтуют по факту runtime, приоритет имеет versioned specification
и проверка текущего поведения.
