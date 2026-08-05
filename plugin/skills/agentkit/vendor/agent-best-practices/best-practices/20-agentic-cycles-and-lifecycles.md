# Cycles and Lifecycles for Agentic Systems

## A cycle and a lifecycle are different things

- **A control cycle** repeats observation, decision, and action during runtime.
- **An improvement cycle** changes the quality of the process or product between
  iterations.
- **A lifecycle** defines the states of an entity from conception to
  retirement.
- **A gate** decides a transition, but is not itself a cycle.

Do not choose one "best" cycle for everything. Assign one primary cycle at each
level and explicit signals between levels. Otherwise the system will reflect
forever inside a step while the outer process waits for a verifiable result.

## Runtime micro-loops

### Sense-think-act

```text
sense -> interpret/decide -> act -> observe result -> stop or repeat
```

The minimal tool-using loop. Use it for bounded execution in a stable
environment. Budgets, permitted actions, an observation schema, and a terminal
condition are required. If the action is expensive or irreversible, insert a
policy gate before `act`.

### ReAct

Alternates local reasoning with new observations. It fits cases where the full
path cannot be planned in advance. Do not store hidden reasoning as canonical
evidence: the trace should contain the decision summary, tool inputs/outputs,
and verifiable grounds.

### OODA

```text
Observe -> Orient -> Decide -> Act ↺
```

Useful for incidents, adversarial security, negotiation, and rapidly changing
environments. `Orient` is not decoration: this is where the world model,
assumptions, priorities, and available actions are updated. With weak
orientation, speed only scales the error faster; Air University explicitly notes
the value of deliberate analysis in the early stages
([OODA overview](https://www.airuniversity.af.edu/AFCLC/News/Article-Display/Article/1777083/cultural-ksas-skill-development-using-the-ooda-loop/)).

### MAPE-K

```text
Monitor -> Analyze -> Plan -> Execute
     ^---- shared Knowledge ----^
```

Fits Agent OS operations: health, cost, queue, drift, self-healing, and
reconciliation. Monitor gathers signals, Analyze diagnoses, Plan selects a
correction, Execute acts through effectors, and Knowledge stores models,
policies, and history. Sensors/effectors and the managed element should be
separate from the controller
([IBM](https://dominoweb.draco.res.ibm.com/reports/h-0219.pdf)).

### Generate-evaluate-improve

The producer creates a candidate, the evaluator applies a fixed rubric, and the
producer then performs a bounded revision. Use this for text, plans, code, and
skill artifacts when criteria can be formalized. Stop on a pass threshold, lack
of measurable improvement, attempt limit, or need for human judgment.

## Development and delivery cycles

### PDCA

```text
Plan -> Do -> Check -> Act ↺
```

PDCA is useful for controlled improvement of a repeatable process: plan a change
and criterion, run a small experiment, check the actual effect, then
standardize or adjust. ASQ describes it as a repeatable four-step approach to
change and continuous improvement
([ASQ](https://asq.org/quality-resources/pdca-cycle)).

For agents:

- Plan - hypothesis, baseline, evals, and risk envelope;
- Do - candidate version or limited experiment;
- Check - independent comparison of quality/safety/cost/latency;
- Act - promote, revise, or abandon, plus standard update.

### Build-measure-learn

```text
hypothesis -> build smallest experiment -> measure behavior -> learn/pivot/persevere
```

Use in discovery when it is unknown whether a product/agent/skill is needed and
what value it creates. Measurement should verify behavior and outcome, not the
volume of produced artifacts. Lean Startup defines the cycle as turning ideas
into products, measuring reaction, and deciding whether to pivot or persevere
([Lean Startup](https://theleanstartup.com/principles)).

### Test-driven and eval-driven development

```text
case/rubric -> baseline failure -> smallest change -> pass -> refactor -> regression
```

TDD fits deterministic code/scripts. Eval-driven development extends it to
probabilistic agents/skills:

1. Save representative and adversarial cases before changing anything.
2. Record a baseline with repeated runs and a confidence interval.
3. Change one meaningful factor.
4. Compare quality, safety, latency, and cost, not only an aggregate score.
5. Analyze regressions and variance.
6. Run shadow/canary before promotion.
7. Add production failures as new cases without leaking test answers into the
   prompt.

DORA links continuous delivery to fast feedback, small batches, continuous
testing, observability, and deployable state
([Continuous delivery](https://dora.dev/capabilities/continuous-delivery/)).

### ADLC

ADLC defines six concurrent modes: Intent, Generate, Validate, Govern, Deploy,
and Observe. It is not a waterfall: validation, governance, and observation are
present throughout the work, while the human governs bets and high-impact
decisions
([ADLC](https://www.adlc.io/)).

Practical mapping:

| Mode | Primary question | Mandatory artifact |
|---|---|---|
| Intent | What outcome and why? | intent/bet record |
| Generate | What are we creating or changing? | candidate artifacts |
| Validate | Does it work and where does it fail? | eval evidence |
| Govern | Are the risk and authority acceptable? | policy decision/approval |
| Deploy | How is the change introduced safely? | release/rollback plan |
| Observe | What is happening in reality? | linked production signals |

## Learning cycles

### Single-loop learning

Corrects the action to reach an unchanged goal: adjust a prompt, threshold,
route, or tool. It fits local optimization when the intent and policy are still
correct.

### Double-loop learning

Also checks the original goals, rules, and assumptions: is an agent needed at
all, is the metric valid, is the autonomy level acceptable, are we optimizing a
proxy. This approach is linked to Chris Argyris's work on double-loop learning
([Harvard Business Review](https://hbr.org/1977/09/double-loop-learning-in-organizations)).

Trigger double loop on a recurring failure class, metric gaming, unexpected
harm, context shift, or persistent lack of value. Changing policy/intent
requires an accountable human, not unauthorized "agent evolution."

### After-action review

After a significant run or incident, answer:

1. What was expected and why?
2. What happened according to the trace/evidence?
3. Where do the model and reality diverge?
4. What should be kept, changed, or stopped?
5. Who owns the action, deadline, and effect verification?

Learning is not complete until the action enters a backlog/eval/runbook and has
an owner. A memory update without verification is not learning; it is noise
accumulation.

## Governance and risk cycles

### NIST AI RMF

Govern is a cross-cutting function; Map, Measure, and Manage are applied
iteratively, not as a rigid sequence. NIST emphasizes continuous risk
management, independent review, roles, inventory, and safe decommissioning
([AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)).

| Function | Application to agents/skills |
|---|---|
| Govern | policy, owners, inventory, training, risk tier, retirement |
| Map | intent, context, stakeholders, misuse, dependencies, impacts |
| Measure | evals, uncertainty, controls, production monitoring |
| Manage | prioritize, mitigate/accept/avoid/transfer, respond and recover |

### Security lifecycle

```text
scope -> threat model -> prevent -> verify -> detect -> respond -> recover -> learn
```

The threat model is updated when there is a new tool, data source, autonomy,
cross-agent protocol, or deployment boundary. Security verification happens
before release, and detection/recovery after. Prompt injection is an untrusted
input problem, not a separate one-off test case.

### Incident lifecycle

```text
detect -> triage -> contain -> diagnose -> remediate -> recover -> review
```

OODA drives fast decisions inside the incident, MAPE-K drives automated
operational controllers, and the incident lifecycle governs accountability and
transitions. Do not confuse containment with root-cause fix: first limit blast
radius, then prove the cause.

### Release lifecycle

```text
candidate -> offline eval -> shadow -> canary -> progressive rollout
          -> promote | pause | rollback -> observation window
```

Promotion criteria and rollback triggers are set before the canary. For a
skill/agent update, preserve the exact versions of the model, prompt,
references, scripts, tools, policies, and eval dataset.

## Entity lifecycles

### Agent

```text
discover need -> design contract -> prototype -> evaluate -> approve -> publish
-> activate -> observe -> improve -> deprecate -> retire
```

### Skill

```text
scout/harvest -> architect -> create -> validate/evaluate -> package -> publish
-> install/activate -> observe -> optimize/doctor -> upgrade -> deprecate -> retire
```

### Workflow

```text
model process -> specify states/contracts -> simulate -> verify failures
-> publish -> run -> reconcile -> evolve/migrate -> retire
```

### Memory item

```text
candidate -> verify provenance -> classify/scope -> approve -> retrieve/use
-> refresh/expire -> supersede/delete/archive
```

### Tool/integration

```text
assess -> threat model -> adapter contract -> sandbox test -> authorize -> observe
-> rotate credentials/update -> revoke -> retire
```

Each state has an owner, entry evidence, allowed actions, an exit gate, a
maximum age, and a recovery path. `Deprecated` is an active migration phase,
not a permanent label.
