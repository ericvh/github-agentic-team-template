# Work Slice Plan

## Summary

- Slice:
- Human outcome:
- Evidence version:
- Target component/API/artifact:
- GitLab milestone:
- GitLab issue:
- GitLab MR:
- Branch:
- Authority level/exceptions:
- Owner:
- Independent reviewer:
- Date:

## Scope

- In scope:
- Explicit non-claims:
- Required dependencies:
- Deferred dependencies:

## Backlog Context

| Rank | GitLab issue | Outcome | Dependency/proof boundary | Why next | Stop/defer rule |
| --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |

## Evidence Map

| Source/spec/runtime/data | Version | Purpose | Constraint | Target |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Design

- Public interface:
- Ownership/state boundaries:
- Invariants:
- Failure and rollback handling:
- Compatibility/migration behavior:
- Observability:

## Proof Plan

| Level | Command or artifact | Expected discriminating result |
| --- | --- | --- |
| Static |  |  |
| Unit |  |  |
| Contract/Golden |  |  |
| Integration |  |  |
| Operational |  |  |

Plausible wrong mechanism and the observation that rejects it:

## Team Orchestration

| Role | Agent/thread | GitLab issue | Read scope | Write scope | Required output | Integration order |
| --- | --- | --- | --- | --- | --- | --- |
| Orchestrator |  |  |  | workflow state | ordered integration | first/last |
| Evidence mapper |  |  |  | evidence rows | evidence/proof map | before code |
| Implementer |  |  |  |  | commit and verification |  |
| Independent reviewer |  |  | full MR | review note only | decision/findings | after coherent MR |
| CI/proof owner |  |  | pipeline/proof | scoped infrastructure | verified result | before ready |
| State closer |  |  | GitLab + records | state rows | landed reconciliation | last |

## Exit Criteria

- [ ] Evidence, authority, dependencies, and write scopes are explicit.
- [ ] Target behavior and non-claims are bounded.
- [ ] Proof rejects the named plausible false positive.
- [ ] Required review and approval are complete.
- [ ] Follow-ups have bounded dispositions.
- [ ] GitLab and durable evidence agree after landing.
