---
name: private-check
description: Performs the code-reviewer's repository-specific trust-boundary check. Use only inside the code-reviewer agent when reviewing changes to protected authorization paths. Do not expose as a globally discoverable skill.
metadata:
  version: 1.0.0
---

# Private Check

Inspect protected authorization paths and report concrete trust-boundary findings.

## Constraints

- Read only.
- Cite the affected file or symbol.
- Stop if the owning code-reviewer identity is not established.
