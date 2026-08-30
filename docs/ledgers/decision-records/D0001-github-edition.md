# Decision Record

- ID: D0001
- Date: 2026-08-30
- Status: Accepted
- Decision: Convert this scaffold to a GitHub edition (Option A) while
  preserving a later dual-host split (Option B) and GitHub-native tightening
  (Option C) as bounded follow-ups.

## Context

The operating model (slice, proof, roles, authority, review classes, ledgers)
does not depend on GitLab. The coordination surface, templates, CI wrapper,
labels, and CLI did. The project needed a GitHub-usable tree without collapsing
the process into GitHub-only enforcement that would have to be ripped out to
support GitLab again.

## Options

| Option | Benefits | Costs and risks |
| --- | --- | --- |
| A. GitHub edition, process-identical | Fastest usable GitHub tree; agents open the right UI | Two future ports instead of one adapter; GitHub labels are not exclusive |
| B. Host-neutral core + adapters now | One process tree for GitLab and GitHub | Extra abstraction before any GitHub user exists; wider slice |
| C. GitHub-native tightening now | Stronger no-self-merge and issue forms | Couples process to GitHub reviews/CODEOWNERS; blocks a clean B split |

## Outcome

A won because the immediate need is a GitHub coordination surface, not two
hosts or GitHub-native enforcement. B and C stay explicit non-claims with
revisit triggers in `docs/HOST.md`.

Preserved for B/C:

- family tokens `kind`, `area`, `proof`, `status`, `review` (separator only
  changed `::` → `:`);
- markdown templates rather than YAML issue forms;
- label-based review authority rather than CODEOWNERS/required reviewers;
- no label-exclusivity bot;
- GitLab origin tree left intact at
  `2b581184d08daed1d0f0b9611fbafbaa0f24e278`.

## Verification

```bash
scripts/check-scaffold.sh
git diff --check
```

Discriminating observation: the validator fails if `.gitlab-ci.yml` or
`.gitlab/` templates are required, and fails if `docs/HOST.md` lacks Option B
and Option C follow-up text. A copied GitLab path would not pass.

## Revisit When

- Option B: a project needs GitLab and GitHub from the same scaffold; host
  wording drifts from the process model; or a second host port would copy this
  tree.
- Option C: a ready PR merges without an independent reviewer; `status` /
  `proof` / `review` siblings accumulate; or humans ask for required reviewers
  or issue forms after one landed slice.
