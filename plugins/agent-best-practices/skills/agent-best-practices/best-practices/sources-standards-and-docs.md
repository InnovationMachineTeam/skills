# Sources: Standards, Security, Lifecycle, and Documentation

Checked: **2026-07-30**.

## Agentic Lifecycle

### [ADLC — Agentic Development Life Cycle](https://www.adlc.io/)

Intent, Generate, Validate, Govern, Deploy, and Observe are parallel modes, not
strict stages. Agents execute, humans govern; bets replace prematurely "known"
requirements; validation and observation run continuously. Version 1.0, March
2026; living document.

### [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

A voluntary framework for managing AI risks; functions Govern, Map, Measure,
and Manage, plus profiles and a playbook. Use it for risk ownership,
documentation, measurement, and governance, not as a concrete agent runtime
design.

### [NIST Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

The AI RMF profile for GenAI risks and corresponding management, measurement,
and governance actions.

## Security

### [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)

Baseline threats: goal hijack, tool misuse, identity/privilege abuse, agentic
supply chain, unexpected code execution, memory/context poisoning, and other
agent-specific risks. Use it together with the local threat model.

### [OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/)

Risks of skills as an execution layer: permissions, orchestration, supply
chain, and portable skill surfaces. Useful for registry/install/security review
of skills.

## Requirements and Quality

### [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html)

A product quality model with nine characteristics and subcharacteristics for
specifying, measuring, and evaluating ICT/software product quality.

### [IREB downloads and resources](https://cpre.ireb.org/en/downloads-and-resources)

Handbooks and a glossary for requirements engineering, elicitation, modeling,
management, quality requirements, and traceability.

## Observability and Operations

### [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/)

Common attributes for model, tokens, operation, and data source.
Verbose/sensitive content must be opt-in; the conventions are under active
development.

### [Google SRE: Monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/)

The four golden signals: latency, traffic, errors, saturation. For Agent OS
they must be extended with task success, routing, tool, cost, approvals, and
safety signals.

## Documentation and Architecture

### [Diátaxis](https://diataxis.fr/)

Separates four reader needs: learning-oriented tutorials, task-oriented
how-to, information-oriented reference, and understanding-oriented explanation.
Do not mix them in a single document.

### [C4 model](https://c4model.com/)

Maps of code at the system context, container, component, and code levels, plus
dynamic/deployment views. Use only the levels that add value; context and
container are usually sufficient.

### [arc42](https://arc42.org/)

A process-agnostic pragmatic template for software/system architecture: goals,
constraints, context, solution strategy, building blocks, runtime/deployment,
cross-cutting concepts, decisions, quality, risks, and glossary. Adapt it
rather than filling it in mechanically.

### [MADR](https://adr.github.io/madr/)

Lean Markdown Architecture Decision Record: context, drivers, options, outcome,
consequences, status, consulted/informed, and confirmation. Decisions
supersede; they do not erase history.

## Source Priority Principle

1. Normative specification or current official documentation.
2. Official engineering guidance.
3. Live implementation at a pinned commit.
4. Secondary interpretation, only as an additional perspective.

If platform docs conflict with repository behavior, record the version and
verify the live runtime. If two approaches express a trade-off, choose the
decision by risk tier and eval evidence, not by brand authority.
