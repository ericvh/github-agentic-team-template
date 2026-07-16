# Work Slice

## Human Goal

What behavior or project outcome changes, and why is it the next dependency?

## Evidence Anchor

- Source of truth:
- Version/commit/hash/date:
- Relevant paths, interfaces, scenarios, or data:
- Existing proof and known gaps:

## Target Change

- Component/API/artifact:
- Behavioral contract:
- Invariants:

## Proof Promotion

- Current level:
- Target level:
- Exact commands or generated artifacts:
- Discriminating negative/failure evidence:

Complete this sentence:

> The proof would fail if the implementation used `<plausible wrong mechanism>`
> because `<specific observation>` would differ.

## Review Focus

- Highest-risk semantics:
- What could pass broad tests while still being wrong?
- Rollback, compatibility, security, migration, or observability concern:

## Boundaries

- In scope:
- Explicitly not claimed:
- Deferred dependencies:

## Backlog Position

- Rank in planned horizon:
- Predecessor:
- Unblocks:
- Dependency boundary:
- Proof boundary:
- Parallel lane:
- Integration order:
- Next issue:

## Ownership and Authority

- Authority level/exceptions:
- Orchestrator:
- Evidence mapper:
- Implementer/write scope:
- Independent reviewer:
- CI/proof owner:
- State closer:

## Durable State

- Evidence-map rows:
- Proof-ledger rows:
- Decision/experiment/risk rows:
- Methodology trigger:

## Done

- [ ] Evidence map and proof plan are current.
- [ ] Predecessor, authority, ownership, and write scope are confirmed.
- [ ] Implementation satisfies the bounded contract.
- [ ] Focused and required broad verification pass.
- [ ] Independent review is resolved and approved.
- [ ] Follow-ups have bounded dispositions.
- [ ] Durable evidence and GitLab state are reconciled.
