# M0 Spec Exercise

## Claim

`check-scaffold.sh` and the named spec-exercise command reject an unfilled
Designed harness: empty First Three Slices rank-1, missing spec-exercise path
or command, and leftover generator placeholders on a generated project.

## Evidence

- Source: `docs/PROOF_MODEL.md` Designed level; `docs/WORKFLOW.md` M0 exit
- Version: this repository's default branch

## Behavioral contract

- Observable outcome: an unfilled formulation fails local validation and CI.
- Semantic unit: one scaffold validator change and one named harness command.

## Non-claims

- Implementation of a consumer project's first vertical is M1, not this slice.
- Existence of template files is not behavioral proof.

## Discriminating observation

The proof would fail if the implementation used an existence-only file check
because a formulation still containing `<project-name>` or an empty rank-1
slice row would still pass.

## Harness

- Path: `docs/specs/m0-exercise.md`
- Command: `scripts/spec-exercise.sh`
- M0 success: the three negative fixtures fail. A generated project replaces
  this command with a domain harness; a red stub is not yet Designed.

## Write scope

- `scripts/check-scaffold.sh`
- `scripts/check-spec-exercise.sh`
- `scripts/spec-exercise.sh`
- `scripts/run-named-spec-exercise.sh`
- `docs/project-formulation.md`
- `docs/WORKFLOW.md`
- `docs/specs/m0-exercise.md`
- CI config that invokes `scripts/run-named-spec-exercise.sh`

## Out of scope

- Product implementation for a consumer first vertical
