# Безопасность, approvals и governance

## Модель угроз

Агентная система расширяет классический threat model:

- goal/prompt hijacking;
- tool misuse и unexpected code execution;
- identity/privilege abuse;
- malicious agent, tool, skill, MCP/A2A или dependency;
- memory/context poisoning;
- sensitive data leakage через prompts, tools, logs и artifacts;
- insecure inter-agent communication;
- denial of service и resource exhaustion;
- cascading failures и rogue loops;
- human-agent trust exploitation;
- supply-chain substitution и version drift.

OWASP Top 10 for Agentic Applications покрывает эти классы и должен
использоваться как baseline, но не заменяет domain threat model
([OWASP](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)).

## Непересекающиеся security boundaries

Разделяйте:

- model instructions;
- deterministic policy enforcement;
- sandbox/process isolation;
- filesystem/worktree isolation;
- network egress;
- identity и credentials;
- data authorization;
- human approval;
- audit.

Prompt-запрет не является access control. Worktree не является sandbox.
Guardrail classifier не заменяет authentication, authorization и стандартную
software security; это также подчёркивает OpenAI
([guide](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)).

## Least privilege

Каждый run получает минимальные:

- tools;
- filesystem paths;
- data rows/tenants;
- network destinations;
- credential scopes;
- action types;
- duration;
- delegation depth.

Permissions SHOULD быть capability-based и привязаны к run/task. Не выдавайте
долгоживущий универсальный токен команде агентов. Потомок не может расширить
authority родителя.

## Risk-classified tools

| Риск | Пример | Policy |
|---|---|---|
| Low | Read public docs | auto |
| Medium | Local reversible edit | sandbox + log |
| High | Push branch, update ticket | preview + scoped approval/policy |
| Critical | Public release, prod delete, payment | accountable human + exact digest + dual control |

Оценка учитывает read/write, reversibility, blast radius, data sensitivity,
financial/reputational impact и externality.

## Approval protocol

Approval MUST быть:

- информированным: intent, exact action, target, diff, risk, alternatives;
- scoped: tool, resource, parameters, duration;
- bound: digest/version, чтобы последующее изменение аннулировало approval;
- attributable: approver identity и authority;
- revocable и auditable;
- fail-closed при ambiguity.

Policy change из рассматриваемого change не может ослабить собственный gate.
Cursor Approval Agents применяют base policy и exact-path policies; при
неоднозначности требуют более строгий режим
([docs](https://cursor.com/docs/approval-agents)).

LLM approval agent MAY подготовить recommendation, но не заменяет accountable
human для critical действий.

## Prompt injection и недоверенный контент

- считать web, issue, PDF, code comments, tool outputs и messages данными, а не
  инструкциями;
- отделять system/task instructions от retrieved content;
- маркировать provenance и trust level;
- не исполнять команды из content без policy и user intent;
- минимизировать доступ tools у reader/researcher;
- применять output encoding/validation перед downstream tools;
- использовать canary tokens и anomaly detection;
- проверять indirect injection в memory и docs;
- не позволять одному недоверенному источнику изменять policy/memory.

## Sandbox и worktree

Write-capable агент запускается в disposable environment с:

- ограниченным filesystem;
- process/resource limits;
- scoped network egress;
- ephemeral runtime secrets;
- clean dependency/bootstrap path;
- artifact export allowlist;
- signed commits/provenance;
- human review перед merge.

Cursor Cloud Agents используют отдельные microVM, но сами предупреждают, что
auto-run commands и internet создают риск injection/exfiltration
([security](https://cursor.com/docs/cloud-agent/security),
[network](https://cursor.com/docs/cloud-agent/security-network)).

Worktree решает collision и branch isolation. Дополнительно проверяйте root,
branch, lease и main checkout. Shared `.git`, plugins и approvals могут
оставаться общими.

## Network policy

- deny by default для high-risk runs;
- allowlist exact domains/ports, не широкие wildcards;
- separate build-time и runtime access;
- egress proxy с identity и audit;
- запрет metadata endpoints и private networks без необходимости;
- DNS rebinding/redirect checks;
- download size/type/digest limits;
- secrets не попадают в URLs или logs;
- внешние agents проходят authentication, authorization и capability validation.

MCP применяется для tools/data, A2A — для opaque cross-platform agents; оба
требуют identity, contracts и least privilege, а не только protocol compliance.

## Supply chain

- pin versions и digests;
- verify signatures/provenance;
- registry lifecycle и revocation;
- manifest capabilities сверяются с фактической регистрацией;
- dependency/tool descriptions проходят review;
- eval/security scan до activation;
- canary rollout;
- inventory всех активных agent, skill, tool, MCP и A2A endpoints;
- emergency disable без обновления prompt.

## Memory и logs

Memory write — привилегированное действие. Требуйте provenance, sanitization,
scope, TTL и reviewer. Sensitive trace content по умолчанию отключается или
редактируется; OpenAI отмечает, что generation и function spans могут хранить
inputs/outputs ([tracing](https://openai.github.io/openai-agents-python/tracing/)).

## Governance

Определите RACI для:

- agent owner;
- tool/data owner;
- policy owner;
- eval owner;
- approver;
- incident commander;
- publisher/release owner;
- compliance/privacy/security reviewers.

Governance решает alignment и accountability, а не повторяет QA. ADLC помещает
человека в слой Govern: агент генерирует и валидирует, человек отвечает за
стратегическое решение
([ADLC](https://www.adlc.io/)).

## Security gates

До activation:

- threat model;
- tool/permission diff;
- prompt injection tests;
- negative authorization tests;
- sandbox/network tests;
- provenance и dependency scan;
- audit completeness;
- emergency stop drill;
- misuse evals.

После activation:

- anomaly detection;
- privilege/use review;
- incident feedback в evals;
- version drift detection;
- periodic access recertification;
- revoke stale/unowned agents.
