# skill-builder

`skill-builder` is the top-level orchestrator for the skill system. It accepts an explicit named scenario or infers the smallest sufficient workflow from the user's context, asks focused questions when a material decision is missing, and coordinates `skill-scout`, `skill-harvester`, `skill-architect`, `skill-evaluator`, `skill-doctor`, `skill-optimizer`, `skill-refactor`, `skill-manager`, and `optimize-prompts` through bounded handoffs.

## Named scenarios

1. `full-lifecycle`
2. `create-from-spec`
3. `discover-opportunities`
4. `research-to-skill`
5. `external-skill-adoption`
6. `evaluate-skill`
7. `repair-and-improve`
8. `optimize-existing`
9. `compare-and-refactor`
10. `split-and-migrate`
11. `portfolio-governance`
12. `master-prompt-development`
13. `specialist-dispatch`
14. `resume-build`

An explicit scenario is optional. For example, “turn this repository into a tested skill” routes to `research-to-skill`, while “use scenario `compare-and-refactor` for these two skills” selects that route directly.

For a single bounded evaluation request, invoke `skill-evaluator` directly. Use builder's `evaluate-skill` when the scenario is explicit, requires resumable orchestration state, or participates in a larger lifecycle.

## Core guarantees

- one primary scenario and the smallest sufficient specialist chain;
- read-only defaults and exact approval gates for mutations;
- resumable state for multi-phase work;
- evidence-bearing handoffs rather than narrative-only delegation;
- productionization gates adapted from gbrain `skillify` without requiring gbrain-specific commands;
- no false completion from scaffolding, static validation, or filesystem presence alone.

## State validation

```bash
python3 scripts/validate_build_state.py skill-build-state.json
python3 scripts/summarize_build_state.py skill-build-state.json
python3 scripts/check_evals.py evals
```

The package is a reviewable bundle. It does not install or activate itself.
