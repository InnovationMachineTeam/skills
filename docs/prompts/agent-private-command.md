# Мастер-промпт private agent command

Применяй после решения `PRIVATE_COMMAND`. Command оправдан, если один agent
получает узкое named действие/template, но отдельные resources, scripts, routing
description и release lifecycle полноценного skill не нужны.

## Создание

Создай `.agents/definitions/<agent-id>/commands/<command>.md` с purpose,
arguments, preconditions, allowed tools/effects, procedure, output contract,
failure/stop behavior и examples. Зарегистрируй command в agent definition и в
registry extension проекта с owner, version/hash, visibility private и allowed
consumers.

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
