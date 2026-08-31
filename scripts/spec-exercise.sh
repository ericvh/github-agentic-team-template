#!/usr/bin/env bash
# Discriminating harness for this template: formulation checks reject an
# unfilled spec-exercise. Feature-green without these negatives is not M0.
set -euo pipefail

cd "$(dirname "$0")/.."
# shellcheck source=scripts/check-spec-exercise.sh
source scripts/check-spec-exercise.sh

tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT

awk '
  /^\| 1 \|/ { print "| 1 |  |  |  |  |  |  |"; next }
  { print }
' docs/project-formulation.md >"$tmp"
if check_spec_exercise_formulation "$tmp" template; then
  echo "spec-exercise: empty rank-1 should fail formulation checks" >&2
  exit 1
fi

awk '!/^- Spec-exercise command:/' docs/project-formulation.md >"$tmp"
if check_spec_exercise_formulation "$tmp" template; then
  echo "spec-exercise: missing command should fail formulation checks" >&2
  exit 1
fi

{
  cat docs/project-formulation.md
  printf '%s\n' '- Project name: `<project-name>`'
} >"$tmp"
if check_spec_exercise_formulation "$tmp" generated; then
  echo "spec-exercise: leftover generated placeholder should fail" >&2
  exit 1
fi

echo "spec-exercise self-test passed: empty rank-1, missing command, and leftover placeholders fail"
