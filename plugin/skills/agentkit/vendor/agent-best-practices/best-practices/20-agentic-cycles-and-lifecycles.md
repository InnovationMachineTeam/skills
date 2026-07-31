# Циклы и lifecycle для агентных систем

## Цикл и lifecycle — разные вещи

- **Цикл управления** повторяет наблюдение, решение и действие во время работы.
- **Цикл улучшения** меняет качество процесса или продукта между итерациями.
- **Lifecycle** определяет состояния сущности от замысла до вывода из эксплуатации.
- **Gate** принимает решение о переходе, но сам по себе не является циклом.

Не выбирайте один «лучший» цикл для всего. Задайте один основной цикл на каждом
уровне и явные сигналы между уровнями. Иначе система бесконечно «рефлексирует»
внутри шага, пока внешний процесс ждёт проверяемый результат.

## Runtime micro-loops

### Sense–think–act

```text
sense → interpret/decide → act → observe result → stop or repeat
```

Минимальный tool-using loop. Применяйте для bounded execution в стабильной
среде. Требуются budgets, permitted actions, observation schema и terminal
condition. Если действие дорого или необратимо, перед `act` вставляется policy
gate.

### ReAct

Чередует локальное рассуждение и получение новых наблюдений. Подходит, когда
невозможно спланировать весь путь заранее. Не храните скрытое reasoning как
каноническое evidence: в trace нужны decision summary, input/output tools и
проверяемые основания.

### OODA

```text
Observe → Orient → Decide → Act ↺
```

Полезен для incidents, adversarial security, переговоров и быстро меняющейся
среды. `Orient` — не украшение: здесь обновляются модель мира, assumptions,
priorities и возможные действия. При слабой orientation ускорение только быстрее
масштабирует ошибку; Air University отдельно подчёркивает ценность осознанного
анализа на начальных стадиях
([OODA overview](https://www.airuniversity.af.edu/AFCLC/News/Article-Display/Article/1777083/cultural-ksas-skill-development-using-the-ooda-loop/)).

### MAPE-K

```text
Monitor → Analyze → Plan → Execute
     ↖──── shared Knowledge ────↗
```

Подходит для Agent OS operations: health, cost, queue, drift, self-healing и
reconciliation. Monitor собирает signals, Analyze диагностирует, Plan выбирает
коррекцию, Execute действует через effectors, а Knowledge хранит модели,
policies и историю. Sensors/effectors и managed element должны быть отделены от
controller
([IBM](https://dominoweb.draco.res.ibm.com/reports/h-0219.pdf)).

### Generate–evaluate–improve

Producer создаёт candidate, evaluator применяет фиксированную rubric, затем
producer делает bounded revision. Используйте для текстов, планов, кода и skill
artifacts, когда критерии формализуемы. Заканчивайте по pass threshold, отсутствию
измеримого улучшения, лимиту попыток или необходимости human judgment.

## Циклы разработки и поставки

### PDCA

```text
Plan → Do → Check → Act ↺
```

PDCA полезен для контролируемого улучшения repeatable process: спланировать
изменение и критерий, выполнить малый эксперимент, проверить фактический эффект,
стандартизировать/скорректировать. ASQ описывает его как повторяемый
четырёхшаговый подход к изменениям и continuous improvement
([ASQ](https://asq.org/quality-resources/pdca-cycle)).

Для agents:

- Plan — hypothesis, baseline, evals и risk envelope;
- Do — candidate version или ограниченный experiment;
- Check — независимое сравнение quality/safety/cost/latency;
- Act — promote, revise или abandon плюс обновление стандарта.

### Build–measure–learn

```text
hypothesis → build smallest experiment → measure behavior → learn/pivot/persevere
```

Используйте в discovery, когда неизвестно, нужен ли продукт/agent/skill и какую
ценность он создаёт. Measure должен проверять поведение и outcome, а не объём
созданных артефактов. Lean Startup определяет цикл как превращение идей в
продукты, измерение реакции и решение pivot/persevere
([Lean Startup](https://theleanstartup.com/principles)).

### Test-driven и eval-driven development

```text
case/rubric → baseline failure → smallest change → pass → refactor → regression
```

TDD подходит к deterministic code/scripts. Eval-driven development расширяет
его на вероятностные agents/skills:

1. Сохранить representative и adversarial cases до изменения.
2. Зафиксировать baseline с повторными прогонами и confidence interval.
3. Изменить один осмысленный factor.
4. Сравнить quality, safety, latency и cost, не только aggregate score.
5. Разобрать regressions и variance.
6. Прогнать shadow/canary перед promotion.
7. Добавить production failures как новые cases без утечки test answers в prompt.

DORA связывает continuous delivery с быстрым feedback, small batches,
continuous testing, observability и deployable state
([Continuous delivery](https://dora.dev/capabilities/continuous-delivery/)).

### ADLC

ADLC задаёт шесть concurrent modes: Intent, Generate, Validate, Govern, Deploy и
Observe. Это не waterfall: validation, governance и observation присутствуют
на протяжении работы, а человек управляет bets и high-impact решениями
([ADLC](https://www.adlc.io/)).

Практическое отображение:

| Mode | Главный вопрос | Обязательный артефакт |
|---|---|---|
| Intent | Какой outcome и почему? | intent/bet record |
| Generate | Что создаём или изменяем? | candidate artifacts |
| Validate | Работает ли и где ломается? | eval evidence |
| Govern | Допустимы ли риск и полномочия? | policy decision/approval |
| Deploy | Как безопасно ввести изменение? | release/rollback plan |
| Observe | Что происходит в реальности? | linked production signals |

## Циклы обучения

### Single-loop learning

Исправляет действие, чтобы достичь неизменной цели: изменить prompt, threshold,
route или tool. Подходит для локальной оптимизации, если intent и policy всё ещё
верны.

### Double-loop learning

Проверяет также исходные цели, правила и assumptions: нужен ли вообще агент,
верна ли metric, допустим ли autonomy level, не оптимизируем ли proxy. Этот
подход связан с работой Криса Арджириса о double-loop learning
([Harvard Business Review](https://hbr.org/1977/09/double-loop-learning-in-organizations)).

Запускайте double loop при повторяющемся классе отказов, gaming metric,
неожиданном вреде, смене контекста или устойчивом отсутствии ценности. Изменение
policy/intent требует accountable human, а не самовольной «эволюции» агента.

### After-action review

После значимого run или инцидента ответьте:

1. Что ожидалось и почему?
2. Что произошло по trace/evidence?
3. Где расходятся модель и реальность?
4. Что оставить, изменить или прекратить?
5. Кто владеет action, сроком и проверкой эффекта?

Learning не завершён, пока action не попал в backlog/eval/runbook и не имеет
owner. Memory update без проверки — не learning, а накопление шума.

## Governance и risk cycles

### NIST AI RMF

Govern — сквозная функция; Map, Measure и Manage применяются итеративно, а не как
жёсткая последовательность. NIST подчёркивает continuous risk management,
независимую проверку, роли, inventory и безопасный decommissioning
([AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)).

| Function | Применение к agents/skills |
|---|---|
| Govern | policy, owners, inventory, training, risk tier, retirement |
| Map | intent, context, stakeholders, misuse, dependencies, impacts |
| Measure | evals, uncertainty, controls, production monitoring |
| Manage | prioritize, mitigate/accept/avoid/transfer, respond and recover |

### Security lifecycle

```text
scope → threat model → prevent → verify → detect → respond → recover → learn
```

Threat model обновляется при новом tool, data source, autonomy, cross-agent
protocol или deployment boundary. Security verification идёт до release, а
detection/recovery — после. Prompt injection считается untrusted input problem,
а не отдельным разовым test case.

### Incident lifecycle

```text
detect → triage → contain → diagnose → remediate → recover → review
```

OODA управляет быстрыми решениями внутри инцидента, MAPE-K — автоматическими
операционными контроллерами, incident lifecycle — ответственностью и переходами.
Не смешивайте containment с root-cause fix: сначала ограничьте blast radius,
затем докажите причину.

### Release lifecycle

```text
candidate → offline eval → shadow → canary → progressive rollout
          → promote | pause | rollback → observation window
```

Promotion criteria и rollback triggers задаются до canary. Для skill/agent
обновления сохраняются точные versions модели, prompt, references, scripts,
tools, policies и eval dataset.

## Lifecycle сущностей

### Agent

```text
discover need → design contract → prototype → evaluate → approve → publish
→ activate → observe → improve → deprecate → retire
```

### Skill

```text
scout/harvest → architect → create → validate/evaluate → package → publish
→ install/activate → observe → optimize/doctor → upgrade → deprecate → retire
```

### Workflow

```text
model process → specify states/contracts → simulate → verify failures
→ publish → run → reconcile → evolve/migrate → retire
```

### Memory item

```text
candidate → verify provenance → classify/scope → approve → retrieve/use
→ refresh/expire → supersede/delete/archive
```

### Tool/integration

```text
assess → threat model → adapter contract → sandbox test → authorize → observe
→ rotate credentials/update → revoke → retire
```

Каждое состояние имеет owner, entry evidence, allowed actions, exit gate,
maximum age и recovery path. `Deprecated` — активная миграционная фаза, а не
вечная метка.

## Вложенная модель циклов

```text
Governance: NIST AI RMF / double-loop       cadence: quarter or major change
Product:    Build–Measure–Learn             cadence: bet/experiment
Delivery:   ADLC + eval-driven development  cadence: change/release
Runtime:    ReAct or OODA                   cadence: step/decision
Operations: MAPE-K                         cadence: seconds to hours
Incident:   response lifecycle              cadence: event
Improvement: PDCA / after-action review     cadence: release or period
```

Сигнал поднимается наружу, если внутренний цикл исчерпал бюджет, требует смены
цели/policy, обнаружил новый high-impact risk или не может восстановить
инвариант. Внешний цикл не должен микроменеджерить каждый tool call.

## Как выбрать цикл

| Ситуация | Основной цикл | Необходимое дополнение |
|---|---|---|
| Локальное tool use | Sense–think–act / ReAct | budgets + action gate |
| Быстро меняющаяся угроза | OODA | human commander + audit |
| Self-healing runtime | MAPE-K | deterministic effectors + SLO |
| Улучшение стабильного процесса | PDCA | baseline + owner |
| Неизвестная ценность/решение | Build–measure–learn | customer evidence |
| Создание или upgrade агента | ADLC + eval-driven | governance + canary |
| Повторяющийся системный провал | Double-loop | accountable policy review |
| Production incident | Incident lifecycle | OODA внутри, AAR после |

## Cycle anti-patterns

- цикл без stop condition, owner или budget;
- Check/Evaluate выполняет тот же контекст без внешнего evidence;
- Plan бесконечно уточняется без experiment;
- Measure собирает доступные метрики, не связанные с outcome;
- Learn автоматически переписывает policy или долговременную память;
- runtime reflection используется вместо deterministic validation;
- все циклы превращены в последовательный waterfall;
- improvement action не имеет срока и проверки эффекта;
- lifecycle заканчивается `active`, без deprecation и retirement.
