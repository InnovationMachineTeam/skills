# Practice rebuild contract

## Required thematic files

The corpus manifest declares these canonical topics:

1. specification and portability;
2. authoring and progressive disclosure;
3. descriptions, discovery, and routing;
4. workflows, scripts, and tools;
5. evaluation and optimization;
6. security and authority;
7. client implementation and context lifecycle;
8. enterprise lifecycle and governance;
9. meta-skills and orchestration;
10. conflicts and unified decisions;
11. checklists.

## File contract

Every thematic file starts with:

```text
Practice-ID: BP-...
Scope: portable|platform|enterprise|exemplar|mixed
Status: current
Sources: SRC-..., SRC-...
Last-rebuilt: YYYY-MM-DD
```

Use stable practice IDs so semantic comparison survives prose edits. Keep one canonical owner for each rule. Cross-reference topics instead of duplicating normative wording.

`claims.json` covers the preamble and every level-two section, or the whole document when a file has no such sections. Each record binds one canonical owner, registered source IDs, and the exact text hash. Any prose change requires a corresponding provenance review and manifest update.

## Staging and replacement

1. Build a fresh directory.
2. Validate required files, index coverage, section provenance, exact section hashes, source IDs, and duplicate owners.
3. Compare semantic manifests and human-readable diff.
4. Preserve the previous corpus as last-known-good.
5. Replace only the authorized review copy.
6. Use manager-controlled versioning for installed copies.

## Material change

A change is material when it alters accepted syntax, trigger behavior, required workflow, authority, security, validation, platform support, lifecycle, or a recommendation that could change a managed skill. Editorial rewording, navigation changes, volatile popularity, and non-practice repository activity are not material by themselves.
