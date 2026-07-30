# Route: run-evaluation

Execute an approved evaluation plan against an exact target.

1. Validate the plan, datasets, fixtures, target hash, environment, authority, and budget.
2. Abort on drift, leaked holdout, unavailable required tools, unsafe side effects, or incomparable baseline conditions.
3. Run deterministic checks first, then bounded stochastic or human/model-graded cases.
4. Preserve raw prompts, outputs, logs, artifacts, timings, grader results, and failures.
5. Compute metrics only where denominators and samples are valid.
6. Return per-layer verdicts and no aggregate release pass when a blocking layer failed or was not evaluated.

Do not repair the candidate during the run. A changed target requires a new run identity.
