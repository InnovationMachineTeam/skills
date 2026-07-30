# Мастер-промпт private agent command

Применяй после решения `PRIVATE_COMMAND`. Command оправдан, если один agent
получает узкое named действие/template, но отдельные resources, scripts, routing
description и release lifecycle полноценного skill не нужны.

## Создание

Создай `.agents/definitions/<agent-id>/commands/<command>.md` с purpose,
arguments, preconditions, allowed tools/effects, procedure, output contract,
failure/stop behavior и examples. Зарегистрируй command в agent definition и в
`docs/AGENT-ASSET-REGISTRY.json` с technical owner, accountable human/team
owner, `revision`, hash, `visibility: private`, единственным allowed consumer и
`parent_version_ref`, равным точной версии owner agent. Command не получает
самостоятельный SemVer. Обнови `docs/AGENT-SKILLS-MAP.json` в той же
revision-checked транзакции.

Command не должен:

- становиться globally discoverable;
- неявно расширять permissions agent;
- дублировать complex reusable capability, которой нужен private skill;
- хранить credentials, durable state или скрытые side effects.

## Проверка

Проверь argument validation, owner invocation, unauthorized-agent denial,
global non-discovery, output/failure behavior, registry/hash parity и removal
rollback. Если command растёт до нескольких workflows/resources/evals, останови
создание и верни decision `PRIVATE_SKILL`.
