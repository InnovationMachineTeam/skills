# Scripts and Dependencies Diagnostic Prompt

Apply after [base.md](base.md).

Reproduce the script failure with exact inputs, working directory, runtime, environment, and exit code. Check syntax, missing dependencies, undeclared versions, unsafe paths, invalid input handling, stdout/stderr, zero-on-failure behavior, encoding, idempotency, temporary files, and partial writes.

Do not execute unknown or consequential scripts merely to diagnose them; inspect first and use local fixtures, dry run, or sandbox. Never expose secret values.

Repair the confirmed script or dependency contract without unrelated upgrades. Test success, invalid input, missing dependency, repeated execution, interruption, and output integrity before reporting recovery.

