# Sources: Platforms, Runtimes, and Protocols

Checked: **2026-07-30**. Links point to primary/official materials.

## Anthropic and Claude Code

### [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

Key point: workflows and agents are different mechanisms; start simple; prompt
chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer;
an autonomous loop requires ground truth, stop conditions, and guardrails; the
tool interface must be understandable and testable.

### [Agents overview](https://code.claude.com/docs/en/agents)

Compares subagents, agent view, agent teams, workflows, and background shell.
It helps choose the coordination surface instead of calling any parallelism an
"agent team."

### [Subagents](https://code.claude.com/docs/en/sub-agents)

Isolated context; project/user/org scopes; tools, model, worktree, skills,
memory, hooks, and permissions; explicit/automatic/background invocation;
focus, least tools, version control, and independent parallel research.

### [Agent view](https://code.claude.com/docs/en/agent-view)

Human-dispatched independent background sessions, needs-input/working/completed
states, and a supervisor view. Suitable for multiple independent tasks managed
by a human.

### [Agent teams](https://code.claude.com/docs/en/agent-teams)

Lead + peers, shared task list, and direct messaging. Useful for parallel
research, competing hypotheses, and cross-layer ownership; poor fit for
sequential tasks and same-file edits. Teams do not provide automatic worktree
isolation.

### [Workflows](https://code.claude.com/docs/en/workflows)

A JavaScript workflow keeps the plan and intermediate state outside the main
context; it suits repeatable orchestration at the scale of tens or hundreds of
steps. The raw plan must be reviewed before execution; the workflow is treated
as code.

### [Worktrees](https://code.claude.com/docs/en/worktrees)

Separate checkouts for changes. Shared git metadata, project plugins, and
approvals mean that a worktree is not a full security boundary.
`.worktreeinclude` should be used carefully for ignored files.

## OpenAI and Codex

### [A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)

Agent = model + tools + instructions. Start with a single agent; split when the
logic is complex or there is tool overlap. Manager/agents-as-tools and
decentralized handoffs; layered guardrails; risk-rated tools; human
intervention based on failure thresholds and high-risk actions; model
optimization only after an eval baseline exists.

### [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

Hierarchical durable project instructions. The nearest file refines general
rules; instructions should be compact, practical, and link to detailed
documents.

### [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

Subagents for bounded exploration, tests, and triage; clean contexts reduce
context pollution. Custom agents should be narrow and have an explicit tool
surface. Read-heavy parallelism is safer than same-file write parallelism.

### [OpenAI Agents SDK: orchestration](https://openai.github.io/openai-agents-python/multi_agent/)

Distinguishes LLM orchestration from code orchestration. `agents as tools`
leaves the manager as the owner of the answer; `handoffs` transfer control to
the specialist. Code patterns: chains, evaluator loop, and parallel execution.

### [OpenAI Agents SDK: tracing](https://openai.github.io/openai-agents-python/tracing/)

Traces/spans for runs, agents, generations, tools, guardrails, and handoffs.
Sensitive inputs/outputs require dedicated configuration and data policy.

## Cursor

### [Agent overview](https://cursor.com/docs/agent/overview)

The overall Cursor Agent model and a tool-driven coding workflow.

### [Subagents](https://cursor.com/docs/subagents)

Foreground/background subagents with their own context;
planner→implementer→verifier; independent verifier; resume; cloud agents on
separate VMs/branches; the distinction between a one-shot skill and a multi-
step subagent.

### [Cloud Agent best practices](https://cursor.com/docs/cloud-agent/best-practices)

First a reproducible environment, secrets/network/local tests, then the prompt.
Rules/skills store repo procedures; tools should be agent-friendly and should
not produce excessive output.

### [Automations](https://cursor.com/docs/cloud-agent/automations)

Schedule/SCM/Slack/webhook/issue/incident triggers; service-account ownership;
the prompt defines decision rules, the quality bar, and the no-op outcome.
Persistent memory and MCP expand supply-chain/poisoning risk.

### [Bugbot](https://cursor.com/docs/bugbot)

Automatic incremental PR review, severity, analytics, dry-run, and optional
autofix. Findings should not be treated as blocking without an explicitly
configured policy.

### [Security agents](https://cursor.com/docs/security-agents)

PR Security Reviewer and scheduled Vulnerability Scanner; custom checks,
instructions/tools; metrics and audit per run.

### [Approval agents](https://cursor.com/docs/approval-agents)

Approval does not replace full review. Exact-path policies, stricter fallback,
and the inability of a change to weaken its own base policy.

### [Cloud Agent security](https://cursor.com/docs/cloud-agent/security)

MicroVM isolation, lifecycle, and retention; auto-run + internet create
injection and exfiltration risks; mitigations include egress, redaction,
review, and signed commits.

### [Cloud Agent network](https://cursor.com/docs/cloud-agent/security-network)

Allow-all/default+allowlist/allowlist-only; exact hosts are preferable to
wildcards; environment/team/enterprise precedence.

### Additional Cursor Materials

- [Agent best practices](https://cursor.com/blog/agent-best-practices) —
  practical prompting and task setup.
- [Cloud agent lessons](https://cursor.com/blog/cloud-agent-lessons) —
  environment as a product, durable execution, state separation, and
  self-healing.
- [Cloud agent development environments](https://cursor.com/blog/cloud-agent-development-environments)
  — reproducible agent environment.
- [Agent autonomy and auto-review](https://cursor.com/blog/agent-autonomy-auto-review)
  — autonomy, review, and trust boundaries.

## Google and Interoperability

### [Google ADK multi-agent workflows](https://adk.dev/agents/multi-agents/)

Composition of specialized agents, delegation, and shared session state.

### [Google ADK workflow agents](https://adk.dev/agents/workflow-agents/)

Deterministic sequential, loop, and parallel orchestration without model
decision; newer graph/dynamic workflows provide more control.

### [A2A specification](https://a2a-protocol.org/latest/specification/)

Cross-platform agent discovery and interaction: Agent Cards, skills,
capabilities, tasks, messages, artifacts, streaming, async updates, cancel,
versioning, auth, and security. Apply it to opaque agents behind a runtime/org
boundary.

### [MCP specification](https://modelcontextprotocol.io/specification/latest)

The host/client/server standard for giving a model access to tools, resources,
and prompts. MCP and A2A complement each other: MCP is the tool/data plane,
A2A is the agent-to-agent task plane.

## Microsoft

### [AI agent orchestration patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)

The complexity ladder and multi-agent patterns; specialization provides
modularity, but adds distributed-systems failures, latency, cost, and security
complexity.

### [Multi-agent patterns](https://learn.microsoft.com/en-us/agents/architecture/multi-agent-patterns)

Least privilege, typed payloads, descriptive errors, parallelism, human
approvals; MCP for tools/data, A2A for cross-platform opaque agents; users
should see collaboration and have cancel/skip controls.
