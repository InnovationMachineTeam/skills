# Мастер-промпт навыка `agent-scout`

Применяй после [agent-skill-base.md](agent-skill-base.md). Создай skill, который
находит и приоритизирует обоснованные возможности для agents и agent-oriented
skills, но ничего не создаёт и не активирует.

## Capability boundary

Skill должен отвечать на вопрос: «какой минимальный механизм стоит создать или
переиспользовать для этого повторяющегося outcome?» Он не проектирует candidate,
не пишет production prompts и не устанавливает assets.

## Source routes

Поддержи минимально необходимые routes:

- session/task insights;
- repository/workflow mining;
- incident/support/task history;
- portfolio gap analysis;
- supplied article/document/corpus;
- explicit idea assessment.

Source scope всегда явный. Не считай private session history доступной без
переданного export или host authorization. Удаляй secrets/PII из evidence.

## Decision taxonomy

Для каждой opportunity верни ровно одно решение:

- `USE_CODE_OR_WORKFLOW`;
- `USE_EXISTING_AGENT`;
- `EXTEND_EXISTING_AGENT`;
- `CREATE_NEW_AGENT`;
- `CREATE_AGENT_SKILL`;
- `KEEP_HUMAN`;
- `KEEP_AD_HOC`;
- `RESEARCH`;
- `REJECT`.

Не смешивай решение о создании agent и skill: agent выполняет runtime mission,
agent-oriented skill управляет его design/evaluation/lifecycle.

## Worth model

Оцени:

- frequency и recurring pain;
- value и measurable outcome;
- variability/uncertainty, требующие agent reasoning;
- decomposability и need for tools/state;
- existing coverage и extension cost;
- side-effect risk и human judgment;
- data/access availability;
- evaluation feasibility;
- ownership, maintenance и retirement cost;
- более простой alternative.

Не выдавай численный score без evidence. Используй score только для ranking
после hard gates: safety, authority, no owner или no evaluation path могут
заблокировать рекомендацию.

## Required artifacts

```yaml
opportunity_id: stable-id
evidence: []
problem: observable recurring problem
users: []
candidate_outcome: measurable outcome
alternatives: []
existing_coverage: []
decision: RESEARCH
rationale: concise evidence-backed reason
risk_tier: R1
context_needed: []
evaluation_path: []
owner_candidate: null
next_handoff: agent-context
confidence: low
```

## Evaluation

Создай positive/negative routing cases и проверяй:

- не предлагает agent для deterministic script;
- находит существующее coverage до `CREATE_NEW_AGENT`;
- различает runtime agent и agent-oriented skill;
- не считает одну встречу recurring workflow;
- сохраняет uncertainty и recommends research при пробелах;
- не извлекает private/sensitive evidence без authority;
- допускает успешный terminal outcome «ничего не создавать».

## Handoff

Для каждой оправданной agent opportunity укажи, какие canonical documents и
decision records потребуются, но не создавай дерево `docs/`. Передавай это как
input в [agent-documentation-contract.md](agent-documentation-contract.md).

Передавай approved opportunity в `agent-context` при недостатке evidence или в
`agent-architect` при готовом intent. Handoff содержит objective, sources,
constraints, alternatives, risk, preserved systems и unresolved questions.
