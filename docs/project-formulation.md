# Project Formulation

Fill this before opening the first implementation issue. Delete examples that do
not fit the project rather than preserving unused process.

## Mission

- Project name: `<project-name>`
- Observable outcome: `<one result a user or operator can observe>`
- GitHub repository: `<owner/repo>`
- Default branch: `main`
- First vertical scenario: `<one end-to-end behavior>`

## Authority

- Default level: `A2`
- Agents may: read named evidence; create scoped issues, branches, commits, and
  draft PRs; run approved verification; update active-slice evidence.
- Human gate: merge, release, deployment, production mutation, external
  communication, destructive history change, secret handling, or wider scope.
- Exceptions: `<explicitly granted or restricted actions>`

Authority levels:

| Level | Agent authority | Typical use |
| --- | --- | --- |
| A0 | Read and report only | sensitive discovery or audit |
| A1 | Create plans and draft issues | early formulation |
| A2 | Create branches, commits, draft PRs, and verification evidence | default engineering work |
| A3 | Mark ready and merge after independent approval and green gates | trusted low/medium-risk project |
| A4 | Release, deploy, or mutate external systems | explicit project-specific authority only |

## Evidence

- Source of truth: `<repo/spec/runtime/data/product requirement/bug report>`
- Versioning rule: `<commit/version/timestamp/dataset hash>`
- Evidence-map owner: `<role>`
- Evidence-map path: `docs/ledgers/evidence-map.md`
- Independent reference required for equality claims: `<yes/no and method>`

## Slicing

- Semantic unit: `<behavior/API/scenario/source interval/migration/hypothesis>`
- Target size: `<range that one implementer and reviewer can bound>`
- Planned backlog horizon: `3-5`
- Parallelism rule: disjoint issues and disjoint write scopes
- Integration rule: predecessor must be landed unless the plan names a stable
  interface and an explicit merge order.

## Proof

- Enabled levels: `mapped, static, unit, contract, integration, operational`
- Required shared gates: `<commands>`
- Required negative evidence: `<rejection/fault/rollback/edge case>`
- Performance claim rule: generated, versioned measurement artifact required
- Proof-ledger owner: `<role>`

## Review

- Creator and reviewer must be distinct: `yes`
- Required approval count: `1`
- Blocking comment classes: `blocker`, decision-critical `question`
- Unresolved blocker policy: PR remains draft or changes-requested
- Human reviewer requirement: `<always/risk-based/agent reviewer acceptable>`
- Review authority in this edition: labels `review:*` and a review-note comment
- Native GitHub reviews / CODEOWNERS / rulesets: deferred (see `docs/HOST.md`)

## GitHub

- Milestone model: `<outcome phases>`
- Branch pattern: `<kind>/<issue-number>-<short-scope>`
- Required label families: `kind`, `area`, `proof`, `status`, `review`
- Label separator: `:` (GitLab origin used `::`; keep family tokens stable)
- Optional label families: `risk`
- Issue/PR workflow authority: GitHub
- Host CLI: `gh`
- Detailed audit location: checked-in report or CI artifact, linked once
- Host edition and deferred B/C work: `docs/HOST.md`

## Cadence

- Methodology review: every `5` landed slices or milestone close
- Early review: `2` repeated blocker/proof/infrastructure failures
- Cleanup consideration: every `10` landed slices when concrete debt exists
- Maximum operating-method changes per normal review: `1`

## Audit and Cost

- PR-local agent report: `off | optional | required`
- Human steering capture: `off | concise GitHub comment | report`
- Context-boundary capture: `off | report`
- Token/cost accounting: `off | diagnostic | required`
- Measurement question: `<why this telemetry changes a decision>`

## First Three Slices

| Rank | Issue | Outcome | Evidence boundary | Proof promotion | Predecessor | Unblocks |
| --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |

Execute only the first slice before deciding whether more process, telemetry, or
parallelism is justified.
