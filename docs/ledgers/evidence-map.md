# Evidence Map

| ID | Domain | Evidence source | Version/commit/hash/date | Relevant boundary | Constraints/dependencies | Audit state | GitHub issue | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E0001 | Host edition | This repository's GitLab-origin scaffold | `2b581184d08daed1d0f0b9611fbafbaa0f24e278` | `.gitlab/`, `.gitlab-ci.yml`, GitLab nouns in contracts | GitHub edition must keep process identical so Options B/C remain file splits | Mapped |  | Keep GitLab tree recoverable from this commit; do not mix hosts in-tree |
| E0002 | Host edition | `docs/HOST.md` | working tree | GitHub surface map, non-claims, B/C triggers | Do not start B or C inside an unrelated product slice | Designed |  | Revisit B/C only on named triggers |

Status vocabulary: `Unmapped`, `Mapped`, `Designed`, `Blocked`, `Superseded`.
