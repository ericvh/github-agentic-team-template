# Proof Ledger

| ID | Claim | Component/artifact | Evidence ids | Current level | Exact proof artifact or command | Explicit non-claims | GitHub issue/PR | Next gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P0001 | Scaffold is a GitHub edition: required GitHub templates, Actions workflow, and host contracts exist; process remains 1:1 with the GitLab origin | `.github/`, `docs/HOST.md`, `scripts/check-scaffold.sh` | E0001, E0002 | Static | `scripts/check-scaffold.sh` and `git diff --check` | Dual-host adapters (B); GitHub-native review/CODEOWNERS/issue forms (C); live `gh` issue/PR loop against a remote |  | Contract/Golden: create issue+draft PR from templates on a GitHub remote |

Use the levels selected from `docs/PROOF_MODEL.md`. A higher level requires an
actual artifact, not only a planned test.
