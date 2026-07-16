---
name: agent-team-methodology-review
description: Use at the configured landed-slice cadence, milestone close, or after repeated blocker, proof, workflow-drift, human-surface, or manual-recovery failures to inspect primary evidence and keep, delete, automate, or change one operating-method surface.
---

# Agent Team Methodology Review

## Purpose

Improve proof movement and human comprehension without letting process work
dominate the project.

## Evidence Order

1. Identify the exact issue/MR trigger set.
2. Read the issues, MRs, diffs, proof artifacts, independent review findings,
   creator responses, and CI results.
3. Inspect the relevant durable evidence and compare it with live GitLab state.
4. If agent-loop telemetry is enabled, inspect its named MR-local boundaries and
   adjacent context; generated counts are indexes, not complete evidence.
5. Read the current `AGENTS.md`, skills, scripts, templates, CI, GitLab
   conventions, and ledger schemas before deciding which surface failed.

## Review Procedure

1. Create a GitLab issue from the methodology-review template.
2. Fill every question with primary evidence, an answer, and one action:
   `keep`, `delete`, `automate`, or `change`.
3. Measure proof movement, material reviewer findings, repeated failures,
   repeated manual work, state drift, human readability, and unbounded
   follow-ups.
4. Identify the single highest-leverage operating-method response.
5. Prefer deleting or automating friction over adding prose.
6. Normally change zero or one guide, skill, script, template, CI job, label
   convention, or ledger schema.
7. Obtain independent review of both the evidence chain and human readability.
8. Update the methodology, decision, and risk records as applicable.
9. Record the next review and cleanup trigger.

## No-Change Decisions

“No change” is valid only when named evidence supports explicit `keep` actions.
A blank template, generated counter, or verdict-only note is not a review.

## Closeout Gate

- Every question has evidence, answer, and action.
- Reviewer value is measured by actual findings and fixes.
- Repeated manual work is counted rather than described vaguely.
- GitLab and durable evidence agree.
- Every actionable follow-up is bounded or explicitly declined/superseded.
- An uninvolved engineer can understand the project from the GitLab human
  surface.
- Independent review approves the current methodology change or no-change
  decision.
