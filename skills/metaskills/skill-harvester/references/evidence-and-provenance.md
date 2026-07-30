# Evidence and Provenance

## Source identity

Record an explicit path, URL, repository and revision, document identifier, artifact hash, or trace ID. A filename alone is not stable identity. Resolve local paths and preserve a deterministic content hash where practical.

## Locator

Use the narrowest durable locator available: file plus heading, symbol, JSON pointer, test ID, commit, page, or line number. Locators should let another reviewer reproduce the observation without searching the whole corpus.

## Evidence levels

- `verified`: directly observed and independently checked against the cited source.
- `supported`: directly observed with a precise locator but not independently checked.
- `inferred`: reasoned from evidence; label the inference and assumptions.
- `speculative`: plausible but weakly supported; normally route to research rather than adoption.

Confidence is not maturity. High confidence that a pattern exists does not mean it is portable or useful.

## Lineage and independence

Track whether sources are original, forks, generated copies, vendored packages, or derived summaries. Repetition across clones is not independent corroboration. Prefer primary artifacts over summaries when available.

## Rights and attribution

Record known license, owner, confidentiality, permitted use, attribution, and transformation requirements. Use `unknown` when evidence is absent. Unknown rights block verbatim reuse and may block redistribution; they do not justify guessing.

## Evidence ledger

For each candidate, preserve source reference, locator, observation, transformation, and reviewer checks. Never invent a license, author, revision, result, or source relationship.
