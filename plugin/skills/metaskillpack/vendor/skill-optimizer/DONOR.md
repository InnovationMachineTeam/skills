---
name: skill-optimizer
description: Measures and improves a healthy existing SKILL.md-based agent skill while preserving intended behavior, capability boundary, and authority. Use when a user asks to optimize, tune, compress, harden, or measurably improve one skill; improve its description or triggering; reduce context cost; reorganize resources; improve scripts or tool workflows; or strengthen safety and portability. Route independent evaluation plans, eval/trigger authoring, baseline or candidate runs, benchmarking, regression comparison, and release verdicts to skill-evaluator; route confirmed defects to skill-doctor; route composition, physical merge, split, subskill extraction, and compatibility-facade work to skill-refactor. Ask for the target and measurable outcome when no usable input is supplied. Do not use for ordinary task execution or unrelated new skill creation.
metadata:
  version: "1.0.0"
---

# Optimize Agent Skills

Improve an existing skill through evidence-backed, minimal experiments. Preserve the user's intent, output contract, authority boundaries, and known-good behavior unless a change is explicitly approved.

Route requested multi-stage recovery, refactor, or rollout workflows through `skill-builder`; retain measured single-skill optimization here.

Optimizer owns the hypothesis and candidate mutation. `skill-evaluator` owns an independent frozen baseline, holdout, run, comparison, and release-evidence verdict when those artifacts are requested or risk warrants separation. Do not tune the evaluation gate after seeing candidate failures.

## Intake

Accept a skill folder, `SKILL.md`, repository path, archive contents, pasted skill, evaluation results, execution traces, or a concrete description of observed failure.

If no usable target is supplied, ask for:

1. the skill or path to optimize;
2. the observed problem or desired measurable outcome;
3. any behavior, host compatibility, or authority that must remain unchanged.

Ask one to three questions per round. Do not edit or fabricate a target skill before receiving enough input to establish a baseline.

When input exists, inspect the complete bundle and available evidence. Ask only when missing information materially changes behavior, authority, target host, evaluation method, or permissible edits. Otherwise state a conservative assumption and proceed.

## Establish the baseline

Before editing:

1. Resolve the exact target and update scope.
2. Preserve unrelated user changes and identify existing validation commands.
3. Record target hosts, model/tool assumptions, installation state, and known constraints.
4. Run the bundled analyzer:

```bash
python3 scripts/analyze_skill.py path/to/skill --format json --output before.json
```

5. Run existing structural, routing, functional, script, security, and portability tests that are safe and relevant.
6. Capture representative successes and failures. Do not infer a routing defect from the description alone when execution evidence is available.

Treat analyzer findings as hypotheses, not verdicts. Do not claim improvement without a comparable post-change measurement.

When an independent baseline is supplied by `skill-evaluator`, preserve its target identity, suite revision, split, environment, metrics, blocking gates, and raw artifacts. Do not reveal holdout answers or overwrite baseline evidence.

## Classify the optimization

Read [references/optimization-taxonomy.md](references/optimization-taxonomy.md). Choose one primary route:

| Primary target | Prompt |
|---|---|
| Routing and discovery | [prompts/routing-discovery.md](prompts/routing-discovery.md) |
| Context and resource architecture | [prompts/context-architecture.md](prompts/context-architecture.md) |
| Workflow and reliability | [prompts/workflow-reliability.md](prompts/workflow-reliability.md) |
| Scripts and tool integration | [prompts/scripts-tools.md](prompts/scripts-tools.md) |
| Safety and authority | [prompts/safety-authority.md](prompts/safety-authority.md) |
| Evaluation-suite quality as an optimization target | [prompts/evaluation-regression.md](prompts/evaluation-regression.md) |
| Portability and packaging | [prompts/portability-packaging.md](prompts/portability-packaging.md) |
| Performance and context cost | [prompts/performance-cost.md](prompts/performance-cost.md) |

Select the route that best explains the observed failure or desired metric. Record secondary targets, but change one behavioral hypothesis at a time. If competing root causes require different experiments, order them rather than merging every optimization into one rewrite.

If evidence is insufficient to distinguish the leading routes, ask one discriminating question or run the cheapest safe diagnostic.

## Launch the optimization prompt

Read [prompts/base.md](prompts/base.md) completely and then the selected route prompt completely. Treat them as one contract. Load other references only when relevant:

- [references/experimental-method.md](references/experimental-method.md) for baselines, comparisons, and acceptance decisions;
- [references/description-and-routing.md](references/description-and-routing.md) for trigger precision, recall, and collisions;
- [references/context-and-resources.md](references/context-and-resources.md) for progressive disclosure and token cost;
- [references/evaluation-methods.md](references/evaluation-methods.md) for behavioral, adversarial, and regression suites;
- [references/safety-and-portability.md](references/safety-and-portability.md) for permissions, external actions, supply chain, and multiple hosts.

Execute the prompt rather than returning it to the user.

## Optimize experimentally

For each iteration:

1. State one falsifiable hypothesis.
2. Select metrics and cases able to disprove it.
3. Apply the smallest coherent change.
4. Keep model, tools, fixtures, settings, and environment constant where possible.
5. Run structural checks and the affected behavioral suite.
6. Inspect raw outputs, diffs, failures, and side effects.
7. Accept, revise, or reject the change based on predefined criteria.

Do not optimize the skill, model, tools, and evaluation rubric simultaneously. Do not shorten text by removing necessary safety, consent, recovery, or verification. Do not broaden triggers merely to increase recall. Do not use only self-scoring as independent proof.

When a change materially alters outputs, permissions, trigger surface, public behavior, or supported hosts, present the decision and obtain approval before treating it as optimization.

## Verify the candidate

Run the analyzer again:

```bash
python3 scripts/analyze_skill.py path/to/skill --format json --output after.json
python3 scripts/compare_reports.py before.json after.json
```

Also run the host's official validator and every changed script on positive and failure cases. Use [evals/routing.json](evals/routing.json) for optimizer routing and [evals/behavior.json](evals/behavior.json) for end-to-end behavior.

Validate the bundled eval schemas and coverage:

```bash
python3 scripts/check_evals.py evals
```

Forward-test substantial revisions with fresh context and realistic tasks. Do not reveal the expected answer, suspected defect, or intended fix to the evaluator. Verify emitted artifacts rather than trusting completion claims.

## Acceptance gates

Accept the candidate only when:

- the target metric improves or the confirmed defect is removed;
- no blocking safety, authority, or false-completion regression appears;
- previously valid representative behavior remains valid;
- routing precision and recall do not degrade outside the intended change;
- links, metadata, resources, scripts, and host assumptions remain valid;
- every removed instruction or resource is proven redundant or intentionally deprecated;
- residual uncertainty and untested surfaces are explicit.

Never return **ACCEPT** when the post-change primary behavioral metric was not run under comparable conditions. Static analysis, description coverage, reduced findings, or a plausible patch may support the hypothesis but cannot substitute for the target measurement; classify such a result as **INCONCLUSIVE** or **REVISE**.

If evidence is mixed, report the candidate as unverified or rejected rather than calling it improved. Preserve the last-known-good version or provide a reversible patch when practical.

## Deliver

Report:

1. baseline and primary optimization classification;
2. hypothesis and acceptance criteria;
3. critical findings and root cause;
4. changed files and intentional behavior changes;
5. preserved invariants;
6. before/after measurements and test evidence;
7. regressions, residual risks, and recommendation;
8. installation or deployment status.

Do not deploy, publish, install, or replace a production skill unless explicitly requested.
