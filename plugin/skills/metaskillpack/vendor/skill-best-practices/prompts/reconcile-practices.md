# Route: reconcile-practices

Compare current source claims with the existing corpus.

1. Load the prior practice index and relevant thematic files.
2. Map every material rule to supporting source IDs and locators.
3. Classify each as `supported`, `changed`, `new`, `conflict`, `deprecated`, `unverified`, or `exemplar-only`.
4. Apply authority and platform precedence without erasing lower-tier observations.
5. Detect copied recurrence, host-specific assumptions, expired dynamic facts, and internal contradictions.
6. Propose exact additions, revisions, removals, or scoped exceptions.
7. Decide whether a semantic rebuild is required.

Do not edit the corpus in this route unless the user explicitly combines it with rebuild.
