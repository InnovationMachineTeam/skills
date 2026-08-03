# Agentic OS Skills

Use these skills only when individual agents or an ordinary team runtime cannot
provide the required durable shared services.

| Skill | Plane or responsibility |
|---|---|
| `agent-os-architect` | minimum platform architecture and build/extend/buy comparison |
| `agent-os-bootstrapper` | approved non-production vertical walking skeleton |
| `agent-os-evaluator` | independent frozen evaluation and release evidence |
| `agent-model-router` | governed runtime routing across an approved model pool |
| `agent-policy-manager` | versioned authorization and approval policy |
| `agent-protocol-manager` | MCP, A2A, host and provider adapter contracts |
| `agent-registry-manager` | desired inventory and observed-state reconciliation |
| `agent-runtime-manager` | durable tasks, leases, retries, cancellation, recovery |
| `agent-observer` | traces, SLOs, alerts, incidents, cost, and drift evidence |

## Full command examples

These are illustrative commands; adapt names, constraints, and approved input
artifacts before execution.

```text
/agent-os-architect Design the minimum Agentic OS for a support-ticket automation platform with durable runs, policy enforcement, observability, and a build-versus-buy recommendation
```

Expected result: an architecture decision and minimum vertical slice with
explicit rejected components, ownership, risks, and release gates.

```text
/agent-os-bootstrapper Materialize the approved non-production walking skeleton from docs/agent-os/architecture.json and keep production activation disabled
```

Expected result: a staged, inspectable skeleton that matches the approved
architecture and reports verification evidence without implying deployment.

```text
/agent-observer Define traces, SLOs, alerts, redaction rules, and incident diagnostics for the approved support-ticket runtime
```

Expected result: an observability contract with measurable signals, privacy
boundaries, alert conditions, and bounded diagnostic actions.

Start with a no-platform alternative and one vertical slice. Production rollout
is never implied by design, bootstrap, evaluation, or registration.

See [Agentic OS onboarding](../../docs/ONBOARDING.md#the-agentic-os-workflow)
and [worked examples](../../docs/use-cases/agentic-os.md).
