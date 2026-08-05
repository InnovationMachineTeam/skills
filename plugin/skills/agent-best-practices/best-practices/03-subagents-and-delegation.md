# Subagents and Delegation

## When to Delegate

A subagent is useful when the task:

- has a clear boundary and a verifiable outcome;
- can be executed independently;
- creates a lot of intermediate noise;
- requires separate expertise, tools, or a permission set;
- benefits from independent review without the author's context;
- can safely run in parallel.

Do not delegate if handing off context is harder than the task itself, if the
work requires frequent synchronous decisions, or if two executors will edit the
same files.

## Good Delegation Units

- investigate a specific question and return an evidence table;
- produce a plan for one bounded change;
- implement a module with exclusive ownership;
- run a test segment and classify failures;
- perform a read-only security, accessibility, or performance review;
- check one document against the source code;
- test one competing defect-cause hypothesis.

Bad units: "study the project," "do everything," "help the main agent."

## Delegation as a Protocol

The orchestrator MUST perform six steps:

1. **Decompose**: build tasks and dependencies.
2. **Assign**: assign owner, write-set, tools, and budget.
3. **Brief**: pass the task envelope and source references.
4. **Observe**: monitor the lifecycle, but do not duplicate the work.
5. **Integrate**: verify schema, evidence, and conflicts.
6. **Verify**: independently verify the final outcome.

After dispatch, the orchestrator must not perform the same task in parallel.
GSD makes this an explicit rule to prevent duplication and conflicting edits.

## Context Isolation

A separate context reduces context rot, but creates an obligation to pass:

- the goal and the reasons behind it;
- current decisions and prohibitions;
- required files or artifact references;
- the actual workspace state;
- the expected response format;
- information about what the subagent does not know.

Before dispatch, everything needed SHOULD be saved to files or durable state.
The parent's conversational memory is not a reliable data bus.

## Ownership and Write-set

For write-heavy work, each subagent gets an exclusive file set or a separate
worktree:

```yaml
ownership:
  agent: api-implementer
  write:
    - src/api/**
    - tests/api/**
  read:
    - docs/**
    - src/shared/**
  forbidden:
    - infra/prod/**
```

If write-sets overlap:

1. split the task differently;
2. assign one writer and make the others reviewers;
3. use separate branches/worktrees and an explicit merge owner;
4. serialize the critical section.

Claude Agent Teams explicitly warns that teammates do not get automatic file
isolation; worktree management must be organized separately
([documentation](https://code.claude.com/docs/en/agent-teams)).

## Parallelism

Run in parallel only tasks with no unfinished dependencies and no overlapping
side effects. Represent the plan as a DAG:

```text
research ─┬─> api plan ─> api implementation ─┐
          └─> ui plan  ─> ui implementation  ├─> integration ─> verify
security review ──────────────────────────────┘
```

A wave is a set of ready nodes in the DAG. The next wave begins after the
previous outputs are verified. The "can run in parallel" marker SHOULD be
derived from the dependency graph and ownership, not assigned intuitively.

## Handoff

Handoff is transfer of control, not just transfer of text. It must include:

- `completed/partial/blocked/failed` status;
- what changed and where;
- evidence and verification results;
- open decisions and risks;
- the continuation point;
- the recommended next owner.

Use manager/agent-as-tool if one agent must synthesize a single answer. Use
handoff if a specialist should become the owner of the next dialog. This is the
official distinction in the OpenAI Agents SDK
([orchestration](https://openai.github.io/openai-agents-python/multi_agent/)).

## Independent Verification

The verifier SHOULD:

- receive the goal and artifacts, but not the author's reasoning;
- start with the hypothesis "the result is not proven";
- verify the outcome, not the number of closed tasks;
- read the source code and run checks;
- distinguish `failed`, `uncertain`, and `human_needed`;
- not fix what it finds if its role is read-only reviewer.

Separating implementer and verifier reduces confirmation bias. Cursor
recommends a skeptical verifier, and GSD formalizes goal-backward verification
([Cursor](https://cursor.com/docs/subagents),
[GSD](https://github.com/open-gsd/gsd-core)).

## Limiting Depth

Do not rely on a specific platform's maximum depth: it changes and differs
across platforms. Organizational practice:

- by default, one delegation level;
- a second level only for an explicit manager pattern;
- recursive teams are prohibited;
- each child inherits or tightens budgets and permissions;
- the trace preserves the full parent/child graph.

The deeper the tree, the worse visibility becomes for spending,
accountability, errors, and cancellation.

## Completion and Cancellation

The orchestrator MUST be able to:

- cancel the whole tree or a specific branch;
- wait for all required results;
- stop unnecessary tasks after a sufficient answer;
- collect a partial handoff on timeout;
- terminate background agents cleanly;
- not declare overall success until the required verifier is complete.
