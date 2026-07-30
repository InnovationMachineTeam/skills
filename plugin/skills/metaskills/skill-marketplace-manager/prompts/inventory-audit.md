# Route: inventory-audit

Perform a read-only inventory.

Collect:

- every `SKILL.md`, declared name, description, metadata version, and relative path;
- category depth and empty categories;
- marketplace and plugin manifests;
- generated bundles, mirrors, symlinks, absolute paths, and parent references;
- duplicate names and overlapping install channels;
- scripts, evals, README, provenance, license, ownership, and release metadata;
- current validator availability and results.

Return a catalog table, topology diagram only if relationships are complex, findings grouped as `FAIL`, `WARN`, and `INFO`, and recommended next route. Do not repair findings in this route.
