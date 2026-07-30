# Harvest Output Schema

## Report

A human-readable report should contain scope, source inventory, method, prioritized candidates, evidence table, contradiction clusters, rejected candidates, rights and security constraints, validation gaps, and downstream handoffs.

## Machine-readable manifest

Use JSON with:

```json
{
  "schema_version": "1.0",
  "harvest_id": "stable-run-id",
  "objective": "what will be reused and by whom",
  "sources": [
    {
      "source_id": "src-001",
      "locator": "path, URL, revision, or artifact ID",
      "sha256": "optional lowercase SHA-256",
      "license": "known identifier or unknown",
      "rights_status": "cleared | restricted | unknown",
      "notes": []
    }
  ],
  "candidates": [
    {
      "id": "cand-001",
      "type": "workflow",
      "title": "short name",
      "summary": "generalized reusable statement",
      "evidence": [
        {
          "source_id": "src-001",
          "locator": "SKILL.md#section",
          "observation": "faithful paraphrase"
        }
      ],
      "confidence": "supported",
      "maturity": "observed",
      "decision": "research",
      "assumptions": [],
      "risks": [],
      "validation": ["falsifiable next check"]
    }
  ],
  "contradictions": [],
  "exclusions": [],
  "downstream_handoffs": []
}
```

Allowed candidate types: `trigger`, `workflow`, `knowledge`, `prompt-template`, `script-tool`, `eval-failure`, `safety-governance`, and `anti-pattern`.

Use `scripts/validate_harvest.py` for structural checks. The validator does not verify source truth, licenses, or semantic quality.
