# Methodology Ledger

| Review | Date | Trigger | Issues/PRs reviewed | Evidence | Decision | Operating surface changed | Next trigger |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M0000 |  | Bootstrap |  | Initial scaffold | Pilot one vertical proof-carrying slice before adding process. | Initial guide/templates/CI | After configured landed-slice count or milestone close |
| M0001 | 2026-08-30 | Host port request | none (scaffold conversion) | D0001, E0001, E0002 | Change host to GitHub; keep process; defer B and C | Templates, CI, contracts, `docs/HOST.md` | Configured landed-slice count, milestone close, or a named B/C trigger |

## Early Trigger Watchlist

| Signal | Current count | Threshold | Action |
| --- | --- | --- | --- |
| Same blocker family repeats | 0 | 2 | Open methodology-review issue. |
| Same proof failure repeats | 0 | 2 | Open methodology-review issue. |
| GitHub and durable evidence drift | 0 | 1 material occurrence | Reconcile and review authority/synchronization rule. |
| Manual recovery repeats | 0 | 3 | Automate, remove, or explicitly keep with evidence. |
| Ready PR lacks independent review | 0 | 1 | Return to draft and review operating contract. Consider Option C. |
| Human GitHub surface is unreadable | 0 | 1 | Prune or relocate process detail. |
| Actionable follow-up is unbounded | 0 | 1 | Link issue/trigger or explicitly decline/supersede. |
| Host-native GitHub control added off-issue | 0 | 1 | Revert or open Option B/C as its own slice (R0002). |
