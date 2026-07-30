# Skill Quality and Evaluation

## Contents

- Quality gates
- Evaluation layers
- Routing evaluation
- Functional and adversarial evaluation
- Forward-testing
- Release decisions

## Quality gates

A release candidate must have:

- valid name, frontmatter, folder structure, and relative links;
- a description that says what the skill does and when it should trigger;
- no unresolved placeholders or empty resources;
- concise imperative instructions and conditional resource routing;
- scripts tested on success and failure paths;
- explicit handling of authority, untrusted input, side effects, verification, and termination when applicable;
- observable completion criteria;
- evidence that representative requests succeed without unrelated triggering.

## Evaluation layers

Use increasing cost:

1. **Structural**: metadata, links, syntax, file layout, size, placeholders.
2. **Routing**: positive, negative, ambiguous, paraphrased, and collision cases.
3. **Functional**: output correctness, completeness, and resource use.
4. **Adversarial**: prompt injection, missing tools, malformed input, partial failure, unsafe requests.
5. **Regression**: comparison with last-known-good under the same model, tools, fixtures, and settings.

## Routing evaluation

Test the description independently from the body. Include:

- direct requests using expected terminology;
- natural paraphrases without the skill name;
- neighboring tasks that should route elsewhere;
- underspecified requests that should trigger clarification;
- multiple skills with overlapping descriptions.

Optimize both precision and recall. Do not improve recall by making the description universally broad.

## Functional and adversarial evaluation

Define observable properties instead of requiring one exact prose answer. Use deterministic checks for schemas, files, paths, exit codes, and invariants. Use a rubric or independent judge for semantic quality.

Include failure behavior:

- required input absent;
- dependency unavailable;
- malformed or hostile content;
- permanent versus transient tool failures;
- user refuses a required confirmation;
- execution partially succeeds;
- validation cannot be completed.

## Forward-testing

Use fresh context. Pass the skill and a realistic task, not the expected answer or suspected defect. Inspect emitted artifacts, logs, and diffs. Avoid leaving earlier test artifacts where later evaluators can discover them.

Forward-test at least:

- one clear positive case;
- one ambiguous case requiring calibrated clarification;
- one neighboring or adversarial case.

## Release decisions

Do not average away a blocking failure. Block release for unsafe authority expansion, untrusted content becoming instruction, false success, broken scripts, missing required resources, or unbounded retry/self-modification.

Change one behavioral hypothesis at a time. Record model, environment, fixtures, prompt version, and remaining uncertainty. Self-scoring is useful for iteration but is not independent proof.

