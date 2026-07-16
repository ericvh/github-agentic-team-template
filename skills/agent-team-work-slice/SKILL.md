---
name: agent-team-work-slice
description: Use to implement one accepted GitLab work-slice issue with pinned evidence, a bounded write scope, focused positive and negative proof, a draft merge request, independent review, and synchronized closeout.
---

# Agent Team Work Slice

## Preconditions

- A GitLab issue exists from `.gitlab/issue_templates/work-slice.md`.
- Evidence is versioned and relevant source/spec/runtime/data has been read.
- Current and target proof levels are named.
- Predecessor, owner, authority, write scope, integration order, and independent
  reviewer are explicit.
- The worktree state is known and unrelated work can be preserved.

If these are missing, use `$agent-team-evidence-map` first.

## Workflow

1. Read `AGENTS.md`, the active issue, `docs/templates/work-slice-plan.md`, and
   relevant evidence, proof, decision, experiment, and risk rows.
2. Confirm the issue and local plan still match current GitLab and evidence.
3. Record the slice boundary before editing: behavior, API/artifact, invariants,
   non-claims, proof, reviewer focus, and write paths.
4. Implement the smallest coherent mechanism that retires or narrows the named
   proof gap.
5. Run focused static, positive, negative/failure, and discriminating proof.
6. Run shared gates proportional to the touched surface.
7. Update durable evidence in the same slice.
8. Open or refresh a draft MR from the work-slice template.
9. Obtain independent review through `$agent-team-independent-review`.
10. Resolve blockers/questions, rerun affected proof, and record creator
    responses.
11. After authorized merge, reconcile landed GitLab and durable state once.

## Implementation Rules

- Preserve behavior promised by the issue; do not widen the claim silently.
- Prefer explicit state and invariants over success inferred from control flow.
- Derive proof values from runtime behavior and independent reference evidence.
- Add rejection, fault, rollback, or edge proof when input/state surfaces widen.
- Keep generated measurements separate from static success.
- Preserve unrelated dirty work and respect disjoint write scopes.
- An actionable follow-up must have a linked issue and exact trigger or an
  explicit declined/superseded disposition.

## Completion Report

Name exact commands and results, proof movement, review decision, GitLab state,
durable rows changed, methodology trigger status, and the next issue. If the
slice is not landed, leave a resumable issue/MR state with exact remaining work.
