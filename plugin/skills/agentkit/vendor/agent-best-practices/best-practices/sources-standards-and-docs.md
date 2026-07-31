# Источники: стандарты, безопасность, lifecycle и документация

Проверено: **2026-07-30**.

## Agentic lifecycle

### [ADLC — Agentic Development Life Cycle](https://www.adlc.io/)

Intent, Generate, Validate, Govern, Deploy и Observe — параллельные modes, а не
строгие stages. Agents execute, humans govern; bets заменяют преждевременно
«известные» requirements; validation и observation идут постоянно. Версия 1.0,
март 2026; living document.

### [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

Добровольная структура управления AI risks; функции Govern, Map, Measure и
Manage, profiles и playbook. Использовать для risk ownership, documentation,
measurement и governance, а не как конкретный agent runtime design.

### [NIST Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

Профиль AI RMF для GenAI risks и соответствующих действий по управлению,
измерению и governance.

## Security

### [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)

Baseline threats: goal hijack, tool misuse, identity/privilege abuse, agentic
supply chain, unexpected code execution, memory/context poisoning и другие
agent-specific risks. Использовать вместе с локальным threat model.

### [OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/)

Риски skills как execution layer: permissions, orchestration, supply chain и
portable skill surfaces. Полезно для registry/install/security review навыков.

## Requirements и quality

### [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html)

Product quality model с девятью characteristics и subcharacteristics для
спецификации, измерения и оценки ICT/software product quality.

### [IREB downloads and resources](https://cpre.ireb.org/en/downloads-and-resources)

Handbooks и glossary по requirements engineering, elicitation, modeling,
management, quality requirements и traceability.

## Observability и operations

### [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/)

Общие attributes для model, tokens, operation и data source. Verbose/sensitive
content должно быть opt-in; conventions находятся в активном развитии.

### [Google SRE: Monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/)

Четыре golden signals: latency, traffic, errors, saturation. Для Agent OS их
нужно дополнять task success, routing, tool, cost, approvals и safety signals.

## Документация и архитектура

### [Diátaxis](https://diataxis.fr/)

Разделяет четыре потребности читателя: learning-oriented tutorials,
task-oriented how-to, information-oriented reference и understanding-oriented
explanation. Не смешивать их в одном документе.

### [C4 model](https://c4model.com/)

Maps of code на уровнях system context, containers, components и code, плюс
dynamic/deployment views. Использовать только уровни, которые добавляют ценность;
context и container обычно достаточны.

### [arc42](https://arc42.org/)

Process-agnostic прагматичный шаблон software/system architecture: goals,
constraints, context, solution strategy, building blocks, runtime/deployment,
cross-cutting concepts, decisions, quality, risks и glossary. Адаптировать, а не
заполнять механически.

### [MADR](https://adr.github.io/madr/)

Lean Markdown Architecture Decision Record: context, drivers, options, outcome,
consequences, status, consulted/informed и confirmation. Решения supersede, а не
стирают историю.

## Принцип приоритета источников

1. Нормативная спецификация или current official documentation.
2. Официальное engineering guidance.
3. Live implementation на зафиксированном commit.
4. Secondary interpretation — только как дополнительный взгляд.

Если platform docs конфликтуют с repository behavior, фиксируется версия и
проверяется live runtime. Если два подхода выражают trade-off, решение выбирается
по risk tier и eval evidence, а не по авторитету бренда.
