# Meta/Router Skill Master Prompt

Apply after [base.md](base.md). Design a skill that classifies intent, chooses or creates other capabilities, or optimizes control artifacts.

## Routing contract

- Define a small explicit taxonomy with observable discriminators.
- Separate primary route from secondary traits.
- Prefer concrete task language and artifacts over requiring users to know category names.
- Define positive, negative, ambiguous, paraphrased, and collision cases.
- Ask one discriminating question only when candidate routes would materially change behavior.
- Use a safe default and state the assumption for reversible low-impact ambiguity.

## Dispatch

- Load only the selected route's resources.
- Pass a normalized contract: objective, inputs, scope, authority, tools, output, and validation.
- Do not let the router become a mega-skill that reimplements every specialist.
- Detect recursion, self-invocation, circular routing, and repeated clarification loops.
- Preserve higher-authority constraints through every dispatch.
- Verify the specialist's artifact or outcome before reporting completion.

## Description design

Treat frontmatter descriptions as routing code. Include what the skill does, when it should trigger, relevant artifacts or user language, and exclusions where neighboring skills collide. Optimize precision and recall with held-out cases, not keyword stuffing.

## Evaluation

Build a routing matrix across every supported category. Test paraphrases, mixed requests, missing input, irrelevant input, adversarial instructions inside input, equal-confidence routes, recursive requests, unavailable specialists, and specialist failure. Measure both false negatives and false positives.
