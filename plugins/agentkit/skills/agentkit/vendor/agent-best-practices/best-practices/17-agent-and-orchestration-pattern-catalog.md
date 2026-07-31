# Каталог паттернов агентов и оркестрации

## Как читать каталог

Паттерн — повторяемое решение задачи в определённом контексте, а не название
фреймворка или универсальная рекомендация. Для каждого применения фиксируйте:

- проблему и силы: качество, задержка, стоимость, риск, параллелизм;
- preconditions и контекст применимости;
- участников, владельца состояния и границы полномочий;
- основной поток, stop conditions и failure path;
- evidence, по которому паттерн считается полезным;
- последствия: новые состояния отказа, стоимость и операционная нагрузка.

Паттерны можно компоновать, но каждый дополнительный цикл и участник должен
закрывать измеримый риск. Академический каталог agent patterns также предлагает
описывать решения через context, forces, solution и consequences
([Agent Design Pattern Catalogue](https://arxiv.org/abs/2405.10467)).

## Уровень 1. Один вызов или один агент

| Паттерн | Когда применять | Контракт | Главный риск |
|---|---|---|---|
| Structured generation | Выход потребляет программа | Схема + validation + repair/fail | Валидная форма при неверном содержании |
| Retrieval-grounded response | Нужны внешние или изменяемые факты | Query → evidence с provenance → ответ | Нерелевантный или отравленный контекст |
| Tool-use loop | Для результата нужны действия | Decide → call → observe → stop | Бесконечный цикл или опасный side effect |
| ReAct | Следующий шаг зависит от наблюдения | Reason → act → observe с бюджетом | Ненужное раскрытие reasoning и drift |
| Plan-and-execute | Задача длинная, но разбиение доступно заранее | Версионируемый plan + checkpoints | Устаревший план продолжают исполнять |
| Generate–verify–repair | Ошибку можно обнаружить формальной проверкой | Candidate → deterministic verifier → bounded repair | «Ремонт» маскирует неверную постановку |
| Reflection | Есть чёткая rubric и полезна самокоррекция | Draft → critique → revision, максимум N | Самоподтверждение и лишняя стоимость |
| Human checkpoint | Решение необратимо или требует суждения | Evidence + варианты + последствия | Формальное одобрение без понимания |
| Bounded autonomy | Допустима локальная самостоятельность | Scope + tools + budget + expiry + escalation | Незаметное расширение полномочий |

### Sense–think–act

Минимальная модель агента: получить наблюдение, выбрать допустимое действие,
выполнить его и оценить новое состояние. Она полезна как runtime primitive, но
сама не задаёт стратегию, память или governance. MUST существовать terminal
condition и лимиты шагов, времени, стоимости и side effects.

### Plan-and-execute

Planner строит проверяемую последовательность или DAG, executor исполняет
готовые узлы. Разделяйте их, когда план нужно проверить до действий или когда
executor должен иметь меньше прав. Разрешайте replan только при зафиксированном
drift, неуспешной проверке или новом evidence; изменения плана сохраняйте как
события, а не перезаписывайте историю.

### Evaluator–optimizer

Producer и evaluator работают по rubric до достижения threshold или бюджета.
Критерии задаются до первой генерации. Для значимого риска evaluator SHOULD
быть независим по контексту, модели, данным или хотя бы prompt; самокритика
producer не считается независимой проверкой. Этот workflow входит в базовые
паттерны Anthropic
([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)).

## Уровень 2. Делегирование субагентам

### Task envelope

Каждая делегация содержит `goal`, `context_refs`, `constraints`, `owned_scope`,
`forbidden_actions`, `deliverables`, `acceptance`, `budget` и `return_schema`.
Это transactional boundary: исполнитель возвращает результат и evidence, а не
продолжает самовольно расширять задачу.

### Context capsule

Субагент получает минимальный самодостаточный пакет: цель, необходимые факты,
ссылки на канонические артефакты, локальные правила и известные решения. Не
копируйте всю историю разговора: большой общий контекст увеличивает coupling,
стоимость и вероятность следовать устаревшей инструкции.

### Manager-as-tools

Главный агент сохраняет владение диалогом и вызывает специалистов как tools.
Подходит, когда нужен единый голос, глобальная политика и синтез. Менеджер MUST
валидировать ответы, потому что успешное завершение вызова не доказывает
правильность результата.

### Handoff

Управление и дальнейший диалог передаются специалисту. Это полезно, когда новый
агент должен непосредственно уточнять доменную задачу. Нужны route history,
максимальная глубина, запрет ping-pong и fallback owner. OpenAI различает
`agents as tools` и handoffs именно по владельцу дальнейшего взаимодействия
([Agents SDK](https://openai.github.io/openai-agents-python/multi_agent/)).

### Fork–join

Оркестратор параллельно запускает независимые подзадачи и объединяет результаты.
До запуска проверяйте independence, write-set и общий bottleneck. Join обязан
обработать partial failure, timeout, duplicate и несовместимые выводы.

Варианты:

- **scatter–gather** — разные источники или аспекты, затем нормализация;
- **map–reduce** — одинаковая операция над разделами, затем ассоциативное
  свёртывание;
- **competing hypotheses** — независимые объяснения и попытки опровержения;
- **candidate ensemble** — несколько решений и отдельный selector;
- **review army** — только релевантные критики, выбранные scope detector.

### Blackboard

Агенты публикуют типизированные claims, evidence и задачи в общем durable store,
не пересылая всё через свободный чат. Blackboard полезен для расследований и
длительной команды, но MUST иметь schema, ownership, conflict policy,
provenance, TTL и compaction. Shared mutable prompt не является blackboard.

### Independent verifier

Исполнитель создаёт результат, verifier проверяет outcome по исходному intent и
прямому evidence. Для высокого риска verifier read-only и не получает summary
исполнителя как единственный источник. Если он исправляет результат, роль
verifier заканчивается и после исправления нужен новый gate.

### Hierarchical delegation

Менеджеры делегируют поддеревьям специалистов, когда плоская координация
перегружена. Ограничьте глубину, fan-out и суммарный бюджет; capability и
permissions могут только сужаться вниз по дереву. Рекурсивная делегация без
глобального task graph создаёт дублирование и потерю ответственности.

## Уровень 3. Оркестраторы

| Паттерн | Решение | Предпочтительная реализация |
|---|---|---|
| Router | Выбрать один capability по типу запроса | Typed classifier + confidence + fallback |
| Supervisor | Назначать шаги и удерживать общий goal | LLM локально, код для budgets и gates |
| Pipeline | Последовательность стабильных преобразований | Workflow-as-code |
| State machine | Явные состояния и разрешённые переходы | Durable deterministic runtime |
| DAG scheduler | Dependencies и параллельные waves | Code + leases + idempotency |
| Dynamic graph | План зависит от наблюдений | Ограниченный LLM planner + validated graph |
| Policy-gated workflow | Side effects зависят от риска | Deterministic policy decision/enforcement |
| Reconciliation controller | Свести desired и observed state | Периодический идемпотентный loop |

### Router

Routing contract включает выбранный маршрут, confidence, признаки решения и
fallback. Проверяйте false-positive triggers, overlapping routes и поведение на
out-of-domain input. При низкой уверенности выбирайте безопасный общий workflow
или запрос уточнения, а не случайного специалиста.

### State machine и DAG

State machine лучше свободного LLM-плана, если процесс повторяем, содержит
approval, деньги, production или долгие ожидания. DAG добавляет параллелизм и
dependencies. Модель MAY предложить узлы, но runtime валидирует типы,
допустимые edges, permissions, cycles и resource limits до исполнения.

### Reconciliation controller

Контроллер регулярно сравнивает desired state с observed state и планирует
минимальное исправление. Подходит для orphan tasks, зависших approvals,
устаревших skill installations и конфигурационного drift. Операция должна быть
идемпотентной, а destructive reconciliation — требовать отдельного gate.

### Policy decision / enforcement split

Policy Decision Point вычисляет решение из проверяемых атрибутов; Policy
Enforcement Point технически блокирует недопустимое действие. LLM может
объяснять правила и классифицировать контекст, но не должна быть единственным
enforcement-механизмом.

## Уровень 4. Команды агентов

### Lead + specialists

Lead владеет mission, task graph и интеграцией; специалисты — непересекающимися
deliverables. Это default team pattern. Lead не должен становиться bottleneck:
стандартизируйте status/evidence и разрешайте прямую peer-коммуникацию только
для явных interfaces.

### Cross-functional pod

Небольшая команда покрывает intent, domain, build, verification и operations
одного bounded outcome. Pod эффективнее функционального «пула», когда может
завершить vertical slice без fine-grained внешней координации. Это согласуется
с DORA-практикой loosely coupled teams
([DORA](https://dora.dev/capabilities/loosely-coupled-teams/)).

### Driver–navigator

Driver создаёт артефакт, navigator непрерывно проверяет направление, риски и
следующий шаг. Роли меняются только на checkpoint. Паттерн полезен для сложной
миграции или debugging, но navigator не заменяет независимый финальный review.

### Producer–critic / red–blue

Producer предлагает решение, critic ищет опровержения и misuse cases. Для
security red team не должна иметь production credentials; blue team владеет
mitigations, а независимый gate подтверждает остаточный риск.

### Debate / jury

Участники сначала формируют независимые позиции, затем обмениваются evidence;
judge применяет заранее заданную rubric. Используйте только если разнообразие
гипотез улучшает evals. Большинство голосов не превращает неподтверждённый факт
в истинный.

### Contract-net / bidding

Оркестратор публикует task envelope, подходящие агенты отвечают capability,
стоимостью, сроком и confidence, затем policy выбирает исполнителя. Полезно в
гетерогенной среде; опасно, если self-reported confidence не откалиброван.

### Choreography

Участники реагируют на типизированные события без центрального пошагового
дирижёра. Это снижает центральный bottleneck, но усложняет глобальную картину,
порядок и compensation. Для high-impact процесса сохраняйте accountable owner,
correlation ID и наблюдаемую process projection.

## Паттерны безопасности и надёжности

- **Least-privilege envelope** — временные права только на конкретную задачу.
- **Write-set partitioning** — один активный writer на файл/ресурс/aggregate.
- **Sandbox per worker** — процессная/контейнерная граница для недоверенного кода.
- **Worktree per worker** — изоляция изменений; не security boundary.
- **Idempotency key** — повторная доставка не дублирует side effect.
- **Lease + heartbeat** — временное владение и обнаружение orphan worker.
- **Circuit breaker** — прекращает вызовы деградировавшего capability.
- **Bulkhead** — отдельные очереди/бюджеты ограничивают blast radius.
- **Backpressure** — intake замедляется раньше, чем рушится downstream.
- **Retry budget** — ограниченные повторы только transient failure с jitter.
- **Dead-letter state** — неисправимая задача сохраняется с evidence.
- **Saga** — длинный workflow имеет compensation для каждого принятого шага.
- **Checkpoint/resume** — durable state позволяет безопасно продолжить после сбоя.
- **Canary/shadow** — новая версия сравнивается на ограниченном трафике.

## Антипаттерны

| Антипаттерн | Почему ломается | Замена |
|---|---|---|
| Recursive swarm | Неограниченные cost, depth и duplicate work | Bounded task graph |
| Chat as database | Нет schema, consistency и replay | Durable state + event log |
| Shared mutable context | Stale reads и неявные конфликты | Versioned artifacts |
| Everyone can write everything | Merge conflicts и неясное владение | Write-set + merge owner |
| Author is sole judge | Confirmation bias | Independent verifier |
| Infinite reflection | Нет нового evidence | Bounded loop + external check |
| Routing by labels only | Overlap и prompt gaming | Evals + confidence + fallback |
| Deep handoff chain | Потеря intent и ответственности | Route limit + accountable owner |
| Consensus as truth | Коррелированные ошибки | Source/evidence adjudication |
| LLM as policy engine | Недетерминированный enforcement | PDP/PEP split |

## Минимальная запись решения о паттерне

```yaml
pattern: fork-join-with-independent-verifier
problem: проверить релиз по четырём независимым аспектам
forces: [latency, independence, security]
participants: [orchestrator, qa, security, reliability, verifier]
state_owner: orchestrator
write_sets: none
stop_conditions: [all_terminal, deadline, budget_exhausted]
failure_policy: partial_results_then_escalate
evidence: eval/release-review-v3
consequences:
  positive: shorter_review_latency
  negative: higher_cost_and_synthesis_complexity
```
