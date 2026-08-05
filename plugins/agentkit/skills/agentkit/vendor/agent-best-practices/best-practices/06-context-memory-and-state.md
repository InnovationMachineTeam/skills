# Context, Memory, and State

## Four Different Concepts

| Concept | Horizon | Example |
|---|---|---|
| Context | One model call/run | task brief, selected files |
| Session state | One dialog | current plan, tool results |
| Workflow state | Until process completion | DAG, leases, checkpoints |
| Memory | Across runs | confirmed decisions and learnings |

Mixing these layers creates stale decisions, uncontrolled prompt growth, and
impossible recovery.

## Context Engineering

Context is a limited budget. Build it as a package:

1. goal and acceptance criteria;
2. current constraints;
3. minimal source excerpts or links;
4. current state snapshot;
5. tools and permissions;
6. output contract;
7. open questions.

Order matters: high-signal instructions and criteria must not drown in raw
logs. Large tool outputs are truncated, saved as an artifact, and passed by
reference. GSD Pi sets an explicit cap on variable tool output as a safeguard
against context overflow ([repository](https://github.com/open-gsd/gsd-pi)).

## Progressive Disclosure

The agent first receives indexes and summaries, then loads details on demand:

```text
docs/INDEX.md
  → domain summary
    → canonical document
      → code/test evidence
```

Do not load the entire `docs/`, all memory, or all tools "just in case."
Retrieval should account for scope, freshness, authority, and permission.

## Durable State

A significant decision MUST be recorded before a context boundary or dispatch.
A good state spine contains:

- current goal/phase;
- task status and owners;
- adopted decisions;
- blockers and approvals;
- artifact references;
- last proven state;
- resume instruction.

GSD Core demonstrates the advantage of plain-text `.planning/STATE.md`;
OpenSpec uses change folders; gstack uses context-save/context-restore. The
general pattern is that important state lives outside the dialog, is versioned,
and is read by a new context.

## Memory Pipeline

```text
candidate → sanitize → verify → classify → approve → store → retrieve → revalidate
```

A memory item SHOULD have:

```yaml
id: learning-checkout-timeout
type: decision | fact | preference | pitfall | procedure
content: ...
source_refs: [...]
confidence: 0.9
scope: repo:checkout
owner: checkout-team
created_at: ...
last_verified_at: ...
expires_at: ...
sensitivity: internal
status: candidate | approved | stale | revoked
```

Automatically discovered "information" remains a candidate until verified.
Cursor warns that persistent memories can be poisoned by untrusted input
([automations](https://cursor.com/docs/cloud-agent/automations)).

## What to Store

Store:

- stable decisions with rationale;
- confirmed codebase characteristics;
- recurring failure modes and fixes;
- user preferences with explicit scope;
- verified commands and runbooks;
- retrospective outcomes and eval regressions.

Do not store:

- secrets and tokens;
- raw chain-of-thought;
- unverified assumptions as facts;
- random tool outputs;
- personal data without justification;
- information without provenance or a review deadline.

## Summary and Compaction

A summary MUST preserve:

- the goal;
- decisions and their rationale;
- changes and hashes;
- verifications;
- incomplete work and blockers;
- the next concrete operation.

It must not be a chronological retelling. Compare the summary to durable
artifacts; on conflict, the source of truth is the verified artifact/code, not
the summary text.

## Recovery

Resume protocol:

1. identify repo/worktree/branch;
2. load task/workflow state;
3. verify that referenced commits and artifacts exist;
4. detect drift since the checkpoint;
5. confirm leases and approval expiration;
6. restore only the required context;
7. continue with the first unfinished verifiable operation.

You cannot simply trust the line "continue from step 4" without checking live
state.

## Knowledge Freshness

A document or memory item must have an owner and an update trigger:

- API/code-path change;
- release;
- incident;
- policy change;
- review-period expiration;
- detected conflict;
- eval failure.

Stale knowledge is not silently deleted: it is marked, excluded from automatic
use, and sent to the owner for review.
