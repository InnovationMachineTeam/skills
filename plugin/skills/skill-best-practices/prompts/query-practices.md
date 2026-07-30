# Route: query-practices

Answer a question using the current validated practice corpus, optionally enriched by an explicitly requested read-only refresh and reconciliation, without modifying the corpus.

1. Resolve the user's platform, skill archetype, and desired answer form when material.
2. Read `best-practices/INDEX.md`, then only the relevant thematic files.
3. When preceded by refresh and reconciliation, distinguish validated corpus guidance from pending changed, new, conflicting, deprecated, or unverified evidence.
4. Distinguish portable rules, platform-specific guidance, enterprise policy, derived synthesis, and exemplar observations.
5. Cite practice IDs and source IDs for material recommendations.
6. Preserve documented conflicts, applicability limits, and the corpus revision date.
7. Return the requested explanation, comparison, or checklist plus any material freshness limitation.

Do not browse unless a preceding refresh route was explicitly requested. Do not rebuild, generate a portfolio prompt, or audit managed targets unless separately requested. Do not imply the corpus itself is newer than its recorded source-check date.
