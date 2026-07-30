# Tools and Environment Diagnostic Prompt

Apply after [base.md](base.md).

Inventory host, OS, runtime, shell, working directory, tool availability, versions, authentication status, permissions, network, sandbox, rate limits, schemas, and service health. Separate capability, credentials, permission, policy, and user authorization.

Classify transient, permanent, validation, authorization, rate-limit, schema, and ambiguous-result failures. Bound retries and avoid repeating side effects.

Repair configuration or usage only after confirming the mismatch. Do not broaden permissions, disable sandboxing, replace official tools with brittle workarounds, or rotate credentials without approval. Verify through the same tool path and read back external state when safe.

