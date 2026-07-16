---
name: agent-team-evidence-map
description: Use before implementation to pin source, specification, runtime, data, requirement, or finding evidence; map dependencies and risks; define a bounded target and discriminating proof plan; and prepare a dependency-ordered GitLab work-slice issue.
---

# Agent Team Evidence Map

## Purpose

Turn an ambiguous project request into a versioned evidence map and one bounded
proof-carrying work slice before implementation begins.

## Fast Path

1. Read `AGENTS.md`, `docs/project-formulation.md`, `docs/PROOF_MODEL.md`,
   `docs/WORKFLOW.md`, and the relevant ledger rows.
2. Inspect GitLab for the current milestone, active issue, planned horizon, and
   predecessor state.
3. Pin the authoritative evidence by commit, version, timestamp, dataset hash,
   or captured runtime artifact.
4. Map relevant interfaces, tests, scenarios, data, dependencies, risks, and
   behavior explicitly outside the claim.
5. Define one semantic slice and target proof promotion.
6. Name a plausible false implementation and the observation that would reject
   it.
7. Update `evidence-map.md` and `proof-ledger.md`.
8. Create or refresh a GitLab issue using the `work-slice` template.

## Required Outputs

- Versioned evidence map.
- Dependency map with predecessor, unblocks, and integration order.
- Target component/API/artifact and behavioral contract.
- Current and target proof levels.
- Positive, negative/failure, and discriminating proof plan.
- Highest-risk reviewer focus.
- Explicit non-claims and deferred dependencies.
- Owner, authority, write scope, and independent reviewer plan.
- GitLab issue and durable ledger updates.

## Rules

- Evidence coverage is not behavioral proof.
- Do not start implementation with an unversioned source of truth.
- Do not choose a slice only because its files are nearby; choose a coherent
  dependency and proof boundary.
- Do not invent a long speculative backlog. Maintain the configured short
  horizon and refresh it as evidence changes.
- If the requested slice cannot be proven with available evidence, mark the
  concrete blocker and required decision or artifact.

## Completion Gate

Another implementer should be able to start from the issue and checked-in plan
without reconstructing the mapper's reasoning from chat.
