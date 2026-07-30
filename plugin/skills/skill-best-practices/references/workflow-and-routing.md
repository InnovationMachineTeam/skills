# Workflow and routing

## Route selection

| User outcome | Route |
|---|---|
| answer from or summarize the current practice corpus | `query-practices` |
| list and assess current resources | `source-audit` |
| check whether sources changed | `refresh-sources` |
| determine whether guidance must change | `reconcile-practices` |
| regenerate the thematic corpus | `rebuild-practices` |
| create the portfolio update prompt | `generate-modification-prompt` |
| audit or modify listed skills | `apply-practices` |
| perform the complete maintenance cycle | `full-refresh` |

## Bounded composition

Default to one route. Compose dependent maintenance routes only when the user explicitly requests each outcome, and execute them in dependency order. For example, `refresh-sources` → `reconcile-practices` is valid when the user wants refreshed evidence and a claim decision but forbids rebuilding. `query-practices` is a presentation route: it may run alone against the validated corpus or as the terminal step after a read-only refresh and reconciliation. In the latter case, label reconciled claims that are not yet in the corpus as pending evidence and do not claim that the corpus was rebuilt. Never infer a later mutating or generating stage from an earlier one. If requested stages depend on missing artifacts, identify the prerequisite and ask only when it materially changes the result.

## Shortest-path rule

Do not refresh the web merely to generate a prompt bound to an already validated practice revision. Do not rebuild practices for an availability audit. Do not apply practices merely because a rebuild completed.

## Clarification triggers

Ask when the exact registry, target corpus, managed roots, platform scope, external research authority, or write destination changes the result. Default to bundled registry, portable core plus explicitly represented platform overlays, read-only audit, and reviewable staging output.

## Role boundaries

This skill owns the declared source registry, evidence maintenance, and knowledge synthesis. It does not replace:

- `skill-harvester` for open-ended discovery or intake of new repositories, articles, documents, or corpora; harvest first, then explicitly add accepted sources to this registry;
- `skill-optimizer` for measured changes to one healthy skill;
- `skill-doctor` for confirmed defects;
- `skill-refactor` for topology changes;
- `skill-manager` for active lifecycle state;
- `skill-builder` for end-to-end multi-skill execution.
