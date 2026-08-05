# Security, Approvals, and Governance

## Threat model

An agentic system expands the classic threat model:

- goal/prompt hijacking;
- tool misuse and unexpected code execution;
- identity/privilege abuse;
- malicious agent, tool, skill, MCP/A2A, or dependency;
- memory/context poisoning;
- sensitive data leakage via prompts, tools, logs, and artifacts;
- insecure inter-agent communication;
- denial of service and resource exhaustion;
- cascading failures and rogue loops;
- human-agent trust exploitation;
- supply-chain substitution and version drift.

OWASP Top 10 for Agentic Applications covers these classes and should be used
as a baseline, but it does not replace the domain threat model
([OWASP](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)).

## Non-overlapping security boundaries

Separate:

- model instructions;
- deterministic policy enforcement;
- sandbox/process isolation;
- filesystem/worktree isolation;
- network egress;
- identity and credentials;
- data authorization;
- human approval;
- audit.

A prompt prohibition is not access control. A worktree is not a sandbox.
A guardrail classifier does not replace authentication, authorization, and
standard software security; OpenAI emphasizes this as well
([guide](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)).

## Least privilege

Each run receives the minimum:

- tools;
- filesystem paths;
- data rows/tenants;
- network destinations;
- credential scopes;
- action types;
- duration;
- delegation depth.

Permissions SHOULD be capability-based and bound to the run/task. Do not issue a
long-lived universal token to an agent team. A descendant cannot expand the
parent's authority.

## Risk-classified tools

| Risk | Example | Policy |
|---|---|---|
| Low | Read public docs | auto |
| Medium | Local reversible edit | sandbox + log |
| High | Push branch, update ticket | preview + scoped approval/policy |
| Critical | Public release, prod delete, payment | accountable human + exact digest + dual control |

Assessment accounts for read/write, reversibility, blast radius, data
sensitivity, financial/reputational impact, and externality.

## Approval protocol

Approval MUST be:

- informed: intent, exact action, target, diff, risk, alternatives;
- scoped: tool, resource, parameters, duration;
- bound: digest/version, so a later change invalidates the approval;
- attributable: approver identity and authority;
- revocable and auditable;
- fail-closed under ambiguity.

A policy change from the change under review cannot weaken its own gate. Cursor
Approval Agents apply base policy and exact-path policies; under ambiguity they
require the stricter mode
([docs](https://cursor.com/docs/approval-agents)).

An LLM approval agent MAY prepare a recommendation, but it does not replace the
accountable human for critical actions.

## Prompt injection and untrusted content

- treat web pages, issues, PDFs, code comments, tool outputs, and messages as
  data, not instructions;
- separate system/task instructions from retrieved content;
- label provenance and trust level;
- do not execute commands from content without policy and user intent;
- minimize tool access for reader/researcher roles;
- apply output encoding/validation before downstream tools;
- use canary tokens and anomaly detection;
- check indirect injection into memory and docs;
- do not let one untrusted source change policy/memory.

## Sandbox and worktree

A write-capable agent runs in a disposable environment with:

- restricted filesystem;
- process/resource limits;
- scoped network egress;
- ephemeral runtime secrets;
- clean dependency/bootstrap path;
- artifact export allowlist;
- signed commits/provenance;
- human review before merge.

Cursor Cloud Agents use separate microVMs, but they explicitly warn that
auto-run commands and internet access create injection/exfiltration risk
([security](https://cursor.com/docs/cloud-agent/security),
[network](https://cursor.com/docs/cloud-agent/security-network)).

Worktree solves collision and branch isolation. Also verify the root, branch,
lease, and main checkout. Shared `.git`, plugins, and approvals may still be
common.

## Network policy

- deny by default for high-risk runs;
- allowlist exact domains/ports, not broad wildcards;
- separate build-time and runtime access;
- egress proxy with identity and audit;
- block metadata endpoints and private networks unless needed;
- DNS rebinding/redirect checks;
- download size/type/digest limits;
- secrets do not appear in URLs or logs;
- external agents undergo authentication, authorization, and capability
  validation.

MCP is used for tools/data, A2A for opaque cross-platform agents; both require
identity, contracts, and least privilege, not just protocol compliance.

## Supply chain

- pin versions and digests;
- verify signatures/provenance;
- registry lifecycle and revocation;
- manifest capabilities are checked against actual registration;
- dependency/tool descriptions pass review;
- eval/security scan before activation;
- canary rollout;
- inventory of all active agent, skill, tool, MCP, and A2A endpoints;
- emergency disable without prompt updates.

## Memory and logs

Memory writes are privileged actions. Require provenance, sanitization, scope,
TTL, and a reviewer. Sensitive trace content is disabled or redacted by
default; OpenAI notes that generation and function spans may store
inputs/outputs ([tracing](https://openai.github.io/openai-agents-python/tracing/)).

## Governance

Define RACI for:

- agent owner;
- tool/data owner;
- policy owner;
- eval owner;
- approver;
- incident commander;
- publisher/release owner;
- compliance/privacy/security reviewers.

Governance resolves alignment and accountability rather than repeating QA. ADLC
places the human in the Govern layer: the agent generates and validates, the
human is responsible for the strategic decision
([ADLC](https://www.adlc.io/)).

## Security gates

Before activation:

- threat model;
- tool/permission diff;
- prompt injection tests;
- negative authorization tests;
- sandbox/network tests;
- provenance and dependency scan;
- audit completeness;
- emergency stop drill;
- misuse evals.

After activation:

- anomaly detection;
- privilege/use review;
- incident feedback into evals;
- version drift detection;
- periodic access recertification;
- revoke stale/unowned agents.
