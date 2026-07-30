# Conflicts and unified decisions

Practice-ID: BP-CONFLICT-001
Scope: mixed
Status: current
Sources: SRC-AS-001, SRC-AS-002, SRC-AS-004, SRC-ANT-002, SRC-ANT-003, SRC-OAI-001, SRC-OAI-003, SRC-EX-001, SRC-EX-002, SRC-DER-001
Last-rebuilt: 2026-07-30

| Tension | Unified decision |
|---|---|
| Spec permits optional frontmatter; some hosts prefer only two fields | Keep portable source minimal; emit host metadata in adapters when possible. |
| Strict authoring versus tolerant clients | Use strict producers and diagnostic, non-silent consumers. |
| Evals inside source versus lean runtime bundle | Separate development source and target runtime packaging when the host benefits. |
| Narrow versus broad skills | Start narrow; consolidate only after routing, behavior, permission, and lifecycle evidence. |
| Instructions versus scripts versus MCP | Instructions for variable judgment, scripts for deterministic repetition, MCP/tools for live authenticated capability. |
| Small approval suite versus production benchmark | Use 3–5 smoke cases early; use larger repeated and held-out suites for production claims. |
| Bundle size versus instruction size | Disk bundle may be large; simultaneously loaded context and navigation depth should stay small. |
| Autonomy versus confirmation | Scale autonomy by scope, reversibility, externality, cost, and impact. |
| Production pinning versus current facts | Pin procedures and releases; retrieve dynamic facts from current authoritative sources. |
| Quality review versus tests first | Review the intended behavior before regression tests lock it in, then keep tests as durable gates. |
| Self-updating practice skill versus active integrity | Rebuild a staged reviewable version; manager controls installation and activation. |
| New guidance versus proven target behavior | Perform per-skill applicability analysis; prefer `NO_CHANGE` over mechanical conformance. |

Security and target-host constraints override stylistic consistency. Preserve unresolved conflicts when evidence cannot support one unified rule.
