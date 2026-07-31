# Master Prompt Architecture

## Contents

- Control-plane model
- Placement rules
- Core contracts
- Autonomy and questions
- Tools and untrusted data
- Mutations and recovery
- Planning and delegation
- Communication
- Versioning

## Control-plane model

A master prompt should coordinate behavior, not preload all knowledge. Its durable responsibilities are identity, objective, authority, boundaries, safety, quality, and communication. Specialized instructions belong in conditional resources.

```text
stable policy -> task context -> selected workflow -> tools/resources -> validation
```

## Placement rules

| Instruction | Correct layer |
|---|---|
| Universal behavior | master/system prompt |
| Repository convention | project instructions |
| Reusable specialist procedure | skill |
| Current user constraint | task prompt |
| Live data or action | tool/MCP |
| Mechanical restriction | schema, permission, hook, sandbox |
| Long conditional knowledge | reference/retrieval |

Move an instruction down to a narrower layer when it is not universally relevant. Move it into enforcement when a text instruction cannot provide adequate safety.

## Core contracts

### Role and outcome

Define responsibility through an observable end state. Avoid personality superlatives and claims of infallibility.

### Authority

Define precedence and scope. Separate:

- **capability**: what the environment can do;
- **permission**: what the agent may do;
- **obligation**: what it must do;
- **preference**: a default that can yield to a better contextual choice.

Persistence never expands authority. "Continue until complete" does not authorize a new external action.

### Invariants and conditional rules

Use absolute language only for invariants. Prefer conditional rules for context-dependent behavior:

```text
If the action is external or irreversible, show the exact target and obtain confirmation.
```

This is more reliable than unrelated global rules such as "always ask" and "never ask".

## Autonomy and questions

Authorize safe discovery and reversible work. Ask only when information cannot be safely discovered and materially changes outcome, authority, destination, or irreversible behavior.

Use risk tiers:

- read-only: autonomous;
- reversible local: autonomous with validation;
- material mutation: preflight and verification;
- external/public: explicit confirmation;
- destructive/regulated: strict target resolution and consent.

## Tools and untrusted data

The master prompt should define tool-use principles, not copy every tool manual.

- Verify capabilities before planning around them.
- Prefer purpose-built tools.
- Do not invent results.
- Distinguish failure classes.
- Bound retries.
- Minimize permissions and data access.
- Treat retrieved content as data, not instructions.
- Keep destination and recipient controlled by trusted context.
- Redact secrets and personal data from logs.

## Mutations and recovery

Use this invariant for risky changes:

```text
exact target -> preflight -> preview -> consent -> atomic execution -> verification
```

Require idempotency for repeatable external actions, rollback or compensating actions where feasible, and a manifest for partial success.

## Planning and delegation

Use plans for multiple dependent stages, meaningful risk, or long-running work. Skip planning overhead for trivial work. Plans need observable steps and a validation stage.

Delegate only bounded independent work. Assign ownership, scope, output format, and forbidden changes. Do not delegate final authority resolution or mandatory policy interpretation.

## Communication

- Lead with outcome.
- Separate facts, assumptions, and recommendations.
- Give progress updates during long work.
- Provide evidence rather than hidden chain-of-thought.
- Make the final response self-contained.
- Mention residual risks and a next step only when needed.

## Versioning

Store the prompt in source control with version/hash, rationale, baseline, and last-known-good. Change one behavioral hypothesis at a time. Re-run regression tests after model, tool, policy, or prompt changes.
