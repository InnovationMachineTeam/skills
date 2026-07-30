# Мастер-промпт размещения agent capability

Запускай после task/capability graph и до создания agent skill или command.
Цель — выбрать минимальную форму и не раздувать public skill catalog.

## Вход

Получишь capability contract, intended consumers, owner agent, triggers,
resources, tools, state, risk, eval needs, target hosts, public/private roots,
registry/map и mutation authority. Если owner или consumers materially unclear,
задай один–три focused questions.

## Решение

Выбери ровно одно:

- `INLINE` — короткое стабильное правило без resources/tests/lifecycle;
- `PRIVATE_COMMAND` — один agent, узкое named действие или template;
- `PRIVATE_SKILL` — один agent, reusable multi-step capability с resources,
  scripts или evals;
- `PUBLIC_SKILL` — два independent consumers либо independent owner/contract/
  release lifecycle;
- `TOOL_SCRIPT` — deterministic execution является главным constraint;
- `WORKFLOW` — durable stages/state/coordination являются главным constraint;
- `USE_EXISTING` или `REJECT`.

Обоснуй, почему следующая более простая форма недостаточна. Similar wording,
prompt length или желание «разложить по папкам» сами по себе не оправдывают
skill.

## Placement и visibility

```text
.agents/skills/<skill>/                         # public project skill
.agents/definitions/<agent>/skills/<skill>/    # private agent skill
.agents/definitions/<agent>/commands/<name>.md # private agent command
```

Marketplace public skills могут находиться в `skills/<category>/<skill>/`.
Private root никогда не добавляется в global discovery. Private означает scope
использования; repository permissions и runtime policy отдельно отвечают за
confidentiality.

## Выход

Верни decision, rationale, owner/consumers, primary archetype when applicable,
canonical path, registry/map effect, agent-version effect, required evals,
loader rule и следующий prompt:

- private command → `agent-private-command.md`;
- private/public skill → primary archetype prompt +
  `agent-private-skill.md` when private;
- promotion/demotion → `agent-skill-visibility-migration.md`.
