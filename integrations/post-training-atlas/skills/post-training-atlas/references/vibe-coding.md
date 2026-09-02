# Research-to-vibe-coding workflow

Use this reference when the user wants an AI coding agent to research post-training methods and then modify a project.

## Phase A — research brief

Before editing code, produce:

- the target capability and user-visible outcome;
- the relevant method family and 3–8 primary sources;
- a short “what changed” comparison;
- assumptions, open questions, and evidence gaps;
- the smallest useful implementation slice.

## Phase B — implementation contract

Translate the brief into:

| Item | Required decision |
|---|---|
| Inputs | Data, metadata, prompts, trajectories, or API responses |
| Outputs | Files, UI behavior, reports, or model artifacts |
| Invariants | Provenance, deduplication, labels, safety, reproducibility |
| Non-goals | What will not be implemented in this change |
| Verification | Tests, fixtures, checks, and an evidence review |

Keep research claims separate from implementation decisions. A paper’s result is not automatically a production requirement.

## Phase C — repository-aware execution

- Inspect existing architecture and conventions before adding a new abstraction.
- Reuse the atlas taxonomy, data schema, controlled labels, and radar commands when extending this repository.
- Keep primary-source URLs and retrieval dates with new records.
- Mark automatically discovered records as candidates until reviewed.
- Prefer a small, reversible change and run the project’s tests and reproducibility checks.

## Phase D — report back

End with:

1. what was researched;
2. what was changed;
3. which claims are sourced versus inferred;
4. validation results;
5. known limitations and a safe next step.
