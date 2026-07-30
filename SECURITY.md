# Security policy

## Reporting

Do not open a public issue for a suspected vulnerability, credential leak, malicious skill, or unsafe script. Report privately to `stanislav.usoltsev@gmail.com` and include the affected skill, version, reproduction, impact, and any known exposure.

## Supply-chain policy

- Treat every imported skill and script as untrusted until reviewed.
- Preserve provenance, upstream revision, license, and local modifications.
- Never store credentials in skills, prompts, fixtures, manifests, generated bundles, or logs.
- Run scripts with least privilege and inspect them before first execution.
- Reject symlinks, traversal, absolute local runtime paths, and hidden executable payloads.
- Use a pilot scope before organization-wide activation.

## Response

The repository owner may quarantine an entry, roll back to a known-good release, or temporarily restrict marketplace access. A follow-up review records root cause, affected versions, remediation, and public-disclosure decision.

## Supported release

Until a public support policy is approved, only the latest private release is supported. The previous known-good release is retained for rollback.
