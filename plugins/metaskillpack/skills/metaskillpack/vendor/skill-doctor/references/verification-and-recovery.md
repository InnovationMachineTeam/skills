# Verification and Recovery

## Contents

- Recovery proof
- Regression scope
- Health decision
- Forward-testing

## Recovery proof

Recovery requires the original reproduction to pass under comparable conditions. A structural validator, successful command, or reduced warning count is not a substitute for the failed user-visible outcome.

## Regression scope

Run checks affected by the patch plus guardrails for:

- discovery and neighboring triggers;
- resource loading and paths;
- scripts, dependencies, and failure codes;
- tools, permissions, and external effects;
- workflow, retries, partial success, and verification;
- security and untrusted data;
- declared hosts and installation.

## Health decision

- **RECOVERED**: original symptom passes and required guardrails hold.
- **PARTIAL**: one path is restored but material failures remain.
- **UNVERIFIED**: repair is plausible but original symptom or comparable environment was not tested.
- **FAILED**: symptom persists or a blocking regression appears.

Do not use static proxies to assign `RECOVERED`.

## Forward-testing

Use fresh context and realistic tasks. Do not reveal the diagnosis or expected fix. Inspect raw artifacts, traces, and side effects before accepting the evaluator's summary.

