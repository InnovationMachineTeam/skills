# Мастер-промпт private agent skill

Применяй после `agent-skill-base.md`, одного primary archetype prompt и решения
`PRIVATE_SKILL` из `agent-capability-placement.md`.

## Contract

Создай обычный versioned/tested skill bundle, но размести его в
`.agents/definitions/<agent-id>/skills/<skill>/`. Требуй stable owner agent,
allowed consumers, target host adapter и candidate registry/map update.
Не встраивай secrets или runtime state.

## Registration

Entry содержит identity, name, semantic version, content hash, locator,
`visibility: private`, `scope: agent`, `discoverability: agent_scoped`,
`owner_agent_ref`, `allowed_consumers`, provenance, trust, lifecycle и evidence.
`allowed_consumers` содержит только owner agent; отдельно укажи accountable
human/team owner. Agent definition ссылается на skill через canonical map.
Registry и map обновляются одной revision-checked транзакцией с rollback.
Behavior-changing
skill update увеличивает agent version по compatibility policy.

## Loader и tests

Global discovery исключает `.agents/definitions/*/skills`. Host adapter получает
private root только после выбора approved agent identity. Проверь:

- owner explicit invocation и intended trigger;
- отсутствие в global discovery;
- denial другого agent и missing owner;
- registry/map path/version/hash parity;
- prompt-injection, permissions и resource boundaries;
- rollback и stale adapter detection.

## Завершение

Верни bundle, owner-agent diff, registry/map diff, generated adapters,
validation/eval evidence и lifecycle status. Не называй capability secret и не
активируй её по факту создания файлов.
