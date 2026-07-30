# Мастер-промпт навыка `agent-best-practices`

Применяй после [agent-skill-base.md](agent-skill-base.md). Создай skill, который
поддерживает evidence-linked, updateable corpus лучших практик agents,
subagents, orchestration, teams, Agent OS и agent-oriented skills.

## Capability boundary

Skill умеет query, audit, refresh, reconcile, rebuild и generate change prompt.
Он не становится open-ended harvester, не переписывает active agents и не
превращает vendor example в normative rule.

## Source registry

Для каждого source храни stable ID, title, locator, publisher, authority tier,
scope, source type, update method, status, last checked, summary и principal
findings. Разделяй:

- normative protocols/specifications;
- official platform documentation;
- official engineering guidance;
- standards/risk/operations frameworks;
- research pattern catalogues;
- version-pinned implementations;
- local derived practices.

Platform fact не становится universal MUST. Implementation pattern не равен
стандарту. У каждого claim должны быть source IDs, platform scope, status,
revision и last rebuilt.

## Routes

- `query` — ответ/checklist из текущего corpus;
- `source-audit` — freshness/status без rebuild;
- `refresh` — получить changed sources в staging;
- `reconcile` — compare claims, conflicts and supersession;
- `rebuild` — атомарно пересоздать thematic files;
- `apply` — audit candidate agent/skill against practices;
- `change-prompt` — создать master prompt для обновления managed portfolio.

## Reconciliation

Для каждого нового/изменённого claim выбери:

- confirms existing;
- narrows platform/version scope;
- extends practice;
- supersedes;
- conflicts as fact;
- represents a trade-off;
- insufficient evidence.

Fact conflict блокирует rebuild до resolution. Trade-off сохраняет alternatives
и selection forces. Не скрывай removed/deprecated platform behavior.

## Corpus themes

Минимальные темы:

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

Fetch/parse в staging, preserve snapshots/hashes, validate registry and claim
links, build complete candidate corpus, compare semantic sections, run routing
and behavior evals, then replace only authorized target. If nothing changed,
report current without rewriting files.

## Managed portfolio prompt

Generated change prompt перечисляет exact managed assets/versions, applicable
practice deltas, required diffs, evals, migration and rollback. Он создаёт
candidate changes; publication/activation remains separate.
