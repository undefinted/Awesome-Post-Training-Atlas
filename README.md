# Awesome Post-Training Atlas

> A structured, continuously updated atlas of post-training research across
> language, reasoning, agents, multimodal models, generative models, and
> embodied intelligence.

[![Paper Radar](https://github.com/undefinted/Awesome-Post-Training-Atlas/actions/workflows/paper-radar.yml/badge.svg)](https://github.com/undefinted/Awesome-Post-Training-Atlas/actions/workflows/paper-radar.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🔎 **[Open the searchable research website](https://undefinted.github.io/Awesome-Post-Training-Atlas/)** · [Browse the controlled label directory](LABELS.md)

Most paper lists answer *what was published*. This atlas tries to answer three
more useful questions:

1. Which part of the post-training pipeline does the work change?
2. What feedback, data, and optimization mechanism does it use?
3. How does it relate to the methods that came before and after it?

The main index is organized as **direction → year → month → paper**. Within
each month, papers are ordered by publication date. Curated entries come from
[`data/papers.yaml`](data/papers.yaml); direct academic-search results from
[`data/candidates.yaml`](data/candidates.yaml) appear on the direction pages
with a visible 🔎 `discovery candidate` marker until their primary papers are reviewed.

## Scope

We use *post-training* broadly but deliberately: methods that adapt, align,
specialize, improve, or evaluate a pretrained foundation model through an
additional learning or feedback loop. The scope includes language models,
VLMs/MLLMs, agents, diffusion and video models, and embodied/VLA systems.

See [TAXONOMY.md](TAXONOMY.md) for inclusion criteria and boundary cases.
The generated [coverage matrix](COVERAGE.md) makes sparse months and directions
visible instead of hiding gaps behind a large total paper count.
The [discovery coverage report](DISCOVERY_COVERAGE.md) separately records the
academic-search window, query counts, and unresolved backlog.

<!-- PAPERS:START -->
## Research directions

Each direction has its own chronological page. Counts include curated papers and visibly marked academic discovery candidates.

| Direction | Curated | Discovery | Total | Latest |
|---|---:|---:|---:|---:|
| [Supervised Adaptation & Data](directions/supervised-adaptation.md) | 2 | 2398 | **2400** | 2026-08-31 |
| [Preference Optimization & Alignment](directions/preference-alignment.md) | 5 | 2134 | **2139** | 2026-08-31 |
| [Reward Models & Verifiers](directions/reward-verifiers.md) | 1 | 1612 | **1613** | 2026-08-31 |
| [Reinforcement Learning & RL with Verifiable Rewards](directions/reinforcement-learning.md) | 3 | 490 | **493** | 2026-08-31 |
| [Distillation & Policy Transfer](directions/distillation.md) | 23 | 151 | **174** | 2026-08-31 |
| [Reasoning & Self-Improvement](directions/reasoning-self-improvement.md) | 3 | 436 | **439** | 2026-08-31 |
| [Agentic & Interactive Post-Training](directions/agentic.md) | 2 | 310 | **312** | 2026-08-31 |
| [Multimodal, VLM & MLLM Post-Training](directions/multimodal.md) | 2 | 474 | **476** | 2026-08-31 |
| [Generative Media Post-Training](directions/generative-media.md) | 2 | 253 | **255** | 2026-08-31 |
| [Embodied & VLA Post-Training](directions/embodied-vla.md) | 1 | 211 | **212** | 2026-08-30 |
<!-- PAPERS:END -->

## Paper Radar

The repository contains complementary discovery and curation agents:

1. the Daily Radar searches 31 direction-specific arXiv queries with pagination
   and adds Hugging Face Daily Papers popularity and code signals;
2. the Direction-Month Coverage Radar audits every direction × month cell
   directly on arXiv, records exact queries, scan limits, counts, and failures,
   then rebuilds all chronological pages and the website in its pull request;
3. the historical Backfill Radar walks paginated arXiv results over a declared
   date range and persists a cursor for every taxonomy query;
4. candidate slots are balanced per direction so a high-volume topic cannot
   starve multimodal, agentic, generative-media, or embodied work;
5. all agents deduplicate curated, rejected, and already queued records and
   preserve the academic query and primary-source provenance;
6. a controlled-vocabulary extractor assigns auditable labels such as OPD,
   OPSD, counterfactual, distillation, RLVR, agent, VLM, and VLA; the website
   supports ANY/ALL multi-label filtering together with year and month;
7. an optional LLM judges scope, classifies direction, and drafts a
   one-sentence key idea;
8. each run opens a reviewable pull request instead of silently modifying the
   curated list.

It works without an API key. To enable semantic triage, add `OPENAI_API_KEY`
as a GitHub Actions secret. `OPENAI_MODEL` is optional.

```bash
python -m pip install -r requirements.txt
python -m radar.main --days 7
python -m radar.backfill --max-new 180
python -m radar.labels
python -m radar.render --check
python -m radar.coverage --check
python -m unittest discover -s tests
```

See [SOURCES.md](SOURCES.md) for source tiers, freshness targets, and the
policy for Chinese and international community signals.

## Contributing

Please use the paper proposal issue template or edit `data/papers.yaml`. A good
entry states why the paper belongs in post-training, not merely that it uses a
foundation model. Automated candidates are proposals, not endorsements.

## Acknowledgements

This project is inspired by the research community's many excellent paper
lists. Its specific focus is a cross-modality taxonomy, chronological reading
paths inside each direction, and a human-reviewed discovery pipeline.
