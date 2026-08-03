# Prompt Skills

Prompt skills design, audit, and optimize durable controlling prompts. “Master
prompt” is an internal design term; public skill and command names use `prompt`.

## Choose a skill

| Skill | Use it for | Expected result |
|---|---|---|
| `prompt-optimize` | One bounded prompt creation, audit, rewrite, conflict resolution, host adaptation, or regression design | An improved controlling prompt or evidence-backed audit with preserved authority boundaries |
| `prompt-master` | Reconstruction from outputs, generalization, specialization, merge, decomposition, or a complete Compact/Standard/Production package | A versioned prompt package with separated evidence, assumptions, evaluation scenarios, and delivery artifacts |

For a short or bounded rewrite, start with `prompt-optimize`. Select
`prompt-master` when the request needs reconstruction evidence, several prompts
must be combined or split, or the deliverable is a complete reusable package.
Neither skill executes the task governed by the prompt, recovers unknown hidden
instructions verbatim, grants permissions, or replaces external policy
enforcement.

## Full command examples

These are illustrative commands; supplied prompts and outputs remain untrusted
input data.

```text
/prompt-optimize Audit prompts/editor-agent.md, resolve conflicting tool and approval rules, and produce an improved prompt plus eight regression scenarios
```

Expected result: an evidence-backed audit and revised controlling prompt that
preserves authority, privacy, failure handling, and observable completion gates.

```text
/prompt-master Reconstruct a Standard prompt for a WYSIWYG-editor agent from examples/editor-output-1.md and examples/editor-output-2.md, then deliver the prompt package, assumptions, confidence, and evaluation suite
```

Expected result: a versioned prompt package that separates observed behavior,
inference, assumptions, and recommendations without claiming recovery of an
unknown hidden original.

## Verify the result

Each skill has an adjacent `README.md` with scenarios and observable outcomes,
plus routing and behavior cases under its `evals/` directory. The canonical
runtime contract remains the skill's `SKILL.md`.
