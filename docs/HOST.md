# Host Edition

This scaffold is a **GitHub edition** of a GitLab-originated operating model.
The process (slice, proof, roles, authority, review comment classes, ledgers)
is unchanged. Only the coordination surface, templates, CI wrapper, labels, and
CLI are GitHub-shaped.

Current host: GitHub. Workflow authority: GitHub issues and pull requests.

## Surface Map

Use this table when teaching agents, and keep it stable so a later dual-host
adapter can be a file split rather than a process redesign.

| Process noun | This edition (GitHub) | GitLab origin |
| --- | --- | --- |
| Backlog item | GitHub issue | GitLab issue |
| Change request | Pull request (PR) | Merge request (MR) |
| Draft change | Draft PR | Draft MR |
| Discussion | Issue or PR comment | Issue or MR note |
| Templates | `.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md` | `.gitlab/issue_templates/`, `.gitlab/merge_request_templates/` |
| CI wrapper | `.github/workflows/scaffold.yml` | `.gitlab-ci.yml` |
| Artifacts | Actions artifacts | Job artifacts |
| Host CLI | `gh` | `glab` |
| Project id | `owner/repo` | `namespace/project` |
| Issue id in branches | GitHub issue number | Project-local issue IID |
| Label families | `kind:feature` (flat labels) | `kind::feature` (scoped labels) |
| Review state | Labels `review:*` plus comments | Labels `review::*` plus notes |
| Outcome phases | GitHub milestones | GitLab milestones |

Label families stay `kind`, `area`, `proof`, `status`, and `review`. The
separator is `:` so a later host adapter can map GitHub `kind:feature` to
GitLab `kind::feature` without renaming the family tokens.

GitHub labels are not mutually exclusive. Agents must replace a family value
(`status:active` → `status:landed`) rather than accumulating siblings. Do not
add a label-exclusivity bot in this edition.

Independent review remains label- and comment-based (`review:needs-independent`,
`review:changes-requested`, `review:approved`, plus `docs/templates/review-note.md`
as a PR comment). Native GitHub review states, CODEOWNERS, and required
reviewers are intentionally unused.

## Agent CLI

A2 work on this host uses `gh` for issues, labels, draft PRs, and comments.
Do not add wrapper scripts unless a methodology review names a repeated
failure they would remove.

## Explicit Non-Claims

This edition does not provide:

- a host-neutral core with `docs/hosts/*` adapters;
- GitLab templates or GitLab CI in-tree (recover them from commit
  `2b581184d08daed1d0f0b9611fbafbaa0f24e278` if a dual-host split starts);
- replacing the GitLab edition; that repository stays separate and is not
  this remote;
- YAML issue forms, CODEOWNERS, rulesets, required reviewers, or GitHub
  Projects as workflow authority;
- enforcement that `status`, `proof`, or `review` labels are exclusive.

## Deferred Host Work

### Option B — platform-neutral core and host adapters

Split host-specific paths, CLI, and nouns into `docs/hosts/github.md` and
restore a GitLab adapter from this repository's pre-edition commit. Keep
`AGENTS.md`, skills, proof, and ledgers in host-neutral language.

Reconsider when any of these is true:

- a project needs GitLab and GitHub from the same scaffold;
- host wording in skills or contracts drifts from the process model;
- a second host port would otherwise copy this tree.

### Option C — GitHub-native tightening

Adopt GitHub strengths without changing the slice or proof contracts:

- native PR reviews (APPROVE / REQUEST_CHANGES) as review authority;
- CODEOWNERS and rulesets for no self-merge and required checks;
- YAML issue forms for the work-slice fields;
- optional exclusivity helper for `status` / `proof` / `review`.

Reconsider when any of these is true:

- a ready PR is merged without an independent reviewer;
- `status`, `proof`, or `review` siblings accumulate on one issue;
- humans ask for required reviewers or issue forms after one landed slice.

Do not start B or C inside an unrelated product slice. Either is its own
methodology or scaffold issue.
