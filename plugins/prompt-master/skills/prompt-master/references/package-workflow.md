# Prompt package workflow

Load and execute only sections required by the selected mode and depth.

## Normalize evidence and entities

Separate supplied instructions, observed behavior, inferred patterns,
assumptions and recommendations. Normalize goal, process, task, role, agent,
skill, tool, policy, artifact, metric and decision as distinct entities.

## Audit

When a source prompt exists, inventory its rules and use `prompt-optimize` to
classify ambiguity, conflict, duplication, missing contracts, unsafe authority,
unbounded loops and unavailable capabilities as Critical, Major, Minor or
Optional. Record the fragment, impact and correction.

## Design

Create only applicable control-plane sections: mission, owner, inputs,
instruction priority, authority, algorithm, tools, untrusted-data handling,
Human decisions, output contract, readiness, completion and evaluation hooks.
Keep project conventions in project instructions, specialist procedures in
skills, live facts in tools and hard controls in schemas or permissions.

## Assemble

For reconstruction, parameterize variable behavior and disclose uncertainty.
For merge, retain provenance and resolve contradictions. For decompose, give
each child one bounded responsibility. For optimize, explain every removed or
relocated rule.

## Verify

Check the complete package against the selected depth contract and evaluation
contract. A structural pass or shorter prompt is not evidence of behavioral
improvement.
