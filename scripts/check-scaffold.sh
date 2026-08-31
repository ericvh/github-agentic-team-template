#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

required_files=(
  AGENTS.md
  README.md
  .github/workflows/scaffold.yml
  .github/ISSUE_TEMPLATE/work-slice.md
  .github/ISSUE_TEMPLATE/methodology-review.md
  .github/PULL_REQUEST_TEMPLATE.md
  docs/project-formulation.md
  docs/HOST.md
  docs/HUMAN_SURFACE.md
  docs/WORKFLOW.md
  docs/PROOF_MODEL.md
  docs/ADOPTION.md
  docs/templates/work-slice-plan.md
  docs/templates/review-note.md
  docs/templates/decision-record.md
  docs/ledgers/evidence-map.md
  docs/ledgers/proof-ledger.md
  docs/ledgers/decision-log.md
  docs/ledgers/experiment-log.md
  docs/ledgers/risk-ledger.md
  docs/ledgers/methodology-ledger.md
  skills/agent-team-evidence-map/SKILL.md
  skills/agent-team-work-slice/SKILL.md
  skills/agent-team-independent-review/SKILL.md
  skills/agent-team-methodology-review/SKILL.md
  docs/specs/m0-exercise.md
  scripts/check-spec-exercise.sh
  scripts/spec-exercise.sh
  scripts/run-named-spec-exercise.sh
)

failures=0

for path in "${required_files[@]}"; do
  if [[ ! -s "$path" ]]; then
    echo "missing or empty: $path" >&2
    failures=$((failures + 1))
  fi
done

required_contracts=(
  "AGENTS.md|Authority Contract"
  "AGENTS.md|Human Surface Contract"
  "AGENTS.md|Team Contract"
  "AGENTS.md|Evidence and Proof Contract"
  "AGENTS.md|Review Contract"
  "AGENTS.md|Methodology Contract"
  "docs/HUMAN_SURFACE.md|Follow-Up Contract"
  "docs/PROOF_MODEL.md|Discriminating Observation"
  "docs/WORKFLOW.md|Work-Slice State Machine"
  "docs/HOST.md|Option B"
  "docs/HOST.md|Option C"
  ".github/ISSUE_TEMPLATE/work-slice.md|Proof Promotion"
  ".github/PULL_REQUEST_TEMPLATE.md|Independent Review"
  "docs/project-formulation.md|Spec-exercise command"
  "docs/WORKFLOW.md|Designed spec-exercise"
)

for check in "${required_contracts[@]}"; do
  path=${check%%|*}
  pattern=${check#*|}
  if ! grep -Fq "$pattern" "$path"; then
    echo "missing contract '$pattern' in $path" >&2
    failures=$((failures + 1))
  fi
done

if [[ -e .gitlab-ci.yml || -d .gitlab ]]; then
  echo "GitLab host files must not ship in this GitHub edition; recover from git history for Option B" >&2
  failures=$((failures + 1))
fi

skill_names_seen=$'\n'
skill_count=0
while IFS= read -r skill; do
  if [[ "$(sed -n '1p' "$skill")" != "---" ]]; then
    echo "skill frontmatter does not start with ---: $skill" >&2
    failures=$((failures + 1))
    continue
  fi

  name=$(sed -n 's/^name: //p' "$skill" | head -n 1)
  description=$(sed -n 's/^description: //p' "$skill" | head -n 1)

  if [[ -z "$name" || -z "$description" ]]; then
    echo "skill missing name or description: $skill" >&2
    failures=$((failures + 1))
  fi

  if [[ -n "$name" ]]; then
    if [[ "$skill_names_seen" == *$'\n'"$name"$'\n'* ]]; then
      echo "duplicate skill name '$name': $skill" >&2
      failures=$((failures + 1))
    fi
    skill_names_seen="${skill_names_seen}${name}"$'\n'
    skill_count=$((skill_count + 1))
  fi
done < <(find skills -mindepth 2 -maxdepth 2 -name SKILL.md -print | sort)

# shellcheck source=scripts/check-spec-exercise.sh
source "$(dirname "$0")/check-spec-exercise.sh"
if ! check_spec_exercise_formulation docs/project-formulation.md auto; then
  failures=$((failures + 1))
fi

if grep -RInE '[[:blank:]]+$' --include='*.md' --include='*.yml' --include='*.sh' .; then
  echo "trailing whitespace found" >&2
  failures=$((failures + 1))
fi

if (( failures > 0 )); then
  echo "scaffold validation failed: $failures problem(s)" >&2
  exit 1
fi

echo "scaffold validation passed: ${#required_files[@]} required files, $skill_count skills"
