#!/usr/bin/env bash
# Spec-exercise formulation checks. Sourced by check-scaffold.sh.
# spec-exercise.sh runs a discriminating self-test against these functions.

check_spec_exercise_formulation() {
  local formulation=${1:-docs/project-formulation.md}
  local mode=${2:-auto}
  local failures=0

  if [[ ! -s "$formulation" ]]; then
    echo "missing or empty formulation: $formulation" >&2
    return 1
  fi

  if [[ "$mode" == auto ]]; then
    if [[ -f README.md ]] && grep -Fq "Generated as an A-Team project" README.md; then
      mode=generated
    else
      mode=template
    fi
  fi

  if ! grep -Fq "Spec-exercise path:" "$formulation"; then
    echo "missing Spec-exercise path in $formulation" >&2
    failures=$((failures + 1))
  fi
  if ! grep -Fq "Spec-exercise command:" "$formulation"; then
    echo "missing Spec-exercise command in $formulation" >&2
    failures=$((failures + 1))
  fi

  local spec_path spec_cmd
  spec_path=$(sed -n 's/^- Spec-exercise path: `\([^`]*\)`$/\1/p' "$formulation" | head -n 1)
  spec_cmd=$(sed -n 's/^- Spec-exercise command: `\([^`]*\)`$/\1/p' "$formulation" | head -n 1)

  if [[ -z "$spec_path" ]]; then
    echo "Spec-exercise path is empty in $formulation" >&2
    failures=$((failures + 1))
  elif [[ ! -s "$spec_path" ]]; then
    echo "missing or empty spec-exercise artifact: $spec_path" >&2
    failures=$((failures + 1))
  fi

  if [[ -z "$spec_cmd" ]]; then
    echo "Spec-exercise command is empty in $formulation" >&2
    failures=$((failures + 1))
  else
    local cmd_file=${spec_cmd%% *}
    if [[ "$cmd_file" == */* ]]; then
      if [[ ! -e "$cmd_file" ]]; then
        echo "spec-exercise command file not found: $cmd_file" >&2
        failures=$((failures + 1))
      fi
    fi
  fi

  if grep -Fq '| 1 |  |  |  |  |  |  |' "$formulation"; then
    echo "First Three Slices rank-1 row is empty in $formulation" >&2
    failures=$((failures + 1))
  fi

  if [[ "$mode" == generated ]]; then
    if grep -Fq '`<project-name>`' "$formulation" \
      || grep -Fq '`<one result a user or operator can observe>`' "$formulation" \
      || grep -Fq '`<namespace/project>`' "$formulation" \
      || grep -Fq '`<owner/repo>`' "$formulation" \
      || grep -Fq '`<one end-to-end behavior>`' "$formulation" \
      || grep -Fq '`<repo/spec/runtime/data/product requirement/bug report>`' "$formulation" \
      || grep -Fq '`<behavior/API/scenario/source interval/migration/hypothesis>`' "$formulation"; then
      echo "generated project still has formulation placeholders in $formulation" >&2
      failures=$((failures + 1))
    fi
  fi

  if (( failures > 0 )); then
    return 1
  fi
  return 0
}
