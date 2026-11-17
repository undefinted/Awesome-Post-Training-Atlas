# Codex Paper Radar

The paper radar is intentionally scheduled and curated by Codex rather than by GitHub Actions.

## Cadence

- Scheduled time: **08:00 America/Chicago every day** on the maintainer's local Codex host.
- Runtime requirement: the host must be awake and logged in, and GitHub CLI authentication must be valid.
- Daily lightweight pass: inspect the previous 48 hours of arXiv metadata from `cs.CL`, `cs.LG`, and `cs.AI`.
- Weekly deep pass: review the accumulated candidates, deduplicate them, classify them by direction, and prepare a proposed repository update.
- The daily pass must not edit `data/papers.yaml` or open a pull request.
- The weekly pass may update candidates and open one reviewable pull request after validation.

## Daily pass

1. Search arXiv for post-training terms: SFT, instruction tuning, preference optimization, reward model, RLHF, RLVR, GRPO, verifier, reasoning training, distillation, self-improvement, tool use, agent RL.
2. Exclude pretraining-only, inference-only, generic application, and unrelated modality papers.
3. Deduplicate by arXiv ID, DOI, and normalized title.
4. Append structured records to `data/candidates.yaml` with `status: candidate`.
5. Record the search date, source, query, and a short reason for inclusion.

## Weekly pass

1. Re-check every candidate against the taxonomy in `TAXONOMY.md`.
2. Verify arXiv IDs and paper URLs.
3. Assign direction, subtopic, tags, publication date, key idea, and relation to prior methods.
4. Sort the rendered catalog as direction → year → month → paper.
5. Move only human-reviewed records into `data/papers.yaml`.
6. Run the repository validation and site generation checks.
7. Create one pull request titled `Codex Radar: weekly post-training update`.

## Safety rules

- Never auto-merge a paper into the curated catalog solely from a keyword hit.
- Never replace existing curated metadata without preserving the old value in the PR diff.
- Keep borderline papers in candidates with an explicit rationale.
- Keep GitHub Actions for validation and Pages deployment only; the paper radar workflows are manual fallback workflows.
