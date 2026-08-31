# Decision Log

| ID | Date | Status | Decision | Evidence | Consequence | Revisit trigger | GitHub issue/PR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D0001 | 2026-08-30 | Accepted | Ship a GitHub edition (Option A): swap host surfaces, keep process identical | E0001, E0002, `docs/HOST.md` | GitLab templates/CI removed from tree; recover from `2b581184d08daed1d0f0b9611fbafbaa0f24e278` | Need both hosts (B) or native GitHub review enforcement (C); see `docs/ledgers/decision-records/D0001-github-edition.md` |  |
| D0002 | 2026-08-31 | Accepted | M0 exit is a Designed spec-exercise, not scaffold-file existence | `docs/PROOF_MODEL.md` Designed; empty rank-1 and leftover placeholders now fail `check-scaffold.sh`; `scripts/spec-exercise.sh` | Consumer pipelines fail until a domain harness lands; template self-test stays green | Named harness becomes allow_failure or is skipped | #1 |

Use `docs/templates/decision-record.md` for a decision that needs alternatives
and detailed rationale.
