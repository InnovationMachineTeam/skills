# Refactor Plan Schema

Use JSON with `schema_version`, `plan_id`, `decision`, `inputs`, `outputs`, `rationale`, `preserved_invariants`, `trigger_ownership`, `resource_ownership`, `consumer_migrations`, `file_operations`, `validation`, `rollback`, and `approval_status`.

Allowed decisions: `KEEP_SEPARATE`, `COMPOSE`, `MERGE`, `SPLIT`, `EXTRACT_REFERENCE`, `EXTRACT_SUBSKILL`, `CREATE_FACADE`.

File actions: `KEEP`, `COPY`, `MOVE`, `CREATE`, `UPDATE`, `DELETE`. Every operation requires an exact target; mutation operations require an exact source when applicable. `DELETE` requires approved status, recovery evidence, and explicit rollback.

Use `scripts/validate_refactor_plan.py` before applying. Structural validity does not establish semantic correctness or migration safety.
