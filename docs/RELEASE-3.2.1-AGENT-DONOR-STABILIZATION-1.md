# Release 3.2.1: Agent Donor Stabilization Cycle 1

Status: **PASS — first post-donor stable release**

## Scope

This maintenance release certifies the first stability cycle after the ten
individual-agent lifecycle donors entered the marketplace in `3.2.0`. Donor
contents and individual versions remain unchanged. The aggregate and repository
marketplace version advances to `3.2.1`.

## Frozen target

- ten donors at `1.0.0`;
- portfolio hash:
  `sha256:9e50a4d18873efe6063b58393a93a56b96658d195b5293fff820c2affd5c5751`;
- baseline release: `3.2.0`;
- candidate release: `3.2.1`;
- changed donor hashes: none.

## Evidence

- official skill validation: 10/10 PASS;
- repository unit tests: 51/51 PASS;
- individual-agent eval fixture sets: 10/10 PASS;
- portable repository: 38 skills and 38 individual plugins PASS;
- marketplace generation: three current manifests, 38 entries each;
- dependency graph: 10 declarations across 38 catalog skills PASS;
- registry, bindings, locators, hashes and generated views: PASS.

The independent `3.2.0` forward evidence remains applicable because every donor
hash is unchanged. This release does not claim a new stochastic model run.

## Lifecycle manifest

- operation: maintenance release and first stability-cycle certification;
- source: unchanged canonical donors plus release/evaluation metadata;
- target: private `InnovationMachineTeam/skills` marketplace;
- affected users: none until they explicitly update or install;
- activation: not performed;
- rollback: pin repository revision or restore marketplace/aggregate `3.2.0`;
- reviewer: `@stanislavus86`.

## Agentkit decision

`agentkit` remains deferred. One of two required stable releases is complete;
the second must be a distinct later observation. At least three real
end-to-end workflows, a frozen upgrade/rollback contract and pack-level holdout
also remain outstanding.
