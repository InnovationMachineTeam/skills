# Agent Design and Its Contract

## Minimal Agent Specification

Every production agent MUST have a versionable contract:

```yaml
id: requirements-analyst
version: 1.0.0
purpose: Transform verified intent into testable requirements
owns:
  - docs/requirements/
inputs:
  required: [intent, stakeholders, constraints]
  optional: [research, existing_specs]
outputs:
  schema: requirements-report-v1
  artifacts: [requirements.md, traceability.md]
tools:
  allow: [read_repo, search_docs, write_docs]
  deny: [deploy, delete, send_external]
permissions: read-mostly
done_when:
  - every requirement has id, rationale and verification
  - unresolved ambiguity is explicit
escalate_when:
  - two authoritative sources conflict
  - a high-impact decision lacks an accountable owner
budgets:
  max_turns: 12
  max_duration_minutes: 20
```

The syntax of a specific runtime may differ, but the semantic fields must be
preserved.

## Instructions

A good instruction answers seven questions:

1. What outcome does the agent produce?
2. What does it not do?
3. Which sources of truth does it use, and in what order?
4. Which tools are available and when?
5. What does a finished result look like?
6. What is checked before completion?
7. When does the agent stop and call a human?

A practical scaffold:

```markdown
## Role
Narrow competence and responsibility.

## Goal
Observable outcome, not a list of actions.

## Inputs and precedence
Sources, freshness, and conflict-resolution order.

## Scope
In scope, out of scope, write-set.

## Process
Key decisions and gates; not micromanagement of obvious actions.

## Output contract
Response schema, artifacts, evidence, and status.

## Validation
Commands, rubrics, independent checks.

## Escalation and stop conditions
Blockers, risk, budget, and user wait state.
```

Instructions SHOULD be concrete and declarative. Important prohibitions are
written as MUST NOT with a reason and a verification method. Do not mix persona,
workflow, and platform-specific workarounds in one unstructured text.

## Task Contract

The orchestrator passes not "help with the project," but a task envelope:

```yaml
task_id: REQ-042
objective: Find missing quality requirements for checkout
context_refs:
  - docs/product/prd.md
  - docs/architecture/context.md
constraints:
  - read_only: true
  - cite_file_and_line: true
expected_output:
  schema: review-findings-v1
acceptance:
  - findings classified by severity
  - every finding contains evidence and proposed verification
dependencies: []
deadline: 2026-07-30T16:00:00Z
```

Context is passed via references and a compact brief. The parent must not
assume that the subagent sees the dialog history: Claude, Codex, and Cursor all
emphasize isolated subagent context
([Claude](https://code.claude.com/docs/en/sub-agents),
[Codex](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[Cursor](https://cursor.com/docs/subagents)).

## Result Contract

The result MUST distinguish completed work from a claim about it:

```yaml
task_id: REQ-042
status: completed | partial | blocked | failed
summary: Short conclusion
artifacts:
  - path: docs/requirements/checkout-quality.md
    sha256: ...
evidence:
  - claim: p95 latency requirement is missing
    source: docs/product/prd.md#checkout
verification:
  - command: markdownlint docs/requirements/checkout-quality.md
    status: pass
open_questions: []
risks: []
handoff_to: requirements-owner
```

It MUST return a partial result upon cancellation or budget exhaustion if that
result is safe and useful. `completed` is invalid without evidence for the done
criteria.

## Tools

A tool is part of the agent interface, not just an API. Every tool SHOULD have:

- a unique verb-based name;
- one purpose;
- a strict argument and result schema;
- a description of preconditions and side effects;
- examples of a typical and edge-case call;
- idempotency or an idempotency key;
- clear errors that allow self-correction;
- timeout, cancellation, and bounded output;
- risk classification and approval requirement;
- an audit event without unnecessary secrets.

Hide rarely used and dangerous tools until needed. Merge similar tools or make
their names and parameters clearly distinguishable. OpenAI and Anthropic tie
agent quality to tool interface quality
([OpenAI](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/),
[Anthropic](https://www.anthropic.com/engineering/building-effective-agents)).

## Errors and Recovery

Minimal taxonomy:

| Type | Action |
|---|---|
| Validation error | Fix arguments, one limited retry |
| Transient | Backoff + jitter within the retry budget |
| Auth / permission | Stop and request the needed authorization without exposing the secret |
| Policy denial | Do not bypass; return the reason and a safe alternative |
| Dependency unavailable | Record state, propose resume |
| Ambiguous high-impact choice | Human checkpoint |
| Irreversible side effect uncertain | Fail closed |
| Budget exceeded | Partial handoff + resume token |

Retry MUST be tied to the error type. Repeating the same request without
changing conditions is not a recovery strategy.

## Versions and Compatibility

- Version the agent contract, prompt, tool schema, and output schema
  separately.
- A breaking change to input, output, or authority requires a major version.
- The orchestrator MUST check compatibility before dispatch.
- The trace records the effective agent, model, tool, and policy versions.
- Behavior should be tested on a fixed corpus before and after updates.
