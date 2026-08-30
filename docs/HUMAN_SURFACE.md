# Human GitHub Surface

GitHub is useful only if an engineer who did not participate in the agent session
can understand the project state from the issue/PR list and the top of each
work item.

## Issue Contract

A work-slice issue should fit on one screen before detailed checklists:

1. Human goal and why the slice is next.
2. Versioned evidence anchor.
3. Target component, API, or behavior.
4. Current and target proof levels.
5. Highest-risk review focus.
6. Explicit non-claims and deferred dependencies.
7. Backlog position, predecessor, unblocks, parallel lane, and owner.

Do not put agent ids, transcripts, token tables, runner ids, or complete
orchestration logs in the issue body. Use comments for meaningful planning
changes, proof updates, blockers, or human steering that changes the contract.

## Pull Request Contract

The top of a pull request must answer:

- What behavior or outcome changed?
- What mechanism or implementation carries it?
- What should the reviewer inspect most carefully?
- What proof passed, using which exact command or artifact?
- What remains unsafe to assume?

Detailed agent provenance, session boundaries, raw logs, and cost tables belong
in a checked-in report or CI artifact. When required, the PR carries one compact
link and a short status summary.

## Sparse Comments

Useful comments are:

- a material planning or scope change;
- a proof update or blocker;
- an independent review decision and findings;
- a creator response;
- human steering that changes scope, proof, authority, methodology, or next
  action;
- final ready or landed closeout.

Do not create a comment for every label change, ledger edit, agent handoff,
telemetry refresh, or routine runner poll.

## Review Comments

Review protects correctness, maintainability, context transfer, and safe landing.
Classify comments by landing impact:

| Prefix | Meaning |
| --- | --- |
| `blocker:` | Must change before merge because a material risk remains. |
| `question:` | Context is required before the reviewer can decide. |
| `suggestion:` | Useful improvement that is non-blocking by default. |
| `nit:` | Optional local polish. |
| `praise:` | A specific engineering choice worth retaining. |

A blocker names the risk and a concrete landing path. Review the change, not the
author. Keep provenance in a short evidence appendix below the author-facing
comments.

## Follow-Up Contract

A known gap is behavior the PR does not claim. It is not automatically a promise.
Every actionable promised fix, accepted suggestion, cleanup, or deferred process
change must have one complete disposition:

- a linked GitHub issue with current state and an exact dependency, counter, or
  event that will reconsider it; or
- explicitly declined or closed as superseded.

“Later” and “remains planned” are not complete dispositions.

## Methodology Question

Every methodology review asks:

> Could an engineer who did not participate in the agent session understand the
> current project state from the GitHub issue/PR list and the top of each PR?

If not, prune or relocate process detail before adding another control.
