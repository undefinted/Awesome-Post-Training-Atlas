---
name: post-training-atlas
description: Track post-training method evolution across language, reasoning, agents, multimodal, generative, and embodied models; compare what changed between papers; extract transferable research ideas; and turn evidence into careful vibe-coding plans.
---

# Post-Training Atlas

Use this skill when the user wants to understand, compare, update, or build on post-training methods. The primary goal is **method-evolution tracking**, not maximizing a paper count.

## Core outcome

Produce an evidence-grounded map that answers:

1. What method family or pipeline stage is this work changing?
2. What changed relative to the closest prior work?
3. What evidence supports the claimed improvement, and what remains uncertain?
4. Which design ideas appear transferable to another model, task, or modality?

The atlas covers language and reasoning models, agents, VLM/MLLM systems, diffusion or video models, and embodied/VLA systems. Use the repository taxonomy as the navigation layer, not as a claim that every boundary is settled.

## Select a mode

- **Track a method:** build a chronological family timeline and a "what changed" matrix. Read [method-evolution.md](references/method-evolution.md).
- **Find research ideas:** compare compatible mechanisms across families, then propose falsifiable hypotheses and experiments. Read [idea-generation.md](references/idea-generation.md).
- **Support vibe coding:** research first, write a compact evidence brief, then translate it into implementation constraints and a verification plan. Read [vibe-coding.md](references/vibe-coding.md).
- **Use another harness:** keep the Markdown contract and optional query helper; read [harness-interop.md](references/harness-interop.md).
- **Maintain the atlas:** use the repository's radar, labels, rendering, coverage, and test commands; preserve provenance and keep discovery candidates visibly provisional.

## Evidence and freshness rules

- Prefer primary sources: arXiv records, official proceedings or publisher pages, author-maintained project pages, and the paper's official repository.
- Community posts and social media can suggest a search term or popularity signal, but are not sufficient evidence for a paper entry or a method claim.
- Separate publication date, revision date, and venue date. Do not infer a conference acceptance year from an arXiv record.
- Display a venue only when structured academic metadata supports it. Do not guess author institutions, acceptance status, or method ancestry.
- Mark every synthesized statement as one of: **reported by authors**, **observed from comparison**, or **hypothesis/inference**.
- When the user asks for "latest," retrieve fresh primary-source evidence before making claims.

## Repository workflow

When the atlas repository is available, inspect the relevant files before answering:

- `TAXONOMY.md` - inclusion boundaries and primary directions.
- `data/papers.yaml` - curated entries.
- `data/candidates.yaml` - academic discovery candidates; do not treat these as endorsements.
- `config/labels.yaml` - controlled label vocabulary.
- `data/monthly_audit.yaml` and `COVERAGE.md` - direction/month audit state.
- `config/method_families.yaml` - method-family definitions, change axes, and transfer prompts.
- `docs/index.html` - searchable website payload and current UI behavior.

For a maintenance task, prefer the existing commands rather than inventing a parallel pipeline:

```bash
python -m radar.main --days 7
python -m radar.monthly --auto
python -m radar.labels
python -m radar.render --check
python -m radar.coverage --check
python -m unittest discover -s tests
```

Automated discovery creates proposals. Keep curation, rejection, provenance, and review status explicit. Do not silently rewrite curated entries.

Method-evolution fields are optional and should be added only when supported: `method_family`, `predecessors`, `change_axes`, and `transfer_ideas`. Treat a predecessor as a sourced or defensible conceptual precedent, not proof of direct authorship or official lineage.

## Default response shape

For a method question, answer in this order:

1. **Short thesis:** the method's central change.
2. **Timeline:** baseline -> key variants -> current frontier.
3. **Change matrix:** data, objective, feedback/reward, optimization, model/task scope, efficiency.
4. **Evidence and caveats:** reported results, comparison limits, missing evidence.
5. **Transferable ideas:** 2-5 concrete hypotheses, each with a rationale and a test.

For a vibe-coding question, do not jump straight to code. First produce the research brief and implementation contract described in [vibe-coding.md](references/vibe-coding.md), then implement only when the user asks for the change.
