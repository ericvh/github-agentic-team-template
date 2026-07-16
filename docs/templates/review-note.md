# Independent Review Note

Use one compact note per review pass. Lead with the decision and risk inspected;
keep provenance below the author-facing comments.

```text
Review: <approved | changes requested | blocked>
Focus: <highest-risk behavior, proof, API, security, migration, or operational boundary>

Comments:
- blocker: <risk, evidence, and concrete landing path>
- question: <context required to decide>
- suggestion: <non-blocking improvement or bounded follow-up>
- nit: <optional local polish>
- praise: <specific choice worth retaining>

Tests/proof requested:
- <specific discriminating observation>

Evidence appendix:
- Reviewer role:
- Scope inspected:
- Commands/source refs/report links:
```

Rules:

- Review the change, not the author.
- Compare the issue claim, implementation, runtime behavior, and proof.
- Focus on what could go wrong if the MR landed as-is.
- Ask for tests where they discriminate a material risk or contract.
- Give every blocker a concrete landing path.
- Keep unrelated redesign as a bounded follow-up or decline it.
- Do not self-approve.
