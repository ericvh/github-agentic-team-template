# Proof Model

Implementation is project movement only when the evidence state changes. Select
the levels that fit the project in `project-formulation.md`.

## Default Ladder

```text
Unmapped -> Mapped -> Designed -> Static -> Unit -> Contract/Golden
         -> Integration -> Operational/Performance
```

| Level | Claim supported | Typical evidence | Does not prove |
| --- | --- | --- | --- |
| Unmapped | No bounded claim yet | initial backlog seed | source coverage or feasibility |
| Mapped | Relevant constraints are known | pinned source/spec/runtime/data and dependency map | implementation correctness |
| Designed | Target behavior, boundary, and proof plan are explicit | accepted work-slice plan | implemented behavior |
| Static | Code/configuration is structurally valid | format, lint, type/build, schema checks | runtime behavior |
| Unit | Local invariants hold | focused positive and negative tests | external compatibility or composition |
| Contract/Golden | Named behavior matches an independent reference | API contract, trace, differential run, Golden artifact | untested input classes or performance |
| Integration | Components compose in a representative route | end-to-end scenario or migration rehearsal | production scale and reliability |
| Operational/Performance | Deployment constraints hold under named conditions | benchmark, canary, fault injection, observability, rollback evidence | behavior outside measured conditions |

## Proof Promotion

Every work-slice issue names:

- current proof level;
- target proof level;
- exact command or generated artifact;
- expected discriminating result;
- explicit behavior outside the claim.

Higher-level evidence does not erase focused negative tests. A broad green
integration test can still miss the wrong owner, stale state, copied constant,
silent fallback, overly broad parser, partial migration, or reordered event.

## Discriminating Observation

Before implementation, complete this sentence:

> The proof would fail if the implementation used `<plausible wrong mechanism>`
> because `<specific observation>` would differ.

Examples:

- A callback owner nonce changes if the implementation substitutes or clones it.
- A negative parser fixture is rejected if the accepted input surface remains
  bounded.
- A rollback rehearsal restores the previous schema and traffic path.
- A trace records runtime ordering rather than expected constants.
- A fault-injection test proves partial success cannot be reported as complete.

## Equality and Golden Evidence

Expected constants may identify provenance but must not stand in for measured
behavior. Derive compared values independently from:

1. the actual implementation execution or generated artifact; and
2. the pinned reference source, specification, captured runtime, or dataset.

Record the reducer or comparison command so another agent can reproduce it.

## Performance and Operational Claims

Static success is not performance evidence. Name:

- workload and input version;
- environment and configuration;
- measurement command;
- artifact path;
- relevant percentiles or failure rates;
- comparison baseline;
- uncertainty and conditions outside the claim.
