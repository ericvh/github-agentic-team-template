#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

cmd=$(sed -n 's/^- Spec-exercise command: `\([^`]*\)`$/\1/p' docs/project-formulation.md | head -n 1)
if [[ -z "$cmd" ]]; then
  echo "missing Spec-exercise command in docs/project-formulation.md" >&2
  exit 1
fi

# The named command is the Designed harness. Missing command fails the job.
# A red domain stub is a failed pipeline, not a skipped job.
bash -lc "$cmd"
