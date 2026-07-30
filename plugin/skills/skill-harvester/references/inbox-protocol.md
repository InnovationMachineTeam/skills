# Inbox Protocol

Use an explicit destination outside source trees:

```text
inbox/
  source-manifest.json
  index.json
  raw/
  extracted/
  sessions/
  web/
  repositories/
  external-skills/
  notes/
  candidates/
  contradictions.md
  open-questions.md
  rounds/
```

Every artifact must map to a source ID, locator, hash or revision when available, rights status, sensitivity, retrieval method, and research round. Do not store secrets or unrelated personal data.

Each round records objective, queries, sources added, candidates changed, contradictions, remaining gaps, and expected value of continuing. `SKILL_CONTEXT.md` is a synthesized deliverable, not a dump of inbox contents.
