# Master Prompt For The `agent-best-practices` Skill

Apply after [agent-skill-base.md](agent-skill-base.md). Create a skill that
maintains an evidence-linked, updateable corpus of best practices for agents,
subagents, orchestration, teams, Agent OS, and agent-oriented skills.

## Capability boundary

The skill supports query, audit, refresh, reconcile, rebuild, and generate-change-prompt.
It does not become an open-ended harvester, does not rewrite active agents, and
does not turn a vendor example into a normative rule.

## Source registry

For each source, store a stable ID, title, locator, publisher, authority tier,
scope, source type, update method, status, last checked, summary, and principal
findings. Separate:

- normative protocols/specifications;
- official platform documentation;
- official engineering guidance;
- standards/risk/operations frameworks;
- research pattern catalogues;
- version-pinned implementations;
- local derived practices.

A platform fact does not become a universal MUST. An implementation pattern is
not the same as a standard. Every claim must have source IDs, platform scope,
status, revision, and last rebuilt.

## Routes

- `query` — answer/checklist from the current corpus;
- `source-audit` — freshness/status without rebuild;
- `refresh` — fetch changed sources into staging;
- `reconcile` — compare claims, conflicts, and supersession;
- `rebuild` — atomically rebuild thematic files;
- `apply` — audit a candidate agent/skill against practices;
- `change-prompt` — create a master prompt for updating the managed portfolio.

## Reconciliation

For each new/changed claim, choose:

- confirms existing;
- narrows platform/version scope;
- extends practice;
- supersedes;
- conflicts as fact;
- represents a trade-off;
- insufficient evidence.

A fact conflict blocks the rebuild until resolution. A trade-off preserves
alternatives and selection forces. Do not hide removed/deprecated platform behavior.

## Corpus themes

Minimum themes:

- foundations and selection;
- agent contracts and patterns;
- delegation/orchestration/teams;
- Agent OS/runtime/state/memory;
- security/authority/governance;
- evals/optimization;
- cycles/lifecycle/roles;
- operations/observability/incidents;
- documentation and artifact contracts;
- agent-oriented skill design;
- conflicts/decisions/checklists.

## Safe rebuild

Documentation claims must conform to
[agent-documentation-contract.md](agent-documentation-contract.md), including
subject-first decisions, on-demand directories, and explicit ownership.

Fetch/parse in staging, preserve snapshots/hashes, validate registry and claim
links, build complete candidate corpus, compare semantic sections, run routing
and behavior evals, then replace only authorized target. If nothing changed,
report current without rewriting files.

## Managed portfolio prompt

The generated change prompt lists exact managed assets/versions, applicable
practice deltas, required diffs, evals, migration, and rollback. It creates
candidate changes; publication/activation remains separate.
