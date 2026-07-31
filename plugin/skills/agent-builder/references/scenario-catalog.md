# Scenario catalogue

| Scenario | Flow |
|---|---|
| `full-lifecycle` | scout → context as needed → architect → evaluator → repair/optimize as needed → evaluator → manager |
| `create-from-spec` | architect → evaluator → optional manager |
| `research-to-agent` | context → architect → evaluator |
| `evaluate-agent` | evaluator only |
| `repair-agent` | doctor → evaluator → optional manager |
| `optimize-agent` | evaluator baseline → optimizer → evaluator compare |
| `compare-and-refactor` | context → refactor → evaluator → manager |
| `incident-recovery` | doctor → recovery gate → manager → post-incident evaluator |
| `portfolio-governance` | manager inventory → bounded specialist → manager verify |
| `resume` | restore state → verify drift → first valid incomplete phase |

Do not blend scenarios into a mega-flow. Team routes belong to
`agent-team-manager`; platform routes belong to Agentic OS skills.
