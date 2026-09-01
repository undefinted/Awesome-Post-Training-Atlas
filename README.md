# Awesome Post-Training Atlas

> A structured, continuously updated atlas of post-training research across
> language, reasoning, agents, multimodal models, generative models, and
> embodied intelligence.

[![Paper Radar](https://github.com/undefinted/Awesome-Post-Training-Atlas/actions/workflows/paper-radar.yml/badge.svg)](https://github.com/undefinted/Awesome-Post-Training-Atlas/actions/workflows/paper-radar.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Most paper lists answer *what was published*. This atlas tries to answer three
more useful questions:

1. Which part of the post-training pipeline does the work change?
2. What feedback, data, and optimization mechanism does it use?
3. How does it relate to the methods that came before and after it?

The main index is organized as **direction → year → month → paper**. Within
each month, papers are ordered by publication date. Every entry is generated
from [`data/papers.yaml`](data/papers.yaml), the single source of truth.

## Scope

We use *post-training* broadly but deliberately: methods that adapt, align,
specialize, improve, or evaluate a pretrained foundation model through an
additional learning or feedback loop. The scope includes language models,
VLMs/MLLMs, agents, diffusion and video models, and embodied/VLA systems.

See [TAXONOMY.md](TAXONOMY.md) for inclusion criteria and boundary cases.
The generated [coverage matrix](COVERAGE.md) makes sparse months and directions
visible instead of hiding gaps behind a large total paper count.

## Contents

- [Supervised Adaptation & Data](#supervised-adaptation--data)
- [Preference Optimization & Alignment](#preference-optimization--alignment)
- [Reward Models & Verifiers](#reward-models--verifiers)
- [Reinforcement Learning & RL with Verifiable Rewards](#reinforcement-learning--rl-with-verifiable-rewards)
- [Distillation & Policy Transfer](#distillation--policy-transfer)
- [Reasoning & Self-Improvement](#reasoning--self-improvement)
- [Agentic & Interactive Post-Training](#agentic--interactive-post-training)
- [Multimodal, VLM & MLLM Post-Training](#multimodal-vlm--mllm-post-training)
- [Generative Media Post-Training](#generative-media-post-training)
- [Embodied & VLA Post-Training](#embodied--vla-post-training)

<!-- PAPERS:START -->
## Supervised Adaptation & Data

### 2023

#### October

- **[UltraFeedback: Boosting Language Models with Scaled AI Feedback](https://arxiv.org/abs/2310.01377)** — Builds large-scale fine-grained preference data by having strong models critique and score multiple responses.  
  2023-10-02 · `ai-feedback` · `preference-data` · `synthetic-data`

### 2022

#### December

- **[Self-Instruct: Aligning Language Models with Self-Generated Instructions](https://arxiv.org/abs/2212.10560)** — Bootstraps diverse instruction-following data from a model using filtering before supervised fine-tuning.  
  2022-12-20 · `synthetic-data` · `instruction-tuning` · `self-generation`

## Preference Optimization & Alignment

### 2024

#### May

- **[SimPO: Simple Preference Optimization with a Reference-Free Reward](https://arxiv.org/abs/2405.14734)** — Uses average response log probability as an implicit reward and removes the reference model from preference optimization.  
  2024-05-23 · `reference-free` · `preference-optimization` · `simpo`

#### February

- **[KTO: Model Alignment as Prospect Theoretic Optimization](https://arxiv.org/abs/2402.01306)** — Learns from unpaired desirable and undesirable examples using a prospect-theoretic utility objective.  
  2024-02-02 · `binary-feedback` · `offline` · `kto`

### 2023

#### May

- **[Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290)** — Converts the RLHF objective into a direct classification-style loss over preferred and rejected responses.  
  2023-05-29 · `offline` · `pairwise-preference` · `dpo`

### 2022

#### December

- **[Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073)** — Uses written principles and model-generated critiques to reduce dependence on direct human harmlessness labels.  
  2022-12-15 · `rlaif` · `critique` · `revision` · `constitutional-ai`

#### March

- **[Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155)** — Establishes the SFT-to-reward-model-to-RLHF pipeline for aligning language models with human intent.  
  2022-03-04 · `sft` · `reward-modeling` · `rlhf` · `ppo`

## Reward Models & Verifiers

### 2023

#### May

- **[Let's Verify Step by Step](https://arxiv.org/abs/2305.20050)** — Shows that supervising intermediate reasoning steps can outperform outcome-only reward supervision for mathematical reasoning.  
  2023-05-31 · `process-reward-model` · `verifier` · `reasoning`

## Reinforcement Learning & RL with Verifiable Rewards

### 2025

#### January

- **[DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948)** — Demonstrates that large-scale reinforcement learning with verifiable rewards can elicit and improve long-form reasoning.  
  2025-01-22 · `rlvr` · `grpo` · `reasoning` · `distillation`

### 2024

#### February

- **[DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models](https://arxiv.org/abs/2402.03300)** — Introduces Group Relative Policy Optimization to improve mathematical reasoning without a separate critic model.  
  2024-02-05 · `grpo` · `mathematical-reasoning` · `reinforcement-learning`

### 2017

#### July

- **[Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)** — Introduces a clipped surrogate objective that makes policy-gradient updates simpler and more stable.  
  2017-07-20 · `policy-optimization` · `on-policy` · `ppo`

## Distillation & Policy Transfer

### 2026

#### August

- **[Step-Level On-Policy Distillation: Interpolating Between On-Policy Distillation and Supervised Fine-Tuning](https://arxiv.org/abs/2608.16333)** — Corrects student trajectories at the step level, yielding a continuum between supervised fine-tuning and fully on-policy distillation for interactive agents.  
  2026-08-17 · `on-policy-distillation` · `step-level-guidance` · `sft` · `long-horizon`

- **[SimpleOPD: Simple Tokenizer-Agnostic On-Policy Distillation for Long-Context Reasoning](https://arxiv.org/abs/2608.14277)** — Aligns shared text spans across mismatched teacher and student tokenizers while stabilizing long-context distillation with reference regularization and termination masking.  
  2026-08-14 · `on-policy-distillation` · `tokenizer-alignment` · `long-context` · `reasoning`

- **[AgentOPSD: Recursive Self-Distillation for Agentic Reinforcement Learning](https://arxiv.org/abs/2608.05987)** — Recursively aggregates teacher-student token evidence into turn-level Bayesian credit signals for long-horizon agent training without a separate critic or extra rollouts.  
  2026-08-06 · `on-policy-self-distillation` · `agentic-rl` · `temporal-credit` · `multi-turn` · [code](https://github.com/ZethWang/AgentOPSD)

#### July

- **[Adaptive FastOPD: Progress-Aware Rollout Horizon Expansion for Efficient On-Policy Distillation](https://arxiv.org/abs/2607.29494)** — Expands the student rollout horizon only when learning at the current boundary plateaus, reducing wasted long-horizon sampling.  
  2026-07-31 · `on-policy-distillation` · `adaptive-horizon` · `efficiency` · `multi-turn`

- **[SEED: Self-Evolving On-Policy Distillation for Agentic Reinforcement Learning](https://arxiv.org/abs/2607.14777)** — Converts completed on-policy trajectories into evolving hindsight skills and jointly distills their token-level guidance with outcome reinforcement learning.  
  2026-07-16 · `on-policy-distillation` · `skill-evolution` · `hindsight` · `agentic-rl` · [code](https://github.com/jinyangwu/SEED)

- **[Demystifying On-Policy Distillation: Roles, Pathologies, and Regulations](https://arxiv.org/abs/2607.13399)** — Frames on-policy distillation as an exploration catalyst, diagnoses teacher-student mismatch and length exploitation, and studies clipping and log-compression controls.  
  2026-07-15 · `on-policy-distillation` · `failure-analysis` · `regularization` · `exploration`

- **[TurnOPD: Making On-Policy Distillation Turn-Aware for Efficient Long-Horizon Agent Training](https://arxiv.org/abs/2607.05804)** — Combines adaptive rollout-depth budgeting with a progressive turn-normalized loss to focus learning on useful parts of long agent trajectories.  
  2026-07-07 · `on-policy-distillation` · `turn-aware` · `rollout-budgeting` · `long-horizon`

#### June

- **[OPID: On-Policy Skill Distillation for Agentic Reinforcement Learning](https://arxiv.org/abs/2606.26790)** — Extracts hierarchical hindsight skills from completed student trajectories and combines skill-conditioned token guidance with outcome-based reinforcement learning.  
  2026-06-25 · `on-policy-distillation` · `skill-distillation` · `hindsight` · `agentic-rl`

- **[OPD-Evolver: Cultivating Holistic Agent Evolver via On-Policy Distillation](https://arxiv.org/abs/2606.17628)** — Couples fast hierarchical memory evolution with a slow privileged-hindsight distillation loop so an agent internalizes how to select, use, write, and maintain experience.  
  2026-06-16 · `on-policy-distillation` · `memory` · `experience-evolution` · `agent` · [code](https://github.com/bingreeky/opd-evolver)

- **[On-Policy Distillation with Curriculum Turn-level Guidance for Multi-turn Agents](https://arxiv.org/abs/2606.15912)** — Mixes teacher- and student-generated turns, then gradually removes teacher intervention as the agent becomes capable of completing longer trajectories independently.  
  2026-06-14 · `on-policy-distillation` · `curriculum` · `turn-level-guidance` · `multi-turn`

#### May

- **[Trust Region On-Policy Distillation](https://arxiv.org/abs/2606.01249)** — Restricts distillation to reliable teacher regions using clipping, masking, and forward-KL controls, with optional off-policy guidance outside the trust region.  
  2026-05-31 · `on-policy-distillation` · `trust-region` · `clipping` · `stability`

- **[When Are Teacher Tokens Reliable? Position-Weighted On-Policy Self-Distillation for Reasoning](https://arxiv.org/abs/2605.21606)** — Models teacher-token reliability as position-dependent and increases supervision weight across a generated reasoning trajectory.  
  2026-05-20 · `on-policy-self-distillation` · `token-reliability` · `position-weighting` · `reasoning` · [code](https://github.com/SaFo-Lab/PW-OPSD)

- **[Learning to Foresee: Unveiling the Unlocking Efficiency of On-Policy Distillation](https://arxiv.org/abs/2605.11739)** — Studies why distillation updates anticipate later optimization directions and exploits that structure to extrapolate updates and accelerate training.  
  2026-05-12 · `on-policy-distillation` · `efficiency` · `update-extrapolation` · `analysis`

- **[On-Policy Distillation with Best-of-N Teacher Rollout Selection](https://arxiv.org/abs/2605.09725)** — Selects among multiple teacher rollouts before supervising the student to reduce the effect of incorrect or high-variance teacher trajectories.  
  2026-05-10 · `on-policy-distillation` · `best-of-n` · `rollout-selection` · `teacher-quality`

- **[MAD-OPD: Breaking the Ceiling in On-Policy Distillation via Multi-Agent Debate](https://arxiv.org/abs/2605.01347)** — Replaces a single teacher with a multi-agent debate collective and uses step-level sampling to provide stronger supervision for agentic trajectories.  
  2026-05-02 · `on-policy-distillation` · `multi-agent-debate` · `teacher-ensemble` · `agent`

#### April

- **[Beyond SFT-to-RL: Pre-alignment via Black-Box On-Policy Distillation for Multimodal RL](https://arxiv.org/abs/2604.28123)** — Inserts a black-box response-level distribution-alignment stage between SFT and RLVR using specialized perception and reasoning discriminators.  
  2026-04-30 · `on-policy-distillation` · `distribution-alignment` · `rlvr` · `mixture-of-experts` · [code](https://github.com/XIAO4579/PRISM)

- **[TCOD: Exploring Temporal Curriculum in On-Policy Distillation for Multi-turn Autonomous Agents](https://arxiv.org/abs/2604.24005)** — Progressively expands trajectory depth to control compounding turn errors and stabilize trajectory-level divergence optimization in autonomous agents.  
  2026-04-27 · `on-policy-distillation` · `temporal-curriculum` · `multi-turn` · `agent` · [code](https://github.com/kokolerk/TCOD)

- **[Rethinking On-Policy Distillation of Large Language Models: Phenomenology, Mechanism, and Recipe](https://arxiv.org/abs/2604.13016)** — Identifies compatible reasoning styles and genuinely novel teacher capability as key success conditions, then derives prompt-selection and off-policy cold-start recipes.  
  2026-04-14 · `on-policy-distillation` · `teacher-student-compatibility` · `cold-start` · `analysis`

- **[A Survey of On-Policy Distillation for Large Language Models](https://arxiv.org/abs/2604.00626)** — Organizes on-policy distillation by feedback signal, teacher access, and loss granularity under a unified divergence-based view.  
  2026-04-01 · `on-policy-distillation` · `survey` · `taxonomy` · `knowledge-distillation`

#### March

- **[Revisiting On-Policy Distillation: Empirical Failure Modes and Simple Fixes](https://arxiv.org/abs/2603.25562)** — Diagnoses sampled-token distillation failures and evaluates top-K local support matching, top-p rollouts, and special-token masking as simple remedies.  
  2026-03-26 · `on-policy-distillation` · `failure-analysis` · `support-matching` · `stability`

- **[Scaling Reasoning Efficiently via Relaxed On-Policy Distillation](https://arxiv.org/abs/2603.11137)** — Interprets distillation as policy optimization and relaxes it through mixture-based reward clipping, entropy-aware token sampling, and staged exploration and refinement.  
  2026-03-11 · `on-policy-distillation` · `reward-clipping` · `entropy-sampling` · `efficiency`

- **[Entropy-Aware On-Policy Distillation of Language Models](https://arxiv.org/abs/2603.07079)** — Uses reverse KL on confident teacher tokens and adds forward-KL supervision under high teacher uncertainty to preserve useful output diversity.  
  2026-03-07 · `on-policy-distillation` · `entropy` · `forward-kl` · `reverse-kl`

#### January

- **[Self-Distilled Reasoner: On-Policy Self-Distillation for Large Language Models](https://arxiv.org/abs/2601.18734)** — Uses one model as both privileged-trace teacher and question-only student, matching their token distributions along student-generated reasoning trajectories.  
  2026-01-26 · `on-policy-self-distillation` · `privileged-information` · `reasoning` · `token-level`

## Reasoning & Self-Improvement

### 2024

#### March

- **[Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking](https://arxiv.org/abs/2403.09629)** — Trains models to generate useful internal rationales at arbitrary positions in ordinary text.  
  2024-03-14 · `rationale` · `self-training` · `reasoning`

#### January

- **[Self-Rewarding Language Models](https://arxiv.org/abs/2401.10020)** — Iteratively uses the model itself as an instruction follower and judge to create preference data for further training.  
  2024-01-18 · `self-reward` · `iterative-dpo` · `llm-as-a-judge`

### 2022

#### March

- **[STaR: Bootstrapping Reasoning With Reasoning](https://arxiv.org/abs/2203.14465)** — Iteratively trains on rationales that lead to correct answers and regenerates rationales for failed examples.  
  2022-03-28 · `rationale` · `bootstrapping` · `self-training`

## Agentic & Interactive Post-Training

### 2023

#### February

- **[Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)** — Lets a model generate and filter its own API-call demonstrations, then learns when and how to invoke tools.  
  2023-02-09 · `tool-use` · `self-supervision` · `api`

### 2021

#### December

- **[WebGPT: Browser-assisted question-answering with human feedback](https://arxiv.org/abs/2112.09332)** — Trains a language model to browse the web and answer with citations using demonstrations and human preference feedback.  
  2021-12-17 · `tool-use` · `browsing` · `imitation-learning` · `reward-modeling`

## Multimodal, VLM & MLLM Post-Training

### 2023

#### September

- **[LLaVA-RLHF: Aligning Large Multimodal Models with Factually Augmented RLHF](https://arxiv.org/abs/2309.14525)** — Adds factually grounded preference feedback and RLHF to improve multimodal helpfulness and reduce hallucination.  
  2023-09-25 · `rlhf` · `hallucination` · `multimodal-alignment`

#### April

- **[Visual Instruction Tuning](https://arxiv.org/abs/2304.08485)** — Uses language-model-generated visual instruction data to adapt a vision-language assistant end to end.  
  2023-04-17 · `instruction-tuning` · `synthetic-data` · `vlm`

## Generative Media Post-Training

### 2023

#### November

- **[Diffusion Model Alignment Using Direct Preference Optimization](https://arxiv.org/abs/2311.12908)** — Adapts direct preference optimization to diffusion likelihoods to align image generation without a learned reward model.  
  2023-11-22 · `diffusion` · `preference-optimization` · `dpo`

#### May

- **[Training Diffusion Models with Reinforcement Learning](https://arxiv.org/abs/2305.13301)** — Treats diffusion denoising as a multi-step decision process so image generators can optimize downstream rewards directly.  
  2023-05-22 · `diffusion` · `reinforcement-learning` · `ddpo`

## Embodied & VLA Post-Training

### 2023

#### July

- **[RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818)** — Co-fine-tunes web-scale vision-language knowledge and robot trajectories by expressing actions as tokens.  
  2023-07-28 · `vla` · `co-fine-tuning` · `embodied`
<!-- PAPERS:END -->

## Paper Radar

The repository contains a lightweight discovery agent that:

1. searches the latest 48 hours of arXiv submissions every day;
2. adds Hugging Face Daily Papers popularity and code signals;
3. applies transparent keyword filters and deduplicates known decisions;
4. optionally uses an LLM to judge scope, classify direction, and draft a
   one-sentence key idea;
5. writes candidates to `data/candidates.yaml`;
6. opens a reviewable daily pull request instead of modifying the curated list.

It works without an API key. To enable semantic triage, add `OPENAI_API_KEY`
as a GitHub Actions secret. `OPENAI_MODEL` is optional.

```bash
python -m pip install -r requirements.txt
python -m radar.main --days 7
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
