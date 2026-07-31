# Retrieval and projections

Progressive retrieval starts at a map/index, filters scope, status, freshness,
data class and consumer, then loads only relevant canonical pages and evidence.
A context capsule cites exact IDs/versions and reports conflicts or staleness.

Projection levels:

1. Markdown, metadata and exact/full-text search.
2. Generated JSON graph with typed nodes/edges and source hashes.
3. Vector index only after measured semantic-retrieval failures.
4. Graph database plus vector hybrid only for measured multi-hop needs.

Every derived record carries source locator, revision/hash and generation time.
Deletion propagates as a tombstone or full rebuild. Projection drift is a test
failure. Similarity and graph paths aid discovery but never replace source
verification.
