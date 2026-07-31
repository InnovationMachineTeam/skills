# Мастер-промпт composite toolkit `agentkit`

Применяй после [agent-skill-base.md](agent-skill-base.md), только когда
independent agent-oriented donor skills уже стабильны и user явно хочет единую
точку входа. Не используй composite как замену правильным boundaries.

## Entry gate

До создания докажи:

- минимум два release cycles donor interfaces;
- versioned donor manifests и reproducible evals;
- реальные user journeys, выигрывающие от единого entry point;
- explicit invocation, не конкурирующая с direct specialists;
- owner и upgrade/release process для pack;
- размер/context/copy cost приемлем.

Если эти условия не выполнены, создай routing design или используй direct
skills, но не vendor snapshots.

## Root contract

Root `SKILL.md` должен быть thin explicit router:

- parse canonical command and aliases;
- select one mode;
- load exactly one donor snapshot;
- preserve donor authority and safety;
- prevent recursion/cycles;
- report donor/version/provenance;
- support native `help`, `route`, `status`, `upgrade`;
- never edit source donors.

Рекомендуемое имя — `agentkit`, если оно не конфликтует с target marketplace.
Не делай generic description, активирующую pack на каждый запрос про agents.

## Suggested modes

Pack сохраняет documentation contract выбранного donor и не создаёт общую
mega-taxonomy `docs/`. `upgrade` обязан сравнивать изменения documentation
interfaces как часть donor compatibility.

| Mode | Donor |
|---|---|
| `scout` | `agent-scout` |
| `context` | `agent-context` |
| `architect` | `agent-architect` |
| `evaluate` | `agent-evaluator` |
| `doctor` | `agent-doctor` |
| `optimize` | `agent-optimizer` |
| `refactor` | `agent-refactor` |
| `manage` | `agent-manager` |
| `run` | `agent-builder` |
| `practices` | `agent-best-practices` |

Expose only installed/locked donors. Unknown mode fails with exact help; no
silent fuzzy route for consequential operations.

## Donor manifest

Для каждого donor фиксируй:

```json
{
  "name": "agent-evaluator",
  "version": "1.0.0",
  "source_commit": "...",
  "tree_sha256": "...",
  "vendored_path": "vendor/agent-evaluator",
  "modes": ["evaluate"],
  "interface_version": 1,
  "transforms": []
}
```

Vendored donor `SKILL.md` переименуй так, чтобы host не discover nested skills,
но сохрани relative resource resolution. Source donors read-only.

## Upgrade

1. Read-only compare versions, hashes and interfaces.
2. If current, exit without rewriting.
3. Missing/invalid donor blocks automatic upgrade.
4. Build complete candidate pack in staging.
5. Review donor, mode, alias and authority diffs.
6. Update integration/routing evals.
7. Run donor validators plus pack-level forward tests.
8. Replace active pack only after explicit target authority.
9. Preserve previous pack as rollback target.

Не fetch/substitute/delete donor by assumption. Major interface change требует
migration decision, а не автоматического copy.

## `run` mode

Перед запуском builder предложи 2–4 viable workflows, gates, mutations и
trade-offs. Рекомендуй один и дождись выбора/подтверждения. После выбора загрузи
только builder donor и соответствующий scenario.

## Evaluation

Проверяй explicit commands, aliases, empty/missing args, collision with direct
skills, absent/stale donors, malicious donor content, recursive routing,
unauthorized mutation, status current/changed/missing, staged upgrade failure,
rollback и context loading only selected donor.
