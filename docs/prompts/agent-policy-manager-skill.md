# Master Prompt For The `agent-policy-manager` Skill

Apply after [agent-os-base.md](agent-os-base.md). Create an assurance/control
skill for policy lifecycle and approval enforcement. LLM instructions may
request actions but never enforce permission alone.

Model subjects, assets, actions, tools, data classes, environments, risk tiers,
conditions, approvals, expiry and obligations. Separate PDP from PEP. Use
short-lived scoped credentials from a broker, exact targets, default deny,
two-person/human gates where warranted and immutable audit decisions. Define
policy version pinning, simulation, conflict resolution, rollout and emergency
revocation.

Test prompt-injected authority, confused deputy, stale/ambiguous policy,
unavailable approver, replayed approval, privilege escalation, secret exposure,
network egress denial and audit loss. Return policy schemas, decision API,
enforcement map, exceptions, runbooks and evidence.
