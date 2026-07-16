# GitLab Agentic Team Template

This repository is a reusable operating scaffold for GitLab-driven agentic
engineering teams. It treats each non-trivial issue as a proof-carrying work
slice: one dependency boundary, one coherent behavior change, one observable
proof promotion, one independent review, and one synchronized closeout.

The scaffold is intentionally domain-neutral. Replace the angle-bracketed
project fields, select a semantic slice unit that fits the work, and delete any
ledger or telemetry surface that does not answer a real coordination or proof
question.

## Core Model

```text
Done = implemented
   AND proven
   AND independently reviewed
   AND integrated
   AND durable state synchronized
```

The team has six responsibilities:

1. The orchestrator owns backlog order, authority, and integration.
2. The evidence mapper pins sources and defines the proof plan.
3. Each implementer owns one issue and one disjoint write scope.
4. An independent reviewer tests the claim and highest-risk boundary.
5. The CI/proof owner keeps verification executable and separates
   infrastructure failures from product failures.
6. The state closer reconciles GitLab and checked-in evidence after landing.

One agent may hold several responsibilities across a project, but a slice's
creator and independent reviewer must be distinct.

## Start a Project

1. Copy or fork this repository.
2. Fill [project-formulation.md](docs/project-formulation.md).
3. Replace the mission and authority placeholders in [AGENTS.md](AGENTS.md).
4. Choose the project proof levels in [PROOF_MODEL.md](docs/PROOF_MODEL.md).
5. Remove ledgers that duplicate GitLab without preserving domain evidence.
6. Run `scripts/check-scaffold.sh`.
7. Create milestone `M0 - Bootstrap`, then open the first issue using the
   `work-slice` template.
8. Land one vertical slice before expanding the process or parallel team.

## Repository Surfaces

| Surface | Purpose |
| --- | --- |
| `AGENTS.md` | Repository-wide mission, authority, roles, proof, and closeout contract |
| `.gitlab/` | Human-first issue and merge-request templates |
| `docs/HUMAN_SURFACE.md` | Separates engineering narrative from audit telemetry |
| `docs/WORKFLOW.md` | GitLab lifecycle, labels, milestones, and team orchestration |
| `docs/PROOF_MODEL.md` | Project proof ladder and discriminating evidence rules |
| `docs/ledgers/` | Evidence that cannot be reconstructed reliably from GitLab |
| `docs/templates/` | Detailed plans, reviews, and decision records |
| `skills/` | Narrow project-local agent workflows |
| `scripts/check-scaffold.sh` | Deterministic scaffold validation |

## Default GitLab Labels

```text
kind::<feature|bug|migration|experiment|cleanup|methodology|scaffold>
area::<project-domain>
proof::<none|mapped|static|unit|contract|integration|operational>
status::<planned|active|blocked|review|ready|landed>
review::<needs-independent|changes-requested|approved>
risk::<project-specific-risk>
```

## Default Cadence

- Keep a dependency-ordered horizon of three to five planned issues.
- Review methodology after five landed slices or at milestone close.
- Trigger early review after two repeated blocker or proof-failure families.
- Consider a behavior-preserving cleanup after ten landed slices when the code
  shows concrete structural debt.

These are starting values. Change them to fit project risk and cycle time.

## Validation

```bash
scripts/check-scaffold.sh
git diff --check
```

## Provenance

This scaffold generalizes the operating pattern observed in the internal
`gem5-rs` project at commit
`adf246c7055fab821dde166ba23a5cd0161e12b3`. It deliberately does not copy the
project's approximately-1,000-line audit budget, full telemetry machinery, or
port-specific parity vocabulary as universal requirements.
