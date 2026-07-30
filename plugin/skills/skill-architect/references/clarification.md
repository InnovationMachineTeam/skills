# Clarification Strategy

## Ask only what changes the design

Use one to three questions per round. Prefer concrete examples over abstract feature lists. Stop asking when the skill can be built safely and tested meaningfully.

## No-input opening

Start with:

1. What should the skill enable the agent to accomplish?
2. Give one or two example requests that should trigger it.
3. Should the result be a reviewable folder or installed into a particular agent client?

Follow up only if architecture remains unclear.

## High-information questions

Choose only applicable questions:

- What observable output should a successful run produce?
- What should look similar but must not trigger this skill?
- Is the skill allowed to change files or external systems, or only analyze and propose?
- Which clients, models, tools, file formats, or operating systems must it support?
- Which knowledge, templates, scripts, examples, or existing skills should be bundled?
- Which actions require confirmation?
- How should partial success, retry, rollback, and failure be handled?
- Where should the skill be created, and should it be installed now?
- What would make you reject the generated result?

## Questions to avoid

- Do not ask for information already present in supplied artifacts.
- Do not ask the user to decide implementation details that can be inferred safely.
- Do not ask a long questionnaire before demonstrating understanding.
- Do not ask both universal "always ask" and "never ask" policies; calibrate by consequence.
- Do not block on optional UI metadata, icons, brand colors, or speculative future features.

## Assumption policy

Proceed with an explicit assumption when the choice is reversible, local, and unlikely to alter triggering or permissions. Ask when a choice changes global installation, overwrites an existing skill, contacts external systems, affects secrets, or creates destructive/irreversible behavior.

