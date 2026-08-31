# Adoption Guide

Adopt the mechanism in stages. Copying every visible control before the project
has produced evidence creates process without continuity.

## Stage 1: One Proof-Carrying PR

- Fill the project formulation, including spec-exercise path and command.
- Land the Designed spec-exercise before the first vertical implementation.
- Customize `AGENTS.md`, one issue template, one PR template, and CI.
- Define the evidence anchor, proof ladder, and independent-review rule.
- Land one vertical behavior through the complete issue-to-closeout loop.

Exit test: a new agent can explain the landed claim and next issue without the
original chat.

## Stage 2: A Real Agent Team

- Use orchestrator, evidence mapper, implementer, reviewer, CI/proof owner, and
  state closer responsibilities.
- Maintain a short dependency-ordered GitHub horizon.
- Add only the ledgers needed to preserve evidence that GitHub and code do not.
- Permit parallel work after issue and write scopes are disjoint.

Exit test: two independent slices can proceed without conflicting edits or
ambiguous integration order.

## Stage 3: Self-Correcting Operations

- Review methodology after landed work and repeated failure signals.
- Add behavior-preserving cleanup when evidence shows structural debt.
- Add compact agent-loop or cost telemetry only for a named measurement
  question.
- Automate repeated CI, evidence generation, or state reconciliation.

Exit test: the project removes or repairs a recurring failure without making the
human GitHub surface harder to read.

## Do Not Copy Literally

- A source-line budget: choose a project-specific semantic unit.
- A five-item backlog: use the shortest horizon that preserves continuity.
- Fixed review and cleanup counts: tune to risk and cycle time.
- Every possible ledger: retain domain evidence, not duplicated workflow state.
- Token/session telemetry: enable only when it changes a cost or continuity
  decision, and keep it PR-local.
- A local runner fallback: add only after runner availability repeats as a real
  constraint.
- Parity vocabulary: use requirement, compatibility, migration, regression,
  experiment, security, or operational fitness language that fits the project.
- Host-native GitHub tightening (CODEOWNERS, YAML issue forms, required
  reviewers, label bots): those are Option C in `docs/HOST.md`, not Stage 1.
