# Performance and Context-Cost Optimization Prompt

Apply after [base.md](base.md). Reduce tokens, latency, tool calls, retries, or monetary cost after correctness and safety are established.

## Diagnose

- Measure loaded context per request, not only bundle size.
- Trace repeated reads, redundant tool calls, unnecessary delegation, oversized outputs, retry amplification, and scripts replaced by free-form reasoning.
- Separate cold-start, steady-state, and failure-path cost.

## Optimize

- Load resources conditionally, cache only safe stable results, batch independent reads, and use scripts for repeated deterministic work.
- Remove redundant prose and duplicate rules.
- Bound searches, loops, retries, and fan-out based on diminishing information gain.
- Keep output proportional to the user request.

## Guardrails

Maintain correctness, safety, routing, verification, and recoverability. Do not hide failures or skip necessary evidence to improve averages. Report absolute and relative changes with comparable workloads.
