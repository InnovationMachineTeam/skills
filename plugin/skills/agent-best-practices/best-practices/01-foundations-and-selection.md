# Foundations and Architecture Selection

## Terms

**Model call** transforms input into output and does not run its own loop.

**Workflow** directs models and tools through pre-defined code or a graph. The
model may make local decisions, but the overall control flow remains
deterministic.

**Agent** receives a goal, instructions, and tools, independently chooses
multiple actions, and works until an explicit stop condition.

**Subagent** is a constrained agent to which a parent delegated a specific
outcome. It runs in a separate context and returns a structured handoff.

**Orchestrator** selects executors, passes them context, manages dependencies,
budgets, retries, and final verification. It may be an LLM agent, a program, or
a hybrid.

**Agent team** is a set of peer or hierarchical participants with separate
contexts, a shared task board, and a messaging channel.

**Agent OS** is the operational layer above agents: capability catalog,
routing, state, memory, policy engine, sandbox, approvals, observability,
evals, artifacts, and lifecycle.

This distinction aligns with Anthropic's distinction between workflows and
agents and with current Claude Code surfaces: subagents, agent view, agent
teams, and workflow scripts ([Anthropic](https://www.anthropic.com/engineering/building-effective-agents),
[Claude Code](https://code.claude.com/docs/en/agents)).

## When an Agent Is Actually Needed

An agent is justified if the task combines several traits:

- it requires ambiguous decisions that are hard to express as a stable ruleset;
- it works with unstructured input;
- it has multiple possible paths and requires adaptation based on action
  results;
- it uses tools to obtain ground truth;
- it has a verifiable completion condition and a safe autonomy limit.

If the task is fully formalizable and predictable, you MUST use regular code.
OpenAI recommends agentic behavior for complex rule logic and unstructured data,
but to start with a simple solution
([guide](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)).

## Selection Matrix

| Situation | Recommended mechanism |
|---|---|
| Clear algorithm and data schema | Deterministic code |
| One intelligent step | One model call + structured output |
| Known sequence of steps | Prompt chain or workflow-as-code |
| Dynamic tool selection | One agent with a narrow toolset |
| Noisy exploration pollutes the main context | Subagent |
| Independent parts can run simultaneously | Parallel subagents |
| One answer must have a single owner | Manager / agents-as-tools |
| A specialist should continue the dialog directly | Handoff |
| Participants need peer-to-peer discussion and a shared board | Agent team |
| Dozens or hundreds of repeatable steps | Workflow-as-code / graph |
| Different runtimes or service owners | A2A with a published contract |

## Signals to Split One Agent

First improve tool descriptions, parameters, examples, and instructions. Then
split the agent if evals show at least one persistent problem:

- the prompt contains too many conflicting branches;
- tools are semantically similar and the agent picks the wrong one;
- domains require different rights or data sources;
- long tool outputs push the goal out of context;
- different parts require different models, budgets, or quality criteria;
- independent verification must be protected from implementer anchoring.

The number of tools by itself is not a criterion: OpenAI notes that overlap and
distinguishability matter more than a fixed threshold
([source](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)).

## Core Loops

### Agent loop

```text
goal → observe → decide → act → inspect result
                       ↘ stop / escalate / retry
```

Each loop MUST have:

- typed exit conditions;
- a maximum number of steps, time, and cost;
- cancellation handling;
- error classification into retryable, user-action, and terminal;
- event and acquired-artifact recording;
- escalation when the failure or risk threshold is exceeded.

### Evaluator-optimizer loop

```text
producer → candidate → evaluator → pass
                         ↓ feedback
                       producer
```

The loop is applicable only if the evaluation criteria are sufficiently
defined. It MUST have an iteration limit and a "best known result" policy,
otherwise agents may rewrite the output forever.

### Orchestrator-workers

```text
request → orchestrator → task graph → workers → evidence → synthesis → verify
```

The orchestrator SHOULD stay thin: store the goal, decisions, and state, but
not duplicate worker activity. This pattern aligns with Anthropic, the OpenAI
Agents SDK, and GSD.

## Progressive Rigor

Choose the process level by risk, not by team size:

| Level | Use case | Required artifacts |
|---|---|---|
| Lite | Reversible local change | intent, diff, verification |
| Standard | Multiple components or a user flow | spec, plan, tests, review |
| High assurance | Data, auth, money, migrations, compliance | threat model, NFR, traceability, approvals, rollback |
| Continuous ADLC | Autonomous delivery and production feedback | bet register, live policies, traces, evals, signals |

OpenSpec calls this progressive rigor; BMAD and GSD provide full phased
contours; ADLC offers continuous Intent-Generate-Validate-Govern-Deploy-Observe
modes. These models are compatible if rigor is enabled by risk policy rather
than imposed uniformly on all tasks.

## Selection Anti-patterns

- "Let's build a swarm because it's modern."
- Multiple agents with identical roles and no independent voting mechanism.
- LLM orchestration for a fully predictable sequence.
- One mega-agent with overlapping tools and contradictory personas.
- Delegation without a contract, owner, and done criteria.
- Parallel writes to the same files without isolation or a merge protocol.
- An autonomous loop without stop conditions, budget, and a cancellation
  operator.
