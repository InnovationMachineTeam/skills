# Противоречия практик и решения

Большинство расхождений — не фактические противоречия, а разные точки на шкалах
риск/сложность/интерактивность. Ниже зафиксированы решения, чтобы Agent OS не
получила конфликтующие правила.

## Workflow или агент

**Различие:** deterministic workflows предсказуемы; autonomous agents гибки.

**Решение:** код владеет lifecycle, budgets, policies и irreversible gates;
агент решает неоднозначные локальные задачи. Начинать с workflow/single agent,
усложнять по eval evidence.

## Один агент или много

**OpenAI/Anthropic:** сначала максимально простой single-agent.

**Реализации:** GSD/BMAD/gstack активно специализируют роли.

**Решение:** специализация оправдана context isolation, distinct permissions,
tool confusion, independent verification или parallel speedup. Само тематическое
разделение не достаточно.

## Жёсткие фазы или fluid actions

**GSD/BMAD/Spec Kit:** последовательные artifacts и gates.

**OpenSpec/ADLC:** итеративные actions; ADLC modes работают параллельно.

**Решение:** dependencies и assurance gates обязательны, фазовая блокировка —
нет. Artifact graph разрешает возврат и итерацию. Lite/standard/high-assurance
policies выбирают строгость.

## Требования или bets

**Классический SDLC:** требования описывают ожидаемое поведение.

**ADLC:** bets фиксируют неизвестное и resolution signal.

**Решение:** bets применяются до подтверждения проблемы/решения; requirements —
к выбранному generation target и обязательным constraints. Bet trace связывает
learning с последующей spec.

## Thin orchestrator или активный manager

**GSD:** orchestrator не трогает source files.

**Manager pattern:** manager синтезирует и может выполнять часть работы.

**Решение:** orchestrator MUST не дублировать dispatched tasks. Он MAY делать
малые интеграционные операции, если ownership явно закреплён и это не загрязняет
контекст. Default — thin.

## Agents as tools или handoffs

**Различие:** manager сохраняет user-facing ownership; handoff отдаёт его
специалисту.

**Решение:** agents-as-tools для bounded subtasks и единого ответа; handoff для
полного владения следующим этапом. Route history и max transitions обязательны.

## Команда или параллельные субагенты

**Различие:** команда даёт peer communication; субагенты возвращаются к lead.

**Решение:** если participants не должны координироваться напрямую, fan-out/fan-in
проще. Team только для genuine shared problem-solving/task board.

## Worktree как изоляция

**Маркетинговое восприятие:** отдельный worktree выглядит безопасной средой.

**Платформенные детали:** `.git`, plugins, approvals или credentials могут быть
общими.

**Решение:** worktree = change/collision isolation. Security boundary = sandbox +
identity + filesystem/network policy. Документировать shared resources.

## Память или stateless agents

**Плюс памяти:** continuity и learning.

**Риск:** poisoning, staleness, privacy и скрытая зависимость.

**Решение:** raw sessions не становятся памятью. Candidate → verify → approve;
provenance, scope, TTL, owner и revocation обязательны. Canonical docs/state
приоритетнее memory.

## Ссылаться на standard или копировать

**Ссылка:** остаётся актуальной, но ломает portability/reproducibility.

**Копия:** self-contained, но устаревает.

**Решение:** active workflow читает canonical reference; immutable run/spec
фиксирует version/digest или snapshot. Dependency graph помечает stale copies.

## Markdown state или database

**Markdown:** прозрачен людям, git-friendly.

**DB:** транзакции, concurrency и queries.

**Решение:** canonical structured store для runtime state, Markdown projection
для review. В небольшом single-writer workflow Markdown допустим при schema/
atomic-write/lock checks.

## Автоматические gates или human review

**ADLC:** loops over gates, continuous signals.

**High-assurance:** блокирующие approvals.

**Решение:** automated continuous validation везде; human gate только для
accountability, irreversible/high-impact action и genuine judgment. Он не
повторяет автоматический checklist.

## LLM verifier или deterministic test

**LLM:** видит смысл и coherence.

**Test:** воспроизводим и проверяет observable behavior.

**Решение:** deterministic evidence имеет приоритет; LLM связывает claims,
находит gaps и оценивает judgment cases. Critical pass не основывается только на
LLM.

## Fail-open или fail-closed

**OpenSpec lite:** verification warnings не блокируют archive.

**Security/GSD:** неопределённость часто требует human_needed/block.

**Решение:** policy по risk class. Low reversible — accept-and-flag; high/critical
— fail-closed или accountable approval. Статус никогда не скрывается.

## Полный контекст или прогрессивная загрузка

**Полный контекст:** меньше risk пропуска.

**Progressive disclosure:** меньше context rot/cost.

**Решение:** обязательный compact context spine + индекс; детали retrieval по
релевантности. Critical constraints дублируются в task envelope, но canonical
source сохраняется ссылкой.

## «Boil the ocean» или минимализм

**gstack:** AI снижает marginal cost, стоит делать complete thing.

**Anthropic/GSD Pi/OpenSpec:** complexity и ceremony только по необходимости.

**Решение:** полнота относится к agreed outcome и важным edge cases, а не к
неограниченному scope. Budget, non-goals и diminishing returns ограничивают
работу.

## Численные лимиты платформ

Глубина nesting, число teammates, размер context и inheritance permissions
различаются и меняются.

**Решение:** не встраивать vendor limits в универсальную архитектуру. Хранить
runtime capability matrix и выбирать более строгие внутренние пределы.

## Итоговая policy разрешения новых конфликтов

1. Определить, это факт, trade-off или platform limitation.
2. Сравнить scope, risk tier и дату источников.
3. Предпочесть primary/current official source для факта.
4. Для trade-off использовать eval evidence и reversible default.
5. Для high-impact ambiguity — human decision и ADR.
6. Зафиксировать исключение, owner и review date.
