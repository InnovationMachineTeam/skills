# Источники: платформы, runtime и протоколы

Проверено: **2026-07-30**. Ссылки ведут на первичные/официальные материалы.

## Anthropic и Claude Code

### [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

Ключевое: workflows и agents — разные механизмы; начинать с простого; prompt
chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer;
autonomous loop требует ground truth, stop conditions и guardrails; tool
interface должен быть понятным и тестируемым.

### [Agents overview](https://code.claude.com/docs/en/agents)

Сравнивает subagents, agent view, agent teams, workflows и background shell.
Помогает выбирать поверхность координации, а не называть любую параллельность
«командой агентов».

### [Subagents](https://code.claude.com/docs/en/sub-agents)

Изолированный контекст; project/user/org scopes; tools, model, worktree,
skills, memory, hooks и permissions; explicit/automatic/background invocation;
focus, least tools, version control и независимый parallel research.

### [Agent view](https://code.claude.com/docs/en/agent-view)

Human-dispatched независимые background sessions, состояния needs-input/
working/completed и supervisor view. Подходит для нескольких самостоятельных
задач, которыми управляет человек.

### [Agent teams](https://code.claude.com/docs/en/agent-teams)

Lead + peers, shared task list и direct messaging. Полезно для parallel research,
competing hypotheses и cross-layer ownership; плохо для последовательных задач
и same-file edits. Teams не дают автоматическую worktree isolation.

### [Workflows](https://code.claude.com/docs/en/workflows)

JavaScript workflow удерживает plan и intermediate state вне main context;
подходит для repeatable orchestration масштаба десятков/сотен шагов. Raw plan
нужно review до запуска; workflow рассматривается как код.

### [Worktrees](https://code.claude.com/docs/en/worktrees)

Отдельные checkout для changes. Shared git metadata, project plugins и approvals
означают, что worktree не является полной security boundary. `.worktreeinclude`
следует использовать осторожно для ignored files.

## OpenAI и Codex

### [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)

Agent = model + tools + instructions. Сначала single agent; split при сложной
логике или tool overlap. Manager/agents-as-tools и decentralized handoffs;
layered guardrails; risk-rated tools; human intervention по failure threshold и
high-risk actions; model optimization только после eval baseline.

### [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

Иерархические durable project instructions. Ближайший файл уточняет общие
правила; инструкции должны быть компактными, практичными и ссылаться на подробные
документы.

### [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

Subagents для bounded exploration, tests и triage; clean contexts уменьшают
context pollution. Custom agents должны быть узкими и иметь явную tool surface.
Read-heavy parallelism безопаснее same-file write parallelism.

### [OpenAI Agents SDK: orchestration](https://openai.github.io/openai-agents-python/multi_agent/)

Разделяет LLM orchestration и code orchestration. `agents as tools` оставляет
manager владельцем ответа; `handoffs` передаёт control специалисту. Code patterns:
chains, evaluator loop и parallel execution.

### [OpenAI Agents SDK: tracing](https://openai.github.io/openai-agents-python/tracing/)

Traces/spans для runs, agents, generations, tools, guardrails и handoffs.
Sensitive inputs/outputs требуют отдельной настройки и data policy.

## Cursor

### [Agent overview](https://cursor.com/docs/agent/overview)

Общая модель Cursor Agent и tool-driven coding workflow.

### [Subagents](https://cursor.com/docs/subagents)

Foreground/background subagents с собственным context; planner→implementer→
verifier; independent verifier; resume; cloud agents на отдельных VM/branches;
различие между one-shot skill и multi-step subagent.

### [Cloud Agent best practices](https://cursor.com/docs/cloud-agent/best-practices)

Сначала воспроизводимая environment, secrets/network/local tests, затем prompt.
Rules/skills хранят repo procedures; tools должны быть удобны для агента и не
создавать огромный вывод.

### [Automations](https://cursor.com/docs/cloud-agent/automations)

Schedule/SCM/Slack/webhook/issue/incident triggers; service-account ownership;
prompt задаёт decision rules, quality bar и no-op outcome. Persistent memory и
MCP расширяют риск supply-chain/poisoning.

### [Bugbot](https://cursor.com/docs/bugbot)

Автоматический incremental PR review, severity, analytics, dry-run и optional
autofix. Findings не должны считаться blocking без явно настроенной policy.

### [Security agents](https://cursor.com/docs/security-agents)

PR Security Reviewer и scheduled Vulnerability Scanner; custom checks,
instructions/tools; metrics и audit per run.

### [Approval agents](https://cursor.com/docs/approval-agents)

Approval не заменяет full review. Exact-path policies, stricter fallback,
невозможность change ослабить собственную base policy.

### [Cloud Agent security](https://cursor.com/docs/cloud-agent/security)

MicroVM isolation, lifecycle и retention; auto-run + internet создают injection
и exfiltration risks; mitigations включают egress, redaction, review и signed
commits.

### [Cloud Agent network](https://cursor.com/docs/cloud-agent/security-network)

Allow-all/default+allowlist/allowlist-only; exact hosts предпочтительнее
wildcards; environment/team/enterprise precedence.

### Дополнительные материалы Cursor

- [Agent best practices](https://cursor.com/blog/agent-best-practices) —
  practical prompting и task setup.
- [Cloud agent lessons](https://cursor.com/blog/cloud-agent-lessons) — environment
  как продукт, durable execution, state separation и self-healing.
- [Cloud agent development environments](https://cursor.com/blog/cloud-agent-development-environments)
  — воспроизводимое окружение агента.
- [Agent autonomy and auto-review](https://cursor.com/blog/agent-autonomy-auto-review)
  — автономность, review и границы доверия.

## Google и interoperability

### [Google ADK multi-agent workflows](https://adk.dev/agents/multi-agents/)

Композиция specialized agents, delegation и shared session state.

### [Google ADK workflow agents](https://adk.dev/agents/workflow-agents/)

Deterministic sequential, loop и parallel orchestration без model decision;
новые graph/dynamic workflows дают больше контроля.

### [A2A specification](https://a2a-protocol.org/latest/specification/)

Cross-platform agent discovery и interaction: Agent Cards, skills,
capabilities, tasks, messages, artifacts, streaming, async updates, cancel,
versioning, auth и security. Применять для opaque agents за runtime/org boundary.

### [MCP specification](https://modelcontextprotocol.io/specification/latest)

Стандарт host/client/server для доступа модели к tools, resources и prompts.
MCP и A2A дополняют друг друга: MCP — tool/data plane, A2A — agent-to-agent task
plane.

## Microsoft

### [AI agent orchestration patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)

Лестница сложности и multi-agent patterns; специализация даёт модульность, но
добавляет distributed-systems failures, latency, cost и security complexity.

### [Multi-agent patterns](https://learn.microsoft.com/en-us/agents/architecture/multi-agent-patterns)

Least privilege, typed payloads, descriptive errors, parallelism, human
approvals; MCP для tools/data, A2A для cross-platform opaque agents; users должны
видеть collaboration и иметь cancel/skip.

