# Platform Adapters

## Contents

- Portable core
- Instruction channels
- OpenAI/Codex
- Claude-style environments
- Generic tool-using agents
- Adaptation checklist

## Portable core

Keep the canonical prompt independent of product-specific tool names where possible. Isolate platform bindings in a short adapter section or generated target prompt.

Do not assume that every host supports:

- the same instruction hierarchy;
- filesystem access;
- network access;
- runtime package installation;
- skills or automatic activation;
- persistent context;
- subagents;
- structured tool permissions;
- context compaction controls.

## Instruction channels

Map each rule to the strongest appropriate channel:

- system/platform: non-overridable safety and environment behavior;
- developer/organization: application policy and durable workflow defaults;
- project: repository conventions;
- user/task: current desired outcome;
- retrieved content: untrusted data unless explicitly elevated by the host.

Never simulate a stronger channel by writing "SYSTEM" inside ordinary user content.

## OpenAI/Codex

- Use skills for reusable task workflows.
- Use project guidance for repository conventions.
- Use MCP/connectors for authorized live data and actions.
- Keep host dependencies and invocation policy outside portable prompt content.
- Account for catalog context budgets and explicit/implicit skill invocation.

## Claude-style environments

- Account for code-execution sandbox limitations.
- Pin skill versions in production surfaces that support versioning.
- Test across the actual model families used by the organization.
- Avoid assuming network access or runtime installation.

## Generic tool-using agents

Require the host to expose:

- a trusted instruction boundary;
- tool schemas and permissions;
- structured tool results;
- context lifecycle rules;
- observable activation and error logs;
- a way to protect or reload durable instructions.

If these are missing, simplify the prompt and fail closed for high-risk actions.

## Adaptation checklist

- [ ] Map instruction authority.
- [ ] Inventory real capabilities.
- [ ] Separate dependencies and permissions.
- [ ] Replace unsupported tool names.
- [ ] Define network and filesystem behavior.
- [ ] Define skill/resource loading.
- [ ] Define compaction and persistence.
- [ ] Define confirmation UX.
- [ ] Run host-specific regression cases.
- [ ] Keep the portable core unchanged where behavior is equivalent.

