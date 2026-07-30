# Skill Optimization Taxonomy

## Contents

- Classification method
- Eight primary targets
- Root-cause and ordering rules
- Confidence

## Classification method

Classify by the metric or failure mechanism, not by the business domain or the type of skill being optimized. A tool skill can have a routing, context, reliability, security, portability, or cost problem.

Extract:

- observed failure and affected users;
- baseline evidence and reproducibility;
- intended behavior and invariants;
- target host, model, tools, and permissions;
- affected stage: discovery, instruction loading, execution, validation, or delivery;
- consequence of false positive, false negative, and regression.

## Eight primary targets

### 1. Routing and discovery

Choose when the skill fails to trigger, triggers on neighboring tasks, collides with another skill, or has unclear UI metadata. Optimize descriptions and held-out routing cases before changing the body.

### 2. Context and resource architecture

Choose when `SKILL.md` is bloated, references are duplicated or deeply nested, irrelevant context loads, resources are hard to discover, or stable and dynamic facts are mixed.

### 3. Workflow and reliability

Choose when steps are ambiguous, order or state is lost, clarification is poorly calibrated, retries are unbounded, partial success is mishandled, or completion is claimed without outcome verification.

### 4. Scripts and tool integration

Choose when deterministic operations are repeatedly regenerated, scripts fail, tool contracts are stale, dependencies are hidden, permissions are confused with capabilities, or mutations are unsafe.

### 5. Safety and authority

Choose when untrusted content becomes instruction, external or destructive actions lack consent, secrets may leak, scope expands silently, or technical enforcement is missing.

### 6. Evaluation and regression

Choose when improvement cannot be demonstrated, test cases are unrepresentative, judges are biased, routing lacks negative cases, or changes regularly reintroduce failures.

### 7. Portability and packaging

Choose when metadata, paths, tools, invocation syntax, host extensions, installation layout, or dependencies work in one client but fail in another.

### 8. Performance and context cost

Choose when latency, token use, tool calls, repeated reads, delegation, or resource size is excessive after correctness and safety are established.

## Root-cause and ordering rules

- Fix invalid structure and broken executables before semantic tuning.
- Fix safety and authority blockers before performance or style.
- Fix routing description before body when the body never loads.
- Fix missing evidence before optimizing against anecdotes.
- Optimize correctness before cost; optimize cost without removing necessary controls.
- Change one causal layer at a time: metadata, body, resources, scripts/tools, or eval rubric.
- Prefer deleting redundant rules to adding exceptions.
- Preserve intentional differences across risk tiers, hosts, and modes.

## Confidence

- **High**: reproducible failure maps to one stage and metric.
- **Medium**: one route leads but secondary causes are plausible.
- **Low**: baseline is missing or different routes imply different behavior changes.

At low confidence, gather evidence or ask the question with the highest expected information gain.

