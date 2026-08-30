---
name: agent-team-independent-review
description: Use when reviewing a GitHub work-slice pull request as a role distinct from the creator; test the stated claim, highest-risk boundary, and proof sufficiency; classify comments by landing impact; and record an approval or changes-requested decision.
---

# Agent Team Independent Review

## Independence

The reviewer must be distinct from the creator for the slice. The reviewer may
use the same repository and tools, but must reconstruct the claim from the issue,
PR, evidence, diff, tests, and generated artifacts rather than accepting the
creator's conclusion.

## Review Order

1. Read `AGENTS.md`, `docs/HUMAN_SURFACE.md`, the issue, and PR human summary.
2. Compare the requested problem, evidence version, target contract, and explicit
   non-claims.
3. Inspect the diff and highest-risk code path or artifact.
4. Run or inspect the narrowest discriminating proof before broad gates.
5. Ask what plausible wrong mechanism could still pass the submitted proof.
6. Check failure, rejection, rollback, compatibility, migration, security,
   observability, ownership, ordering, and terminal-state boundaries as relevant.
7. Verify durable evidence matches the actual claim and GitHub state.
8. Post one comment using `docs/templates/review-note.md`.

## Comment Classes

- `blocker:` material landing risk that must change, with a concrete path.
- `question:` context required before deciding.
- `suggestion:` useful non-blocking improvement.
- `nit:` optional local polish.
- `praise:` specific engineering choice worth retaining.

Do not convert preferences or unrelated redesign into blockers.

## Decisions

- `approved`: the bounded claim is supported and no blocker/question remains.
- `changes requested`: a concrete correction or proof improvement is required.
- `blocked`: an external decision, authority, or evidence artifact is required.

After creator changes, review the corrected head and affected proof. Approval
must refer to the current code/artifact state, not an earlier diff.

Apply the matching `review:*` label. Native GitHub approve/request-changes
states are optional extra signal in this edition, not the process authority.

## Follow-Ups

Check every accepted suggestion or deferred action. It must be completed, linked
to an issue with an exact reconsideration trigger, or explicitly declined or
superseded.
