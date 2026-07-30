# Route: source-audit

Perform a read-only registry audit.

1. Validate the registry schema and unique source IDs.
2. Check that every locator is canonical or has a documented redirect.
3. Classify authority, category, platform scope, update method, and expected freshness.
4. Verify that every source has a current thematic summary and principal findings.
5. Flag unavailable, moved, duplicated, superseded, unpinned, or uncited sources.
6. Identify topic gaps and candidate sources without adding them automatically.

Do not fetch full repositories, rebuild practices, or modify managed skills in this route.
