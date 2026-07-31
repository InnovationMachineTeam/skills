# Documentation, Research, Trendwatching, and Innovation

## Documentation system

### One-agent pattern

Use one documentation steward when the task is to inventory a repository,
maintain a documentation map, detect drift, and propose updates without making
product or architecture decisions.

```text
Create one documentation-steward agent. It reads code, tests, registries, ADRs,
and release artifacts; writes only under docs/ and review output; uses private
skills for claim verification and link checking; and requests owner review for
semantic changes. Register the agent and its private capabilities.
```

### Team pattern

Use a team for a large platform with separate product, developer, API,
architecture, operations, security, and learning documentation. Add a content
architect, domain writers, code-sample verifier, editor, accessibility reviewer,
and independent fact checker. Every claim must have a source or a verification
marker; generated views must be labeled and rebuilt from canonical data.

## Research

### One-agent pattern

A bounded desk-research question can use one research agent plus human review.
It owns a query plan, source log, evidence table, contradiction log, synthesis,
confidence, limitations, and dated output. It must distinguish source facts,
quotes, calculations, and inference.

```text
Use agent-builder to create and evaluate one market-research agent for the
question "What prevents mid-sized product teams from adopting agent evaluation?"
It may use approved web sources and supplied documents, must preserve provenance
and dates, and writes under docs/research/. It cannot contact participants or
publish externally.
```

### Team pattern

Use separate question-framing, source-discovery, extraction, quantitative or
qualitative analysis, synthesis, red-team, and editorial roles for consequential
or multi-method research. Keep holdout sources or challenge cases away from the
primary synthesizer when evaluating robustness.

Required documents:

```text
docs/research/<study>/question.md
docs/research/<study>/protocol.md
docs/research/<study>/sources.json
docs/research/<study>/evidence/
docs/research/<study>/analysis/
docs/research/<study>/contradictions.md
docs/research/<study>/report.md
docs/research/<study>/review.md
```

## Trendwatching

A recurring trendwatching team includes horizon scanner, source curator, signal
classifier, trend analyst, scenario/implications analyst, domain challenger,
and briefing editor. A one-off scan can use one agent.

Track signals separately from trends:

- signal: dated observation with source and confidence;
- pattern: related signals across time or domains;
- trend: sustained direction with evidence and counter-signals;
- implication: conditional effect on a named stakeholder or decision;
- scenario: internally coherent future, not a prediction;
- watch item: trigger, owner, cadence, and next review date.

```text
Use agent-team-manager to design a monthly AI product trendwatching team. Create
the required research, provenance, contradiction, scenario, and briefing skills;
keep client-specific taxonomy private. Produce a signal log, trend cards,
counter-signals, implications, scenarios, watchlist, and executive briefing.
```

## Design Thinking

Design Thinking needs divergent discovery and convergent decisions without
letting synthesis fabricate evidence.

Suggested roles:

- challenge owner and human decision maker;
- research planner/interviewer;
- evidence synthesizer;
- opportunity/point-of-view facilitator;
- ideation facilitator;
- prototype designer;
- experiment/usability evaluator;
- process orchestrator.

Documents include challenge brief, stakeholder map, consent/research plan, raw
evidence, observations, insight statements, jobs/needs, opportunity areas,
ideation log, selection criteria, prototype briefs, test scripts, results, and
decision log.

```text
Use agent-team-manager to create a Design Thinking team for improving new-user
activation. Preserve raw research separately from synthesis, keep the human
product owner accountable for framing and selection, and stop after a tested
prototype and evidence-backed decision. Create private facilitation skills for
this team and public research-evidence skills only if already reusable.
```

## Business TRIZ

Business TRIZ work benefits from explicit problem models rather than generic
brainstorming.

Suggested roles:

- problem/framing analyst;
- system and stakeholder modeler;
- contradiction analyst;
- resources and constraints analyst;
- evolution/trend analyst;
- solution-concept generator;
- feasibility and risk challenger;
- experiment designer;
- accountable decision owner.

Documents include initial situation, ideal final result, system/operator model,
contradictions, available resources, harmful/useful functions, constraints,
analogy/principle applications, concept portfolio, risk/feasibility evidence,
experiments, and decisions.

```text
Use agent-team-manager to design a Business TRIZ team for reducing onboarding
time without increasing compliance risk. Require explicit contradictions,
resources, ideal final result, solution concepts, feasibility, risk, and
experiments. The team may recommend but cannot change compliance policy or
production processes without approval.
```

## Research and innovation gates

- research questions and decision use are declared before collection;
- participant consent, PII, rights, and source terms are enforced externally;
- raw evidence is preserved separately from interpretation;
- negative and contradictory evidence is visible;
- inference and uncertainty are labeled;
- trend claims include time window, baseline, counter-signals, and review date;
- innovation frameworks structure thinking but do not manufacture validation;
- decisions state owner, evidence, alternatives, risks, and revisit trigger.
