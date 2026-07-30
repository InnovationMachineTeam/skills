# Evaluation artifact contracts

Use JSON for machine-consumed state and Markdown only for human summaries. Preserve stable IDs and source/run hashes.

## Evaluation plan

```json
{
  "schema_version": "1.0",
  "evaluation_id": "skill-v2-release-eval",
  "objective": "Decide whether v2 is releasable",
  "risk": "high",
  "target": {"identity": "skill@2.0.0", "hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
  "environment": {"host": "codex", "model": "record-exact-id", "runtime": "python-3.12"},
  "authority": {"read": true, "write": false, "external": false},
  "layers": ["routing", "behavior", "scripts-tools", "security-authority"],
  "baselines": ["skill@1.0.0"],
  "metrics": ["routing-precision", "routing-recall", "behavior-pass-rate"],
  "datasets": ["routing-v1", "behavior-v1", "scripts-v1"],
  "graders": ["deterministic-assertions", "calibrated-rubric-v1"],
  "repetitions": 3,
  "timeouts": {"max_case_seconds": 30},
  "budget": {"max_runs": 60, "max_seconds": 1200, "max_cost": 10},
  "acceptance": {
    "blocking_layers": ["behavior", "security-authority"],
    "criteria": {
      "routing": {"min_precision": 0.9, "min_recall": 0.9},
      "behavior": {"min_pass_rate": 0.95},
      "scripts-tools": "all blocking cases pass",
      "security-authority": "all cases pass"
    }
  },
  "holdout_policy": {"protected": true, "exposure_rule": "Expose only after candidate and gates are frozen; rotate after exposure."},
  "artifacts": {"raw_output_dir": "work/eval-runs/skill-v2"},
  "execution_policy": {
    "side_effects": "read-only isolated fixtures",
    "abort_conditions": ["unexpected external write", "credential request", "budget exceeded"],
    "cleanup": "remove only evaluator-created temporary fixtures after artifact capture"
  }
}
```

Every selected layer needs an explicit acceptance criterion. Record `NOT_EVALUATED` in the run report for intentionally excluded evidence rather than silently omitting a declared layer.

## Evaluation datasets

- `routing.json`: `id`, `input`, boolean `expected_trigger`, `expected_action`, `split`, and optional neighbor/tags. These are the trigger fixtures.
- `behavior.json`: `id`, `request` or `input`, `expected_properties`, `forbidden_properties`, `split`, and optional grader/tags.
- `scripts.json`: `id`, `script`, an array of string `args`, integer `expected_exit`, `side_effect_policy`, `split`, and optional fixture/timeout/assertions.

Use `train`, `validation`, or public `regression` for answer-bearing bundled cases. Use `holdout` only when the expected answers are access-controlled outside the candidate/optimizer context; otherwise declare an `external-protected` holdout policy and keep those cases out of the bundle. Keep duplicate or derived cases in one split family to prevent lineage leakage.

## Normalized run report

```json
{
  "schema_version": "1.0",
  "run_id": "candidate-2026-07-30T12:00:00Z",
  "evaluation_revision": "eval-v1",
  "environment_id": "codex-model-tools-runtime-v1",
  "target_hash": "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "metrics": {"routing_recall": 0.94, "latency_ms": 420},
  "cases": [
    {"id": "route-positive-01", "layer": "routing", "verdict": "PASS"},
    {"id": "no-exfiltration-01", "layer": "security-authority", "verdict": "PASS"}
  ]
}
```

Allowed case verdicts are `PASS`, `FAIL`, `INCONCLUSIVE`, `BLOCKED`, and `NOT_EVALUATED`. Store raw prompts, outputs, logs, files, grader traces, timings, and side effects outside this normalized summary and link them from the human report.
