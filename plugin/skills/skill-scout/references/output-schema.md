# Opportunity Manifest Schema

Use JSON with top-level `schema_version`, `scout_id`, `scope`, `sources`, `candidates`, `rejected`, and `open_questions`.

Each source requires `source_id`, `locator`, `consent`, and `sensitivity`.

Each candidate requires:

- `id`, `title`, `problem`, and `opportunity_type`;
- non-empty `evidence` with source IDs and locators;
- `existing_coverage` and `current_workaround`;
- `users`, `trigger_examples`, and `negative_triggers`;
- `context_plan`, `resources`, `tools`, `permissions`, and `risks`;
- non-empty `evaluation`;
- eight integer scores from 0 to 5: `frequency`, `leverage`, `repeatability`, `specificity`, `gap`, `evalability`, `risk`, `maintenance`;
- `decision`, `confidence`, and `next_step`.

Allowed decisions: `CREATE_NEW`, `EXTEND_EXISTING`, `USE_EXISTING`, `USE_AUTOMATION`, `KEEP_AD_HOC`, `RESEARCH`.

Use `scripts/validate_opportunities.py` before ranking. A valid manifest does not prove demand or ROI.
