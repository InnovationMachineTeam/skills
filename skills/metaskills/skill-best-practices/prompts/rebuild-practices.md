# Route: rebuild-practices

Regenerate the complete thematic corpus from an approved claim ledger.

1. Create a clean staging directory outside the active installed skill.
2. Recreate `INDEX.md` and every required thematic file.
3. Write concise imperative practices with source IDs, platform scope, conflicts, and validation consequences.
4. Remove superseded guidance while preserving an explicit replacement or deprecation note.
5. Avoid duplicated rules across topics; use one canonical owner and cross-reference it.
6. Run corpus validation and inspect the semantic diff against last-known-good.
7. Present material changes, especially weaker safety, broader permissions, or changed lifecycle behavior.
8. Replace only the authorized review bundle after validation.

If the reconciliation ledger contains no material change and the corpus is healthy, return `NO_REBUILD` unless force was explicit.
