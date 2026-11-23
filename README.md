# Awesome Post-Training Atlas

> A structured, continuously updated atlas of post-training research across
> language, reasoning, agents, multimodal models, generative models, and
> embodied intelligence.

**English** · [简体中文](README.zh-CN.md)

[![Codex Radar: daily 08:00 CT](https://img.shields.io/badge/Codex_Radar-daily_08%3A00_CT-10a37f)](CODEX_RADAR.md)
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

The curated layer also carries an optional method-evolution view: method
families, carefully sourced precedents, change axes, and explicit idea surfaces.
The website visualizes these annotations separately from the much larger
discovery pool so provisional records do not look like confirmed lineage.

<!-- PAPERS:START -->
## Research directions

Each direction has its own chronological page. Counts include curated papers and visibly marked academic discovery candidates.
Radar last scanned academic sources: **2026-11-23T08:12:45-06:00**. `Latest paper` is the first-publication date.

| Direction | Curated | Discovery | Total | Latest paper |
|---|---:|---:|---:|---:|
| [Supervised Adaptation & Data](directions/supervised-adaptation.md) | 2 | 3606 | **3608** | 2026-11-20 |
| [Preference Optimization & Alignment](directions/preference-alignment.md) | 6 | 2861 | **2867** | 2026-11-20 |
| [Reward Models & Verifiers](directions/reward-verifiers.md) | 2 | 3377 | **3379** | 2026-11-20 |
| [Reinforcement Learning & RL with Verifiable Rewards](directions/reinforcement-learning.md) | 4 | 849 | **853** | 2026-11-20 |
| [Distillation & Policy Transfer](directions/distillation.md) | 25 | 502 | **527** | 2026-11-20 |
| [Reasoning & Self-Improvement](directions/reasoning-self-improvement.md) | 3 | 864 | **867** | 2026-11-19 |
| [Agentic & Interactive Post-Training](directions/agentic.md) | 3 | 611 | **614** | 2026-11-20 |
| [Multimodal, VLM & MLLM Post-Training](directions/multimodal.md) | 3 | 888 | **891** | 2026-11-20 |
| [Generative Media Post-Training](directions/generative-media.md) | 2 | 438 | **440** | 2026-11-20 |
| [Embodied & VLA Post-Training](directions/embodied-vla.md) | 1 | 434 | **435** | 2026-11-20 |
<!-- PAPERS:END -->

## Codex Paper Radar

Discovery is maintained by a **Codex-operated radar**, rather than a scheduled
GitHub Actions workflow. The maintainer's local Codex task is scheduled for
**08:00 America/Chicago every day**; it requires the host computer to be awake
and its GitHub CLI session to be authenticated.

The operating model is:

1. the daily lightweight pass searches recent primary-source metadata across
   arXiv post-training queries and records traceable candidates;
2. candidates are deduplicated by arXiv ID, DOI, and normalized title, then
   classified into the atlas taxonomy;
3. primary-paper URLs, dates, authors, venue claims, and code links are
   verified before promotion;
4. borderline results remain visibly marked discovery candidates instead of
   entering the curated catalog automatically;
5. a deeper review pass promotes accepted work into `data/papers.yaml` and
   preserves the **direction → year → month → paper** ordering;
6. GitHub Actions workflows remain available as manual validation, rendering,
   and deployment fallbacks; they no longer schedule paper discovery.

The latest recorded run is the
[2026-11-23 Codex radar report](data/codex-radar/2026-11-23.md). Full cadence,
review rules, and safety constraints are documented in
[CODEX_RADAR.md](CODEX_RADAR.md).

To run the repository pipeline manually:

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
