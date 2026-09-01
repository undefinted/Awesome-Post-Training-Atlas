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
each month, papers are ordered by publication date. Curated entries come from
[`data/papers.yaml`](data/papers.yaml); direct academic-search results from
[`data/candidates.yaml`](data/candidates.yaml) are also shown with a visible
🔎 `discovery candidate` marker until their primary papers are reviewed.

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

### 2026

#### August

- 🔎 **[Sequential Trajectories and Simultaneous Blending: Multi-Emotion Modeling for Instruction-Following TTS](https://arxiv.org/abs/2608.30325)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Post-Training VLMs for Video Mistake Detection](https://arxiv.org/abs/2608.28406)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Retrieval Heads Meet Vision: Uncovering How VLMs Locate and Extract Visual Information](https://arxiv.org/abs/2608.27417)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[TailSFT: Filtered Fine-Tuning Improves Post-Training Performance](https://arxiv.org/abs/2608.25756)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[DCGC: Draft-Conditioned Global Correction for Complex Reasoning with Masked Diffusion Models](https://arxiv.org/abs/2608.25428)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Unfolding Scientific Papers into Multi-Turn Generation Trajectories for Continued Pre-Training](https://arxiv.org/abs/2608.25826)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[From Specialization to Generalization: Instruction-tuned LLMs for Robust Harmful Content Mitigation](https://arxiv.org/abs/2608.25605)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Beyond Static Interpretability: Anticipating Post-SFT Mechanisms from Pre-SFT Parameters for Better Tuning](https://arxiv.org/abs/2608.24482)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Flower Hub: A Reproducible Benchmarking Platform for Federated Learning in Simulation and Deployment](https://arxiv.org/abs/2608.25114)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[PROOF-Gen: From Optimized Data to Better Distillation](https://arxiv.org/abs/2608.23911)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Manifold Drift in Flow Preference Optimization: A Root Cause of Reward Hacking](https://arxiv.org/abs/2608.20011)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-20 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SignalReasoner: Assessing the Upper Bound of 3B Models for Signal Mathematical Reasoning](https://arxiv.org/abs/2608.17301)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-18 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[REChart: Reasoning-Efficient Chart Editing with Large Reasoning Models](https://arxiv.org/abs/2608.17414)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-18 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Geo-VLA: Geometry-Aware Vision-Language-Action Planning via Internalization of Map Semantics](https://arxiv.org/abs/2608.21440)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-18 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[TransAnyText: Translating Arbitrary Text in E-commerce Images via Structured Visual Generation](https://arxiv.org/abs/2608.16284)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-17 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Palmyra x6 Technical Report: An Agentic, Tool-Use Model Post-Trained via Anchored Supervised Fine-Tuning](https://arxiv.org/abs/2608.16620)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-17 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Listen, Reason, and Segment: Aligning LALMs with Editorial Judgment for Media Chapterization](https://arxiv.org/abs/2608.16539)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-17 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[HarmTrace: Anchor-Calibrated Decoupled Optimization for Fine-Grained Target Identification in Harmful Memes](https://arxiv.org/abs/2608.16622)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-17 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SQuad: Sub-Quadratic Attention Distillation for Efficient Video Generation](https://arxiv.org/abs/2608.16585)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-17 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Ask to Be Sure: Informative Interactions for Confident Multi-Turn LLM Recommendation](https://arxiv.org/abs/2608.15949)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[AlloEgo-VLM: Disambiguating Allocentric and Egocentric Reference Frames in Vision-Language Models](https://arxiv.org/abs/2608.15605)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Do Language Models Consistently Encode the Current Year?](https://arxiv.org/abs/2608.15507)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SEER: Long-Context Reasoning via Selective Visual-Text Compression](https://arxiv.org/abs/2608.15962)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[How Language Models Choose Sides: Internal Representations of Instruction Hierarchy](https://arxiv.org/abs/2608.28648)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[OTel: Building Domain-Specialized Telecom LLM Foundations for Intelligent Networks](https://arxiv.org/abs/2608.15436)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-15 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[MetaReason: Precise Interleaved Multimodal Reasoning via Editing Meta Information for Solving Geometry Problems](https://arxiv.org/abs/2608.15006)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-15 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[MoE Router-Guided Clustering for Heterogeneous Federated Instruction Tuning](https://arxiv.org/abs/2608.15311)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-15 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[APTER: Adaptive Post-Training with Expert-Grounded Rubrics](https://arxiv.org/abs/2608.14212)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-14 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[MathForm: Scaling Mathematical Autoformalization with Knowledge Retrieval and Verification-Guided Refinement](https://arxiv.org/abs/2608.14221)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-14 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Act2Intention: A Benchmark For Developing Active Mobile Agents Through Inferring User Intention from GUI Actions](https://arxiv.org/abs/2608.14132)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-14 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Intern-S2-Preview: Scientific Agentic Foundation Model](https://arxiv.org/abs/2608.13505)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-13 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Spatial Memory Agent: Experience-Grounded Procedure Memory for Spatial Intelligence](https://arxiv.org/abs/2608.12743)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-13 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[HPSD: Hybrid-Policy Self-Distillation for Text-Image-to-Video Diffusion Models](https://arxiv.org/abs/2608.13205)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-13 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[AdsWorldEngine: A Self-Evolving Conversational Advertising Agent through Orchestrator and Tool Coevolution](https://arxiv.org/abs/2608.13833)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-13 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[HiRoute: Hierarchical Routed Prompt Tuning for Safety Alignment of Large Language Models](https://arxiv.org/abs/2608.12821)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-13 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Are You Sure You're Sure? On the Impact of Instruction Tuning on Confidence and Lexical Diversity](https://arxiv.org/abs/2608.13430)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-13 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[LongEarth-R1: Benchmarking and Aligning Vision-Language Models for Long-Horizon Earth Observation Reasoning](https://arxiv.org/abs/2608.13344)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-13 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[EEG-PRIME: Prototype-Aligned Representation Learning with Multi-Level Conditioning for EEG Decoding](https://arxiv.org/abs/2608.13072)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-13 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Learning from Unreachable Rewards: Hint-Conditioned Reinforcement Learning for Generative Recommendation](https://arxiv.org/abs/2608.11980)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-12 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[When the API Speaks the Wrong Language: Revisiting Post-Training for Multilingual Tool Use](https://arxiv.org/abs/2608.11715)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-12 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[CLAIM: Leading Open-domain Active Clarification of Large Language Models with Uncertainty Measurement](https://arxiv.org/abs/2608.11631)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-12 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[From Visual Widgets to UI Code: Efficient Tool-Grounded Generation](https://arxiv.org/abs/2608.12611)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-12 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[MBA: Multimodal Benchmark and Agents for Real-World Business Ideation](https://arxiv.org/abs/2608.11616)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-12 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Reference-Free Post-Training of Open Large Language Models for Multilingual Machine Translation](https://arxiv.org/abs/2608.10812)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Calibrating Post-Training Feature Shifts for LLM Data Contamination Detection](https://arxiv.org/abs/2608.10462)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Self-Evolving Embodied Agents via Skill-Harness Evolution](https://arxiv.org/abs/2608.11350)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[MIRA: Medical Image Reflection for Agentic Diagnosis](https://arxiv.org/abs/2608.10827)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[FADE: From Passive Verification to Active Discovery in Counterfactual Video Understanding](https://arxiv.org/abs/2608.10764)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[When Self-Consistency Backfires: Majority Vote Hurts the Majority of Hard Science Problems for Small LLMs](https://arxiv.org/abs/2608.11403)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Self-Knowledge Retrieval Augmented Generation Framework for Patent Matching](https://arxiv.org/abs/2608.11030)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[ThinkAfford: Affordance-Centric Reasoning for Fine-Grained 3D Grounding in Cluttered Scenes](https://arxiv.org/abs/2608.10981)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[CARE: Confidence-Aware Reasoning for Reliable Medical VQA](https://arxiv.org/abs/2608.10964)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Motif 3: Technical Report](https://arxiv.org/abs/2608.09119)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[MedPixel: A Unified Pixel-Language Model for Medical Reasoning and Segmentation](https://arxiv.org/abs/2608.09818)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[CHORUS: Complementary Experts for High-Coverage Testbench Stimulus Generation](https://arxiv.org/abs/2608.10090)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[FactorDrive: Adaptive Multi-Step Reasoning Driven by Planning-Critical Factors for End-to-End Autonomous Driving](https://arxiv.org/abs/2608.09591)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[ZetaGPT: A Reference Implementation of Positional--Encoding--Free State--Space--Attention Language Models](https://arxiv.org/abs/2608.09432)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SoftmaxGRPO: Learning to Reason using Softmax Advantage Group Estimation](https://arxiv.org/abs/2608.09271)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[DistMoE: Private-data Rehearsal-free Routing in Mixture-of-Experts for Distributed Instruction Tuning](https://arxiv.org/abs/2608.09907)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Intent Speaks Louder: Controllable User Simulation Beyond Response Imitation](https://arxiv.org/abs/2608.09420)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Financial Numerical Prediction and Allocation as Token Generation](https://arxiv.org/abs/2608.09880)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Listwise Cross-Encoder Fine-Tuning vs. Agentic Instruction Tuning for LLM Rerankers: A Systematic Study in Medical Procedure Reranking](https://arxiv.org/abs/2608.09650)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Visual Distortion Detection in UGC Images Using Large Multimodal Models](https://arxiv.org/abs/2608.09122)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Diagnosing as Cardiologists Do: ECG Agents with Doctor-Grounded Priors for Clinical Reasoning Across Diseases and Populations](https://arxiv.org/abs/2608.09053)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Linguistically-Aligned and Visually-Grounded Preference Optimization for Clinically-Augmented Medical Report Generation](https://arxiv.org/abs/2608.08494)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-09 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Domain Agnostic Text Redaction from Natural Language Rules using Instruction Tuning](https://arxiv.org/abs/2608.14693)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-09 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[NeuPAT: Neuron-aware Plasticity Allocation Tuning for Language-Preserving MLLMs](https://arxiv.org/abs/2608.08107)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-08 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Distilling Physical Priors into Streaming World Models](https://arxiv.org/abs/2608.07981)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-08 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[TEMPO: Semantic-Action Decoupled RL Post-Training for Vision-Language-Action Models](https://arxiv.org/abs/2608.07314)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-07 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Retrieval-Constrained Policy Optimization for Attack Technique Extraction from Cyber Threat Intelligence](https://arxiv.org/abs/2608.06778)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-07 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Glance, Scrutinize, and Think: Advancing Video Anomaly Detection from Training-Free to Agentic Reasoning](https://arxiv.org/abs/2608.11260)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-07 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SciQNet: Two-Stage Multimodal Adaptation for Scientific Image Quality Assessment](https://arxiv.org/abs/2608.05691)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[StepReflect: Structured UI Transition Reflection for Mobile GUI Agents](https://arxiv.org/abs/2608.05587)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[State2State: Environment-Derived Mid-Training for LLM Agents](https://arxiv.org/abs/2608.04934)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-05 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[OctoLong: Mid-Training On Cross-Repository Code Contexts Enhances Long-Context Modeling](https://arxiv.org/abs/2608.05141)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-05 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Spoken Function Calling: A New Perspective on Spoken Language Understanding for Large Audio Language Models](https://arxiv.org/abs/2608.05126)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-05 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Hierarchical Data Selection via Manifold Coverage and Sparse Feature Coverage in LLM Post-training](https://arxiv.org/abs/2608.16927)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-05 · `academic-query-vote` · `arxiv-backfill`

### 2023

#### October

- **[UltraFeedback: Boosting Language Models with Scaled AI Feedback](https://arxiv.org/abs/2310.01377)** — Builds large-scale fine-grained preference data by having strong models critique and score multiple responses.  
  2023-10-02 · `ai-feedback` · `preference-data` · `synthetic-data`

### 2022

#### December

- **[Self-Instruct: Aligning Language Models with Self-Generated Instructions](https://arxiv.org/abs/2212.10560)** — Bootstraps diverse instruction-following data from a model using filtering before supervised fine-tuning.  
  2022-12-20 · `synthetic-data` · `instruction-tuning` · `self-generation`

## Preference Optimization & Alignment

### 2026

#### August

- 🔎 **[Scaling Large Reasoning Models beyond Human Supervision: A Path toward Superintelligence](https://arxiv.org/abs/2608.31075)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[PLC-DPO: Posterior Label Correction in Noisy and Ambiguous Preference Optimization](https://arxiv.org/abs/2608.30597)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Balancing Privacy, Utility, and Safety in LLM Alignment through Preference Optimization](https://arxiv.org/abs/2608.30141)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[PaperBanana-Interact: Scientific Diagram Refinement with Multi-Turn Human Feedback](https://arxiv.org/abs/2608.30241)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Co-Evolving Actor-Conditioned Critics for Non-Verifiable Generation](https://arxiv.org/abs/2608.30397)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Thesis Proposal: Toward a Human-Centered and Perspective-Aware Framework for Reproducible ML Evaluation and AI Alignment](https://arxiv.org/abs/2608.30842)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Arabic Safety Alignment as Selective Refusal: An Empirical Study of SFT, DPO, and Guard Calibration](https://arxiv.org/abs/2608.29378)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-29 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Locked at the Entrance, Open Inside: Where RLVR Narrows the Solution Space](https://arxiv.org/abs/2608.29188)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-29 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[STAR : Sentence Translation Alignment Rate for Document-to-Document Machine Translation](https://arxiv.org/abs/2608.27161)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Disentangling Optimization Scale from Preference Scale in DPO](https://arxiv.org/abs/2608.27032)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[INSPIRE: An Internalize-Then-Improve Approach for Example-Driven Mathematical Reasoning](https://arxiv.org/abs/2608.27501)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Preference Optimization for Non-Verbal Vocalization Synthesis](https://arxiv.org/abs/2608.24163)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Improving Cross-Problem Vehicle Routing with Locally Augmented Preferences and Representation Disentanglement](https://arxiv.org/abs/2608.24859)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Algorithmic Impact Reveals the Hidden Social Choice Structure of Alignment](https://arxiv.org/abs/2608.24046)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Preference Data Selection for Mitigating the Alignment Tax in Large Language Models](https://arxiv.org/abs/2608.24192)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[MoPLEx: Estimating Plackett-Luce Mixture Models for Multi-Objective Alignment](https://arxiv.org/abs/2608.25200)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[CAFE: Self-Improving Search Agents Need Co-Evolving Feedback](https://arxiv.org/abs/2608.24794)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Neurosymbolic Alignment for Physiologically-Safe Clinical Language Models](https://arxiv.org/abs/2608.24534)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[NeurRAFT: Robot Motion Planning via Anchor-Level Flow Matching with Clearance-Aware Preference Tuning](https://arxiv.org/abs/2608.24026)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Can We Perform Online RL for Image Editing without Editing Rewards?](https://arxiv.org/abs/2608.22780)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Function-Level Execution Feedback for Code Preference Optimization](https://arxiv.org/abs/2608.23632)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-23 · `academic-query-vote` · `arxiv-backfill`

#### July

- 🔎 **[SciForma: Structure-Faithful Generation of Scientific Diagrams](https://arxiv.org/abs/2607.18091)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-20 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Diversity-Oriented Fine-Tuning for Uncertainty-Based Hallucination Detection](https://arxiv.org/abs/2607.16643)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-18 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[When Physical Preferences Meet Semantic Constraints: Physical and Semantic Direct Preference Optimization for Text-to-Video Generation](https://arxiv.org/abs/2607.16947)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-18 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[RIMS: Preference Optimization via Smoothed Multi-pair Aggregation for Small-Scale LLM Retrieval-Augmented Generation](https://arxiv.org/abs/2607.16431)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-17 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[TD-DPO: Difference-Aware Preference Optimization for Mitigating Sycophancy in Clinical Autism Intervention Dialogue](https://arxiv.org/abs/2607.18304)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-17 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Digital Pantheon: Simulating and Auditing Coalition Formation with LLM Agents](https://arxiv.org/abs/2607.15095)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Step-Level Preference Learning for Generative Agents in Social Simulations](https://arxiv.org/abs/2607.14485)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Exploring Post-Training Alignment of Small Language Models for Biomedical Data-to-Text Generation: A Case Study of Medication Leaflet](https://arxiv.org/abs/2607.13430)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-15 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Groc-PO: Grounded Context Preference Optimization for Truthful Multimodal LLMs](https://arxiv.org/abs/2607.13712)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-15 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Improving Text-to-Audio Instruction Following via Fine-Grained Feedback from Audio-Aware Large Language Models](https://arxiv.org/abs/2607.13408)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-15 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Meta-Learning Preferences for Multilingual LLM Alignment](https://arxiv.org/abs/2607.13315)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-14 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SARFA: Segment Anything with Radiomic Feature Alignment](https://arxiv.org/abs/2607.13323)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-14 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[DeepBias: Adaptive In-depth Probing of Social Biases in LVLMs](https://arxiv.org/abs/2607.11228)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-13 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Agentic-DPO: From Imitation to Agentic Policy Optimization on Expert Trajectories](https://arxiv.org/abs/2607.10601)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-12 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Ontology-Amplified Distillation and Contextuality Auditing for Sovereign Enterprise Language Models: A Combined Proof-of-Mechanism and Negative-Results Method Study](https://arxiv.org/abs/2607.11948)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Breaking the Quality--Intelligibility Trade-off in Streaming Target Speaker Extraction via Deep-Feature-Anchored Preference Optimization](https://arxiv.org/abs/2607.10191)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Index SLM Technical Report](https://arxiv.org/abs/2607.09885)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Metadata-Free Meta-Reweighted Direct Preference Optimization under Noisy Preference Labels](https://arxiv.org/abs/2607.09796)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-09 · `academic-query-vote` · `arxiv-backfill`

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

### 2026

#### August

- 🔎 **[Reconciling Process Supervision with Outcome-Based Credit in Agentic Policy Optimization](https://arxiv.org/abs/2608.31077)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[HSRM: Hidden-State Reward Models for Test-Time Verification](https://arxiv.org/abs/2608.30841)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[VIBE: Video Instruction-aligned Background music gEneration](https://arxiv.org/abs/2608.30125)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Mitigating Over-Optimization in PRM-Guided Search in Mathematical Reasoning by Optimizing the Guide](https://arxiv.org/abs/2608.30051)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Small Language Models as Judges for Rubric-Based Reinforcement Learning](https://arxiv.org/abs/2608.30005)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Adaptive Doubly Robust Off-Policy Evaluation for Ranking Policies under Diverse User Behavior](https://arxiv.org/abs/2608.29600)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[The Nearest Target Is the Wrong One: Target Separation in Arc2Face Identity Unlearning](https://arxiv.org/abs/2608.30087)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[XQDT: eXplainable and Quantitative Data-Text Alignment Metric with Feedback Signals](https://arxiv.org/abs/2608.29948)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SkillForge: Compositional Skill Synthesis with Verification-in-the-Loop for Generating Formally Verified Dafny Programs](https://arxiv.org/abs/2608.29841)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[RAGDiffusion++: From Macro-Retrieval to Micro-Fidelity Alignment for Garment Generation](https://arxiv.org/abs/2608.29280)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-29 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Learning to Follow In-Context Watermark Instructions via Self-Distillation](https://arxiv.org/abs/2608.29030)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-29 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Beyond Correctness: Validity-Oriented Evaluation of Biomedical LLM Judges](https://arxiv.org/abs/2608.29127)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-29 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Asymmetric Phase Coding Video Watermarking](https://arxiv.org/abs/2608.29212)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-29 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Acquire, Repair, Preserve: A Diagnosis-Guided Post-Training Recipe for Small-Model Dialogue Game Agents](https://arxiv.org/abs/2608.28458)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Beyond the Answer Key: Robustness Evaluation of Large Language Models for Step-Level Mathematical Verification](https://arxiv.org/abs/2608.28725)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Pro-Router: Token-Aware Progressive Model Routing with Adaptive Edge-Cloud Collaboration for Efficient Multimodal LLM Inference](https://arxiv.org/abs/2608.28726)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Moving the Mean Toward the Known Good, Not Beyond It: What Inference-Time Interventions and Weight Consolidation Buy in Open-Ended Generation](https://arxiv.org/abs/2608.28886)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[JudgeStealer: Extracting LLM Judging Capabilities across Evaluation Protocols](https://arxiv.org/abs/2608.26982)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Equal Ranking Quality, Different Decisions: Training Order-Consistent LLM Scorers](https://arxiv.org/abs/2608.26762)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Understanding Evolution Strategies for LLM Reasoning: Broader Reasoning Coverage than GRPO](https://arxiv.org/abs/2608.27351)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Circuit Condensation: Post-Training that Concentrates a Behavior's Causal Circuit](https://arxiv.org/abs/2608.27254)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Safety Does Not Compose: Non-Decaying Loop State for Autonomous LLM Agents](https://arxiv.org/abs/2608.27141)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[BekchiAI: Measuring, Observing, and Controlling LLM Agents in One Click](https://arxiv.org/abs/2608.26867)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Privacy Without Regret: Differentially Private Inference-Time Alignment](https://arxiv.org/abs/2608.26324)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SpeechGym: An Audio-Native Gym for Training Voice Agents via Reinforcement Learning](https://arxiv.org/abs/2608.26432)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Knowledge-Verified Emergent Deception in LLM Agents Under Conflicting Incentives](https://arxiv.org/abs/2608.26372)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[AsymSpec: Context-Asymmetric Speculative Decoding for Agentic LLMs](https://arxiv.org/abs/2608.26004)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Plans You Can Check: Verifier-Grounded Learning of an Open-Weight Planner for Executable Video-Editing](https://arxiv.org/abs/2608.25622)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Selective Regenerative Decoding: Trajectory-Level Intervention for Inference-Time Reasoning](https://arxiv.org/abs/2608.24338)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Unsupervised Post-Training of Foundation Models: A Survey](https://arxiv.org/abs/2608.24982)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[PinSieve: Production Selective VLM Serving and a Governed Memory Flywheel for Enterprise Content-Quality Triage](https://arxiv.org/abs/2608.24040)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Knowing When to Ask for Help: Bayesian Self-Escalation in Hierarchical LLM Agents](https://arxiv.org/abs/2608.24087)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[The Dialect Tax: Dialectal Biases Persist throughout the Language Modeling Pipeline](https://arxiv.org/abs/2608.24952)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[ADE: Agentic Data Evolution Framework for Human-Centered Objectives](https://arxiv.org/abs/2608.23719)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[ParallelWorld: Test-Time Scaling for Embodied Reasoning](https://arxiv.org/abs/2608.22971)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams](https://arxiv.org/abs/2608.23541)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Adversarial Entropy Inflation Against Gumbel-Based Inference Verification](https://arxiv.org/abs/2608.23375)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[LongWoF-Bench: Evaluating EvoMap Genes for Verifiable Long-Workflow Tasks](https://arxiv.org/abs/2608.23200)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[FinixDoc: Rethinking Financial Document Parsing Beyond Saturated Benchmarks](https://arxiv.org/abs/2608.22842)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Learning Generalizable Behaviors for Terminal Agents](https://arxiv.org/abs/2608.22631)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-23 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Mitigating Speaker Leakage in Cascaded Multi-talker ASR with Diarization-based Transcript Correction](https://arxiv.org/abs/2608.22196)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-23 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[CONTRAMEM: Learning Self-Evolving Procedural Memory from Contrasting Multi-Model Trajectories](https://arxiv.org/abs/2608.22533)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-23 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[The Chase Is the Curriculum, the Capture Anchors the Credit: Pursuit-Evasion Self-Play for Zero-Data LLM Reasoning](https://arxiv.org/abs/2608.21871)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-22 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Beyond Success and Failure: Length-Aware Contrastive Learning for GUI Agents](https://arxiv.org/abs/2608.21830)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-22 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[MCite-RL: Towards Reliable Multimodal RAG via Citation-enhanced Agentic Reinforcement Learning](https://arxiv.org/abs/2608.21808)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-22 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[HIRA: A Human-in-the-Loop Retrieval-Augmented Cascade for Document Classification in Regulated Industries](https://arxiv.org/abs/2608.21792)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-22 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Reinforcement Learning on Benign Facts Amplifies Leakage of Memorized Private Data](https://arxiv.org/abs/2608.21727)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-22 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[DynaContext: Self-Improving Dynamic Contextualization of Optimized Prompts for Heterogeneous Parameter Extraction](https://arxiv.org/abs/2608.22014)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-22 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[FIRM-Video: Check Before You Score for Reliable Text-to-Video Reward Modeling](https://arxiv.org/abs/2608.21839)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-22 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Perturb the Thought, Not the Pixels: Latent-Space Rollout Diversification for Reinforcement Learning of Vision-Language Models](https://arxiv.org/abs/2608.21595)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-21 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Test-Time Scaling for Scientific Equation Discovery](https://arxiv.org/abs/2608.28660)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-21 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[FlavourBench: Executable Culinary Reward Maps for Language Model Evaluation and Post-Training](https://arxiv.org/abs/2608.20574)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-20 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Robo-Dopamine 2.0: History-Conditioned and OOD-Aware Process Reward Modeling for Robotic Manipulation](https://arxiv.org/abs/2608.15680)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Why Summaries Turn Neutral: Policy Attribution for Sentiment Drift in Reinforcement Learning from Human Feedback](https://arxiv.org/abs/2608.15530)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Catching Hallucinated Citations in Video-LLM Question Answering: A Self-Verification Pipeline and Verifier Ablation Study](https://arxiv.org/abs/2608.15574)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Global Federated Learning Strategies for Building Efficient Personalized Models](https://arxiv.org/abs/2608.15107)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-15 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[PRM-as-a-Judge 1.5: A Toolkit for Robot Process Assessment](https://arxiv.org/abs/2608.14284)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-14 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Bootstrapping Niche Multilingual Code Translation via Reinforcement Learning with Execution-Based Verifiable Supervision](https://arxiv.org/abs/2608.13854)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-14 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Towards Socially Compliant Navigation in Deep Reinforcement Learning via Proxemics-Based Reward Modeling](https://arxiv.org/abs/2608.12917)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-13 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[REOPD: Reliability-Adaptive Reward Extrapolation for On-Policy Distillation](https://arxiv.org/abs/2608.11698)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-12 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[MuseCritic: Learning Multi-Aspect Song Rewards through Natural-Language Aesthetic Critiques](https://arxiv.org/abs/2608.11755)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-12 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Jagged Judges: Epistemic Stability Under Perturbation, Pressure, and Persistence](https://arxiv.org/abs/2608.12645)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-12 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Large Language Models Can Follow Instructions, But Not Many at Once: Phase Transitions in Compositional Constraint Satisfaction](https://arxiv.org/abs/2608.12426)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-12 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[From Prompting to Behavioral Alignment: Personalized LLM Judges for Recommendation Evaluation](https://arxiv.org/abs/2608.11493)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Procedural Fairness Failures in RLHF from Preference Averaging](https://arxiv.org/abs/2608.10126)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[RynnValue: Scaling Robotic Value Foundation Models with Temporal Distance](https://arxiv.org/abs/2608.09853)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[UNMASK: Discovering and Causally Verifying Spurious Shortcuts in Text Classifiers](https://arxiv.org/abs/2608.09209)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Social Gym and SPaRTan: Benchmarking and Improving LLM Social Reasoning via Multi-Agent Game Tournaments](https://arxiv.org/abs/2608.09128)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Multi-Agent Reinforcement Learning via Agent-Specific Preference](https://arxiv.org/abs/2608.08604)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-09 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Quality-Diversity Stress Tests for Process Reward Models:What Archive Coverage Can and Cannot Certify](https://arxiv.org/abs/2608.08008)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-08 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Evaluator Ensembles Under Reward Hacking: Covariance Geometry and Finite-Search Guarantees](https://arxiv.org/abs/2608.08002)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-08 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Progressive Alignment of Recommender Foundation Model through Multi-Phase Post-Training](https://arxiv.org/abs/2608.06792)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-07 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[The Horizon Gap: Planning, Memory, Execution, Training, and Evaluation for Long-Horizon LLM Agents](https://arxiv.org/abs/2608.06663)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-07 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Refining Over Resampling: Test-Time Self-Correction for LLM Reasoning](https://arxiv.org/abs/2608.05643)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction](https://arxiv.org/abs/2608.06310)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Does Latent Context Help? A Controlled Evaluation of Inverse Reinforcement Learning in Arctic Shipping](https://arxiv.org/abs/2608.06105)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Cautious Context Steering for Language Model Personalization](https://arxiv.org/abs/2608.05813)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Data-DPO: Direct Preference Optimization for Target Model Data Selection in LLM Post-Training](https://arxiv.org/abs/2608.16926)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-05 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[GeoReward: Mitigating Contextual Variable Overestimation in Vision-Language Models for Cross-Market Preference Prediction](https://arxiv.org/abs/2608.04504)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-05 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Mitigating Rubric Interference in LLM Judges via On-Policy Self-Distillation](https://arxiv.org/abs/2608.14684)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-05 · `academic-query-vote` · `arxiv-backfill`

### 2023

#### May

- **[Let's Verify Step by Step](https://arxiv.org/abs/2305.20050)** — Shows that supervising intermediate reasoning steps can outperform outcome-only reward supervision for mathematical reasoning.  
  2023-05-31 · `process-reward-model` · `verifier` · `reasoning`

## Reinforcement Learning & RL with Verifiable Rewards

### 2026

#### August

- 🔎 **[GMTS: Gradient Magnitude-based Token Selection Improves RLVR Training for LLM Reasoning](https://arxiv.org/abs/2608.30632)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[When Does Predictor-Based RL Align with Human Perception? A Study of Subjective Rewards in Codec-Based Speech Language Models](https://arxiv.org/abs/2608.31035)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[InspectorGPT: A Comparative Reasoning Enhanced VLM for Comprehensive Industrial Anomaly Detection](https://arxiv.org/abs/2608.29783)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[TEMPO: Temporally-grounded Multi-task Post-training for Large Audio-Language Models](https://arxiv.org/abs/2608.29999)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[JPO: Juris Policy Optimization for Structured Legal Reasoning in Criminal Judgment Prediction](https://arxiv.org/abs/2608.29616)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[FRAMEWORKERS: A Dynamic Multi-Agent Framework for AI-Generated Video Production](https://arxiv.org/abs/2608.29814)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Program Learning with Verifiable Rewards: Symbolic Backpropagation for Post-Training LLMs](https://arxiv.org/abs/2608.28421)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Boosting LLM Exploration via Weak-Model Guidance in RLVR](https://arxiv.org/abs/2608.27420)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[AutoVerifier: Residual-Guided Non-Parametric Optimization for Reference-Based Answer Verification](https://arxiv.org/abs/2608.25637)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Where vs What: Decomposing Structural and Content Failures in LLM-Generated Structured Outputs](https://arxiv.org/abs/2608.25358)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection](https://arxiv.org/abs/2608.25243)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Contrastive Branch Policy Optimization](https://arxiv.org/abs/2608.24300)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[RePolicy: Reinforcement Learning for Safety-Policy Invocation in Agent Safeguards](https://arxiv.org/abs/2608.24275)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Task-Adaptive Rubrics for GUI Reward Modeling](https://arxiv.org/abs/2608.24174)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[FARCA: Fact-Aligned Reliability-Aware Credit Assignment for Reinforcement Learning with Factual Supervision](https://arxiv.org/abs/2608.24350)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Robust Code RL via Faulty-Code-Driven Test case Synthesis and Dense Reward Shaping](https://arxiv.org/abs/2608.24135)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Demystifying Reinforcement Learning Post-Training of Language Models](https://arxiv.org/abs/2608.24949)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[GSAR: Goal-State-Anchor Rewards for Mobile GUI Agents with Self-Evolving Data Synthesis](https://arxiv.org/abs/2608.22847)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Think with Structured Grounding: Perceptual Reinforcement Learning for Chart and Visual-Tabular Understanding](https://arxiv.org/abs/2608.22429)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-23 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Evidence-RL: Towards Evidence-intensive Visual Reasoning](https://arxiv.org/abs/2608.08021)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-08 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[CreativeInstruct: Scalably Teaching LLMs to Balance Quality, Creativity, and Diversity](https://arxiv.org/abs/2608.07460)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-07 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[On-Policy Self-Distillation without Any Supervision](https://arxiv.org/abs/2608.06296)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[GRASP: Reinforcing Language Model Anonymizers with Group Relative Policy Optimization](https://arxiv.org/abs/2608.06526)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Contextual Information Policy Optimization for Search Agents](https://arxiv.org/abs/2608.06128)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Agentic Reinforcement Learning with Observation-Calibrated Self-Distillation](https://arxiv.org/abs/2608.04788)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-05 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Teaching MLLMs to Say No: Generalized Referring Expression Comprehension via Refusal Calibrated GRPO](https://arxiv.org/abs/2608.04698)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-05 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts](https://arxiv.org/abs/2608.04962)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-05 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Recursive Synthesis for Long-Horizon Terminal Tasks](https://arxiv.org/abs/2608.05466)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-05 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Multi-Branch Policy Optimization for Multimodal Large Language Models](https://arxiv.org/abs/2608.07581)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-05 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[TACT: Taxonomy-Aligned Post-Training for Pedagogically Adaptive English Tutoring](https://arxiv.org/abs/2608.03952)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-04 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Taming the Implicit: Dual-Channel Risk-Aware Reinforcement Fine-Tuning for Continual Multimodal Post-Training](https://arxiv.org/abs/2608.03660)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-04 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SFT Conflicts, RL Coexists: A Theoretical and Empirical Analysis of Multi-Task Learning for LLMs](https://arxiv.org/abs/2608.03573)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-04 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[DocTrace: Towards Traceable Long Document VQA via Hierarchical Evidence Graph Reasoning](https://arxiv.org/abs/2608.03292)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-04 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[COMEX: A Composition-Grounded Benchmark and Learning Framework for Explainable Aesthetic Image Cropping](https://arxiv.org/abs/2608.07570)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-04 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Cooperative Coevolution for Resource-Constrained Agentic LLM Post-Training](https://arxiv.org/abs/2608.02391)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-03 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[LEAP: Lean Environment-Feedback via Adaptive Pruning for Code RL in GPU Kernel Generation](https://arxiv.org/abs/2608.01804)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-03 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Start Classifying: Categorical Critics for LLM Reinforcement Learning](https://arxiv.org/abs/2608.02181)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-03 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories](https://arxiv.org/abs/2608.02276)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-03 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[AdaThinkV: Adaptive Thinking for Token-Efficient Video Reasoning](https://arxiv.org/abs/2608.01980)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-03 · `academic-query-vote` · `arxiv-backfill`

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

- 🔎 **[Does On-Policy Distillation Really Distill? From Noisy Teacher to Self-Improvement](https://arxiv.org/abs/2608.31046)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[PaperGym: Rubric-Centered Evolution for Research-Plan Generation](https://arxiv.org/abs/2608.31119)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Call Neighbours Yourself: Graph Walks with Destination-Conditioned On-Policy Self-Distillation](https://arxiv.org/abs/2608.29588)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Influence-Directed Distillation: Solving the Diversity Bottleneck in Sampled-Token On-Policy Distillation](https://arxiv.org/abs/2608.29846)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[When Teacher Guidance Misleads: Reward-Aligned On-Policy Distillation](https://arxiv.org/abs/2608.27960)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[VISTA: Verifier-Informed Student-to-Teacher Adaptation for On-Policy Self-Distillation](https://arxiv.org/abs/2608.28306)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SpikeOPD: Stable On-Policy Distillation for Autoregressive Spiking Language Models](https://arxiv.org/abs/2608.27857)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning](https://arxiv.org/abs/2608.26550)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Consolidating RLVR Capabilities Across Domains: A Deep Dive into Fusion Paradigms](https://arxiv.org/abs/2608.27409)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[TTPO: Test-Time Policy Optimization](https://arxiv.org/abs/2608.27448)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Video-OPSD: Exploiting Privileged Visual Evidence for On-Policy Self-Distillation in Video Large Language Models](https://arxiv.org/abs/2608.27065)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Self-OPD: On-Policy Distillation for Flow Matching Models without Teacher](https://arxiv.org/abs/2608.26872)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD](https://arxiv.org/abs/2608.26735)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[PailitaoGR: Latent Think-with-Images for Generative Image Retrieval](https://arxiv.org/abs/2608.26658)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[One Symptom, Three Levers: A Critical Review of On-Policy Self-Distillation](https://arxiv.org/abs/2608.25936)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding](https://arxiv.org/abs/2608.25356)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[A Token-Level Analysis of Sampled-Token Reverse-KL On-Policy Distillation](https://arxiv.org/abs/2608.25643)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[DualOPSD: Adaptive Privileged Teachers for On-Policy Self-Distillation](https://arxiv.org/abs/2608.26019)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[On-policy Distillation with Verifiable Reward](https://arxiv.org/abs/2608.24696)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[On-Policy Self-Distillation in Diffusion Models](https://arxiv.org/abs/2608.24646)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[OPDSearch+: On-Policy Distillation with RL Refinement for Search-Augmented Reasoning](https://arxiv.org/abs/2608.24310)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[D$^3$-MOPD: Adaptive Dynamic Domain ScheDuling for Efficient Multi-Teacher Distillation](https://arxiv.org/abs/2608.24987)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[AudioLens: Multi-Perspective Speech Clustering with Reasoning Audio-Language Models](https://arxiv.org/abs/2608.25177)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[TailSieve: Partial-Rollout-Guided Tail Routing for LLM Rollouts](https://arxiv.org/abs/2608.22788)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Buried in Textual Debt: Context Pruning with Visual Evidence Preservation for MLLM Agents](https://arxiv.org/abs/2608.22963)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[WAM-OPD: On-Policy Distillation for World Action Models](https://arxiv.org/abs/2608.22364)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-23 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[DreamMimic: Learning Visuomotor Whole-Body Loco-Manipulation via World Model](https://arxiv.org/abs/2608.22278)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-23 · `academic-query-vote` · `arxiv-backfill`

- **[Step-Level On-Policy Distillation: Interpolating Between On-Policy Distillation and Supervised Fine-Tuning](https://arxiv.org/abs/2608.16333)** — Corrects student trajectories at the step level, yielding a continuum between supervised fine-tuning and fully on-policy distillation for interactive agents.  
  2026-08-17 · `on-policy-distillation` · `step-level-guidance` · `sft` · `long-horizon`

- **[SimpleOPD: Simple Tokenizer-Agnostic On-Policy Distillation for Long-Context Reasoning](https://arxiv.org/abs/2608.14277)** — Aligns shared text spans across mismatched teacher and student tokenizers while stabilizing long-context distillation with reference regularization and termination masking.  
  2026-08-14 · `on-policy-distillation` · `tokenizer-alignment` · `long-context` · `reasoning`

- **[AgentOPSD: Recursive Self-Distillation for Agentic Reinforcement Learning](https://arxiv.org/abs/2608.05987)** — Recursively aggregates teacher-student token evidence into turn-level Bayesian credit signals for long-horizon agent training without a separate critic or extra rollouts.  
  2026-08-06 · `on-policy-self-distillation` · `agentic-rl` · `temporal-credit` · `multi-turn` · [code](https://github.com/ZethWang/AgentOPSD)

- 🔎 **[Latent Reward Registers for Diffusion Preference Alignment](https://arxiv.org/abs/2608.03929)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-04 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Language-Specialized Multi-Teacher On-Policy Distillation for Multilingual LLM-Based ASR](https://arxiv.org/abs/2608.03610)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-04 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[When Teachers Mislead: Spurious-Signal-Aware On-Policy Distillation](https://arxiv.org/abs/2608.03632)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-04 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Any-OPD: Heterogeneous On-Policy Distillation for Flow-Matching Models via Representation-Space Bridging](https://arxiv.org/abs/2608.03316)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-04 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[TurnSight: Turn-Level Hindsight Self-Distillation for Tool-Integrated Reasoning](https://arxiv.org/abs/2608.04007)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-04 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SMOPD: Multi-Reward Reinforcement Learning via Specialize-and-Merge Online Policy Distillation](https://arxiv.org/abs/2608.03092)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-04 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Self-Improving Large Language Models via Progressive Experience Evolution](https://arxiv.org/abs/2608.02139)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-03 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Cross-Domain Hybrid OPD for Generalizable Search Agents](https://arxiv.org/abs/2608.02101)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-03 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[PCSD: Persistent Consistency for Self-Distillation in Agentic Reinforcement Learning](https://arxiv.org/abs/2608.01837)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-03 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Same Semantics, Different Paths: Self-Improving Alignment for Vision-Text Compression](https://arxiv.org/abs/2608.02109)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-03 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning](https://arxiv.org/abs/2608.01597)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-03 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[OPTD: On-Policy Transition Distillation with Consistency-Guided Adaptive Compression for Few-Step Diffusion Language Models](https://arxiv.org/abs/2608.02942)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-03 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Look Ahead Before You Distill: Future Trajectory Validation of Teacher Guidance for Agentic On-Policy Distillation](https://arxiv.org/abs/2608.01953)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-03 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Rubrics as Privileged Information for Open-Ended Generation](https://arxiv.org/abs/2608.02948)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-03 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[DAPD: Dual-Anchored Policy Distillation](https://arxiv.org/abs/2608.01735)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-03 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Is More Privileged Information Better? From Solution Traces to Problem-Solving Structure in Self-Distilled Reasoning](https://arxiv.org/abs/2608.01589)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-03 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Distill What the Student Can See: Fisher-Projected On-Policy Distillation for Vision-Language Models](https://arxiv.org/abs/2608.01263)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-02 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[AlphaG-OPD: Reliability-Gated Sibling Counterfactuals for On-Policy Distillation in Symbolic Alpha Factor Discovery](https://arxiv.org/abs/2608.01303)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-02 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Distill Where You Fail: Recovering Learning Signals of Negative RL-Groups from Adaptive Teacher Guidance](https://arxiv.org/abs/2608.00782)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-01 · `academic-query-vote` · `arxiv-backfill`

#### July

- **[Adaptive FastOPD: Progress-Aware Rollout Horizon Expansion for Efficient On-Policy Distillation](https://arxiv.org/abs/2607.29494)** — Expands the student rollout horizon only when learning at the current boundary plateaus, reducing wasted long-horizon sampling.  
  2026-07-31 · `on-policy-distillation` · `adaptive-horizon` · `efficiency` · `multi-turn`

- 🔎 **[Verifier-Induced Support Reshaping in On-Policy Optimization](https://arxiv.org/abs/2608.00220)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Visual Contrastive Self-Distillation](https://arxiv.org/abs/2607.21556)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-23 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[REGEN: Replay-recycling for Expert-to-Generalist distillation with Offline Reinforcement Learning](https://arxiv.org/abs/2607.19450)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-21 · `academic-query-vote` · `arxiv-backfill`

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

### 2026

#### August

- 🔎 **[S3Gym: Can LLMs Turn Self-Testing and Self-Judging into Self-Improvement?](https://arxiv.org/abs/2608.31100)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[S3C-LLM: Skill-Code Guided Agentic Language Models for Spectrum-to-Structure Elucidation](https://arxiv.org/abs/2608.30910)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[LCoT-GV: Graph Attention Networks for Verifying Long Reasoning Chains in Large Language Models](https://arxiv.org/abs/2608.30679)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[WebWorld: The Browser as a World Model for Self-Improving Web Code](https://arxiv.org/abs/2608.30530)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[GeoAgent: Evaluating VLM Geolocalization Through Embodied Navigation](https://arxiv.org/abs/2608.29483)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[DataFoundry: Evolving Data Preparators via Recursive Self-Improvement](https://arxiv.org/abs/2608.29966)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[ERR+: Sequential Entropy Resolution for Efficient and Decisive LLM Reasoning](https://arxiv.org/abs/2608.28771)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Ladders in Chaos: When, How, (and Perhaps Why) Does Test-Time Scaling Improve LLM Machine Translation](https://arxiv.org/abs/2608.28496)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[LLM-Based Agents for Software and Systems Security: Approaches, Applications, and Assessment](https://arxiv.org/abs/2608.28490)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Performance Foundations of Parallel & Distributed Reasoning Language Models](https://arxiv.org/abs/2608.27046)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Naive Prompt Optimization: Rethinking the Need for Complex Prompt Search](https://arxiv.org/abs/2608.27266)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[J-Zero: Unified Challenger--Solver--Judge Co-Evolution from Zero Data](https://arxiv.org/abs/2608.26582)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Redwood: A Frontier AI Accelerator Designed, Verified, and Deployed from Scratch in 2 Weeks by AI](https://arxiv.org/abs/2608.26418)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[ProofEvolve: Neuro-Symbolic Evolution for Formal Automated Theorem Proving](https://arxiv.org/abs/2608.26334)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[RecurSE: Bounded Recursive Self-Evaluation for LLM Rubric Judges](https://arxiv.org/abs/2608.24231)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Multi-Agent Self-Improving Reinforcement Learning for Video Reasoning](https://arxiv.org/abs/2608.28675)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[VideoHarness-RSI: Recursive Harness Self-Improvement for Long-Video Understanding with Frozen Vision-Language Models](https://arxiv.org/abs/2608.24302)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Meta$^n$: Recursive Self-Improvement through Emergent Depth](https://arxiv.org/abs/2608.24735)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Is Next-Chunk Reasoning RL Really Better than SFT? Revisiting Training Strategies under no-CoT Data](https://arxiv.org/abs/2608.23256)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[HPFA: Hypergraph-Based Paired Failure Attribution for LLM Reasoning](https://arxiv.org/abs/2608.02026)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-03 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Gaokerena: A Small Persian Medical Language Model Family](https://arxiv.org/abs/2608.00932)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-02 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Native Multilingual Chain-of-Thought Reasoning in Low-Resource Southeast Asian Languages](https://arxiv.org/abs/2608.00533)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-01 · `academic-query-vote` · `arxiv-backfill`

#### July

- 🔎 **[Translation with Thought: Difficulty-Adaptive Reasoning via Reinforcement Learning for Multi-Domain Machine Translation](https://arxiv.org/abs/2607.29287)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Cybersecurity Detection Classification with Reasoning-enabled Language Models](https://arxiv.org/abs/2607.28460)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[IndustryForge-27B: A Domain-Enhanced Multimodal Foundation Model for Industrial CAD](https://arxiv.org/abs/2607.28050)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Can Vision-Language Models Reason about AI Edits in Images?](https://arxiv.org/abs/2607.28464)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[TELLER: Dual-Path Iterative Preference Optimization for Table Entity Linking](https://arxiv.org/abs/2607.28680)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-29 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[WhisperRec: Latent Reasoning for Efficient Foundation Recommendation Models](https://arxiv.org/abs/2607.26621)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-29 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[GPT-Red: Automated Red Teaming via Self-Play at Scale](https://arxiv.org/abs/2607.26115)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[RSIBench-Data: Benchmarking Data-Centric Research for Recursive Self-Improvement](https://arxiv.org/abs/2607.25886)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Self-Authored Verification Is Unreliable in Heuristic Self-Improving Agents](https://arxiv.org/abs/2607.24300)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[CONSISTRE: A Unified Consistency-Aware Framework for Document-Level Relation Extraction with Large Language Models](https://arxiv.org/abs/2607.24312)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[From RLVR to RLSVR: Task Transformation Induces Self-Verifiable Rewards for Open-Ended LLM Self-Improvement](https://arxiv.org/abs/2607.23802)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Training Language Models to Cooperate with Inference-Time Controllers](https://arxiv.org/abs/2607.23771)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Learning as Reasoning Unfolds: Progressive Rollout Allocation for Efficient Reinforcement Learning](https://arxiv.org/abs/2607.22002)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Multimodal Language Models Benchmarked Against the NRC Reactor Operator Licensing Examination: Fine-Tuning and Retrieval Strategies](https://arxiv.org/abs/2607.22067)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-24 · `academic-query-vote` · `arxiv-backfill`

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

### 2026

#### August

- 🔎 **[Learning to Reason and Use Tools through Unsupervised Fine-Tuning in Task-Oriented Dialog Systems](https://arxiv.org/abs/2608.30426)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Strong Drafts Need Compact Memories: Long-Context Speculative Decoding with Compressed KV Cache](https://arxiv.org/abs/2608.30252)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[VisLens: Single-Pass Interpretable Visual Search for Multimodal LLMs](https://arxiv.org/abs/2608.30705)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[HiRS-Agent: A Hierarchical Multi-Agent System for Reliable Long-Horizon Remote Sensing Task Solving](https://arxiv.org/abs/2608.30672)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[AgenticRag-R1: Agentic Reinforcement Learning with Stack Memory for Multi-Step Reasoning, Retrieval and Memorizing](https://arxiv.org/abs/2608.29622)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Arkios: An Open Bilingual English-Nepali Language Model Trained From Scratch, with a Devanagari-Aware Tokenizer](https://arxiv.org/abs/2608.30092)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SearchWiki: Learning to Build and Navigate Knowledge Wikis for Active Information Seeking](https://arxiv.org/abs/2608.29953)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[When History Is Multimodal: Rethinking Context Management for Long-Horizon Agents](https://arxiv.org/abs/2608.29897)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[LiteSearch-VL: Small Multimodal Search Agents via Trajectory Distillation and Synthetic Step-DPO](https://arxiv.org/abs/2608.29357)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-29 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[ReToolSQL: Agentic Reinforcement Learning for Robust Text-to-SQL](https://arxiv.org/abs/2608.27796)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[HARTS: Efficient Agentic Reinforcement Learning for Hybrid-Attention Models over Arbitrary Rollout Trees](https://arxiv.org/abs/2608.28158)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[VICT: Verifier-Instrumented Credit Tracing for Long-Horizon LLM Agent Reinforcement Learning](https://arxiv.org/abs/2608.28128)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[WeAgent-MMSearch: Native Text-Vision Interaction for Multimodal Search Agents](https://arxiv.org/abs/2608.28062)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Learning to Use Tools: Reinforcement Learning for Tool-Integrated Mathematical Reasoning](https://arxiv.org/abs/2608.28447)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SPT: Skills as Pre-Training Data for Agentic Language Models](https://arxiv.org/abs/2608.26563)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[PILOT in the Loop: Live Self-Improvement for Long-Horizon Agents](https://arxiv.org/abs/2608.26530)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Neuro-symbolic PRM: Enhancing Scientific Reasoning via Structured Traces and Symbolic Verification](https://arxiv.org/abs/2608.26329)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Agentic Game Development as a Verifiable Trajectory Data Engine for Scaling World Models](https://arxiv.org/abs/2608.25518)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research](https://arxiv.org/abs/2608.25559)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Tunable Tool-Call Rates in LLM Agents via Representation Steering](https://arxiv.org/abs/2608.25198)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Joint Optimization of Tool Creation and Use for Large Language Model Agents](https://arxiv.org/abs/2608.24571)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[IAPO: Influence-Aware Policy Optimization for Credit Assignment in Multi-Turn Service Agents](https://arxiv.org/abs/2608.24588)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Recursive Experiential-Working Memory Evolution for Long-Horizon Agent Harnesses](https://arxiv.org/abs/2608.24876)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning](https://arxiv.org/abs/2608.23493)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Agent-G$^2$: Gaussian Guidance for Agentic Reinforcement Learning](https://arxiv.org/abs/2608.23318)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Thinking Beyond Videos: Unifying Video Reasoning and Deep Research for Open-World Video Agents](https://arxiv.org/abs/2608.23329)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

#### July

- 🔎 **[Echoverse: Deep, Evolving Environments for Training Computer-Use Agents at Scale](https://arxiv.org/abs/2607.28074)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Graph Is the Verifier: Agentic Reinforcement Learning for Interprocedural Vulnerability Detection](https://arxiv.org/abs/2607.26656)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-29 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Beyond Zooming: Learning Multi-Tool Visual Reasoning for Ultra-High-Resolution Remote Sensing](https://arxiv.org/abs/2607.25993)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[A Control System, a Dataset, and a Recipe for Making Frozen LLM Agents Learn a Domain](https://arxiv.org/abs/2607.25415)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SearchArt: Training Long-Horizon Search Agent with Scalable Synthetic and Verified Task](https://arxiv.org/abs/2607.24850)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-25 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Nanbeige4.2-3B: Unlocking Agentic Capabilities in a Compact Model](https://arxiv.org/abs/2607.22083)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[AREX: Towards a Recursively Self-Improving Agent for Deep Research](https://arxiv.org/abs/2607.21461)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-23 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[OmniReasoner: Thinking with Long Audio-Video via Native Tool Use](https://arxiv.org/abs/2607.19339)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-21 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[A Self-Evolving Default Action for Cooperative Tasks with Continuous Action Space](https://arxiv.org/abs/2607.18597)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-21 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[DocAtlas: Long-Document Understanding as Mutable-State Interaction](https://arxiv.org/abs/2608.07527)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-21 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[PRIME: Plasticity Recovery in Multi-Agent Environments for UAV-Assisted Emergency Communication Networks](https://arxiv.org/abs/2607.17922)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-20 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Structured Output Collapses Answer Diversity Across 44 Language Models](https://arxiv.org/abs/2607.18476)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-20 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Teach it to stop, not just to click](https://arxiv.org/abs/2607.17136)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-19 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[WAR: Workload-Aware Rollouts for Synchronous Agentic Reinforcement Learning](https://arxiv.org/abs/2607.17299)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-19 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[A Multi-Agent System for 5G Throughput Prediction in Multi-Operator Urban Environments](https://arxiv.org/abs/2607.16930)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-18 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[When Does Muon Help Agentic Reinforcement Learning?](https://arxiv.org/abs/2607.16169)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-17 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[ToolVerse: Unlocking Massive Environments and Long-Horizon Tasks for Agentic Reinforcement Learning](https://arxiv.org/abs/2607.15660)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-17 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[DSWorld: A Data Science World Model for Efficient Autonomous Agents](https://arxiv.org/abs/2607.15901)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-17 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[ToolSciVer: Multimodal Scientific Claim Verification with Visual Tool Augmented Reinforcement Learning](https://arxiv.org/abs/2607.16131)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-17 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Exploratory, Communicative, and Deployable: Vision-Driven Embodied Agents for Open-World Mobile Manipulation](https://arxiv.org/abs/2607.13653)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-15 · `academic-query-vote` · `arxiv-backfill`

### 2023

#### February

- **[Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)** — Lets a model generate and filter its own API-call demonstrations, then learns when and how to invoke tools.  
  2023-02-09 · `tool-use` · `self-supervision` · `api`

### 2021

#### December

- **[WebGPT: Browser-assisted question-answering with human feedback](https://arxiv.org/abs/2112.09332)** — Trains a language model to browse the web and answer with citations using demonstrations and human preference feedback.  
  2021-12-17 · `tool-use` · `browsing` · `imitation-learning` · `reward-modeling`

## Multimodal, VLM & MLLM Post-Training

### 2026

#### August

- 🔎 **[LightNav-0: Eliciting VLM Spatial Intelligence for Generalist Embodied Navigation](https://arxiv.org/abs/2608.30935)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[DICS: Exploring Data Intrinsic Consistency for Visual Instruction Selection](https://arxiv.org/abs/2608.30209)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[DreamX-Creator: Democratizing Native Audio-Video Generation at 2K Resolution](https://arxiv.org/abs/2608.31106)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Learning Where Outcomes Change:Credit-Addressable Reasoning for Multimodal Geometry](https://arxiv.org/abs/2608.30457)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Think, Look, and Revise: Inconsistency-Aware Visual Self-Correction in MLLMs](https://arxiv.org/abs/2608.29374)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-29 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[CommerceVibe: Learning to Design E-Commerce Creatives as Executable Visual Code via Dual-Feedback Reinforcement Learning](https://arxiv.org/abs/2608.27893)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[CoRe-MoE: Compact Reusable MoE for Continual Multimodal Instruction Tuning](https://arxiv.org/abs/2608.27867)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[A Survey on Rubric-Guided Reinforcement Learning for Language Models](https://arxiv.org/abs/2608.27505)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Beyond Atomic Layouts: Compositional Design Understanding with Vision-Language Models](https://arxiv.org/abs/2608.26716)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[RubricRM: Generative Reward Modeling via Dynamic Rubrics for Image Generation and Editing](https://arxiv.org/abs/2608.26956)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Reason in the Words You Speak: Idiolectal Paraphrasing Off-Policy Traces for Reasoning Distillation in VideoLLMs](https://arxiv.org/abs/2608.26684)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[LLaVAFlow: Preserving Latent Alignment Flow for Parameter-Efficient Multimodal Fine-Tuning](https://arxiv.org/abs/2608.26820)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Simple Actors and Deep Critics for Scalable Reinforcement Learning](https://arxiv.org/abs/2608.26659)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Not Just Reason, Not Just Scan: Reinforcement Learning for Proactive Scientific Error Verification over Academic Paper](https://arxiv.org/abs/2608.26596)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Video-FLAIR: Not Whether to Reason, But How](https://arxiv.org/abs/2608.26495)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[VISA: Agentic Self-Evolving Data Synthesis for Multimodal Instruction Following](https://arxiv.org/abs/2608.26013)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning](https://arxiv.org/abs/2608.25580)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning](https://arxiv.org/abs/2608.26105)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[PointRL: Learning Point-Level Vision-Language Grounding from Verifiable Annotation Evidence](https://arxiv.org/abs/2608.25299)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[AffectOmni: RL-Verifiable People-Centric Grounded Affective Reasoning for Social and Art-Related Scenes](https://arxiv.org/abs/2608.26193)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Pointing-VLA: Typed Spatial Grounding Interfaces for Vision-Language-Action Manipulation](https://arxiv.org/abs/2608.23138)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Decoupled Physical Modeling and Execution for Physics Reasoning](https://arxiv.org/abs/2608.22126)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-22 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Is Multimodal Speculative Decoding Ready for Diffusion-Based Parallel Drafting? A Survey and Empirical Diagnosis](https://arxiv.org/abs/2608.20743)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-21 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[G-CARL: Grounded Checklist-Aligned Reward Learning for Patient-Oriented Medical Report Interpretation](https://arxiv.org/abs/2608.20331)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-20 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Scaffolding Minds: Optimizing Latent Visual Target Representations for Multimodal Reasoning](https://arxiv.org/abs/2608.19669)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-20 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[PEA-DPO: Perception-Enhanced Alignment Direct Preference Optimization for MLLMs Alignment](https://arxiv.org/abs/2608.19598)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-20 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Vision-Language Models for Egocentric Video: From Hand-Object Interaction to Embodied AI](https://arxiv.org/abs/2608.18671)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-19 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Embodied-Navigator: Point, Think, Memorize, and Align for Efficient Navigation](https://arxiv.org/abs/2608.17512)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-18 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[MS-MFAD : Multimodal large language models for Face Anti-spoofing Detection](https://arxiv.org/abs/2608.17328)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-18 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Prism-GRPO: Faster VLA Policy Optimization via Splitting Same-outcome Groups](https://arxiv.org/abs/2608.17423)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-18 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Deep Thought Alignment: Trajectory-Level Latent Distillation for Video Reasoning](https://arxiv.org/abs/2608.16316)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-17 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Defake-o3: From Speculative Rationales to Verifiable Evidence for Explainable AIGI Detection](https://arxiv.org/abs/2608.16259)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-17 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[UniFed-VLM: Federated Instruction Tuning for Vision-Language Models with Multiple Heterogeneity](https://arxiv.org/abs/2608.15516)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[MINT: A Universal Zero-Shot Predictor for Transaction Data](https://arxiv.org/abs/2608.14198)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-14 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[AdvDex: Learning Dexterous Manipulation from Human Demonstrations via Joint-Aligned Actions and Adversarial Learning](https://arxiv.org/abs/2608.14028)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-14 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Beyond Correctness: Benchmarking and Aligning Response Behaviors in Hybrid-Thinking MLLMs](https://arxiv.org/abs/2608.12781)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-13 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[AutoDesign: Meta-Harness Optimization for Long-Horizon Agentic Design](https://arxiv.org/abs/2608.13560)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-13 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Dual-Stream Cross-Anchor Correction Grounding Long-Form Captions and the Domain Limits of Object-Level Anchors](https://arxiv.org/abs/2608.12746)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-13 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Context Blindness in DPO: Mitigating Object Hallucination in MLLMs via Context-Calibrated Preference Optimization](https://arxiv.org/abs/2608.12158)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-12 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Once Poisoned, Arbitrarily Controlled: A Programmable Backdoor in VLMs](https://arxiv.org/abs/2608.10959)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Multi-View Relational Distillation for Spatial Reasoning with Vision-Language Models](https://arxiv.org/abs/2608.10864)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[UniProbe: A Learnable Token-Level Hallucination Detector for Large VLMs using Multi-Structural Internal Representations](https://arxiv.org/abs/2608.10835)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SafeCap: Improving LVLM Safety with Image Captioning Reinforcement Learning](https://arxiv.org/abs/2608.10513)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Evidence-Grounded Trustworthy Multimodal Reasoning and Evaluation Benchmark in Complex Urban Scenes](https://arxiv.org/abs/2608.10954)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[TrustRoboReward: Preference-Ordered Isotonic Score Editing for Multi-Paradigm Robot Reward Models](https://arxiv.org/abs/2608.08491)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-09 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[StructReward: Efficient Structured Process Rewards for Self-Correcting Multimodal Reasoning](https://arxiv.org/abs/2608.08326)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-08 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[VTO: Visual Tool Orchestration for Video Anomaly Detection](https://arxiv.org/abs/2608.08219)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-08 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SportsGrounder: Proposal-Aided Interleaved Grounding for Dense Sports Video Reasoning](https://arxiv.org/abs/2608.07932)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-08 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[ChronoVision: Temporal Reasoning via Latent State Reconstruction](https://arxiv.org/abs/2608.05631)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[A Six-Dimensional Taxonomy of Post-Training Adaptation Techniques with Applications in AI Governance](https://arxiv.org/abs/2608.06246)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Shape Your Feed: An LLM-based Agentic System for Conversational Recommendation](https://arxiv.org/abs/2608.06632)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Learning from Failures: Retrieval-Centric CoT via Hard Negatives for Unified Multimodal Retrieval](https://arxiv.org/abs/2608.06060)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[M$^3$R-Bench: A Unified Benchmark for Evidence-Grounded Multimodal Metaphor Understanding](https://arxiv.org/abs/2608.05817)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[CARGO-VL: Counterfactual Arbitration with Risk-Constrained Group Optimization for Vision-Language Models](https://arxiv.org/abs/2608.04509)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-05 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Positive-Unlabeled Preference Optimization For Chest X-ray Report Generation](https://arxiv.org/abs/2608.05341)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-05 · `academic-query-vote` · `arxiv-backfill`

#### July

- 🔎 **[Reasoning to Regulate: Chain-of-Thought for Traffic Rule Understanding](https://arxiv.org/abs/2607.24199)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-27 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Spatial-IQ: Deconstructing Spatial Intelligence via Hierarchical Capability Tests](https://arxiv.org/abs/2607.22864)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Debiasing Text-to-Image Evaluation via Implicit Cultural Alignment Reward Modeling](https://arxiv.org/abs/2607.15740)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-17 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Direct Image-to-Modern Vietnamese Translation of Han-Nom Manuscripts via Multimodal RLHF Preference Alignment](https://arxiv.org/abs/2607.11434)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-13 · `academic-query-vote` · `arxiv-backfill`

### 2023

#### September

- **[LLaVA-RLHF: Aligning Large Multimodal Models with Factually Augmented RLHF](https://arxiv.org/abs/2309.14525)** — Adds factually grounded preference feedback and RLHF to improve multimodal helpfulness and reduce hallucination.  
  2023-09-25 · `rlhf` · `hallucination` · `multimodal-alignment`

#### April

- **[Visual Instruction Tuning](https://arxiv.org/abs/2304.08485)** — Uses language-model-generated visual instruction data to adapt a vision-language assistant end to end.  
  2023-04-17 · `instruction-tuning` · `synthetic-data` · `vlm`

## Generative Media Post-Training

### 2026

#### August

- 🔎 **[Sycophantic Agreement Transfers with Neutral Data via Contrastive Preference Optimization](https://arxiv.org/abs/2608.31079)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[DiffPDE: Masked Diffusion Language Models as PDE Solver](https://arxiv.org/abs/2608.30532)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Off-Manifold Refinement: Guiding Video Generators with a Frozen World Model](https://arxiv.org/abs/2608.29904)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[A-MADiff: Attention-Guided Multi-Agent DRL with Diffusion Policies for Memory-Aware Task Orchestration in Mobile AIGC Networks](https://arxiv.org/abs/2608.29255)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-29 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Efficient Geothermal Well-Control Optimization via Diffusion-Surrogate Reinforcement Learning](https://arxiv.org/abs/2608.28791)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-28 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[VGA-BenchV2: An Expanded Unified Benchmark and Multi-Model Framework for Evaluating Video Aesthetics and Generation Quality](https://arxiv.org/abs/2608.25452)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[FixAnything: 3D-Consistent Rendering Refinement via Video Generative Priors](https://arxiv.org/abs/2608.23549)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Scaling Reinforcement Learning for Diffusion Models via Velocity Matching](https://arxiv.org/abs/2608.23664)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-24 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Spatially-Grounded Flow Matching: Structured Source Distributions for Image Generation](https://arxiv.org/abs/2608.15452)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Aligning Human Sense: Calibrated Distributional Reward Learning for Video Generation](https://arxiv.org/abs/2608.21425)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[FMReward: Aligning and Evaluating Audio-Driven 3D Facial Animation with Human Preferences](https://arxiv.org/abs/2608.15296)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-15 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Designing Reinforcement Learning for Diffusion Models: A Unified Path-Space View](https://arxiv.org/abs/2608.14430)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-14 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[SPARED: Reasoning-Based AI-Generated Image Detection via Adversarially Edited Data](https://arxiv.org/abs/2608.12876)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-13 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[HarmoniDPO: Video-guided Audio Generation via Preference-Optimized Diffusion](https://arxiv.org/abs/2608.11913)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-12 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Beyond Trial-and-Error: Agentic Optimization for Image-to-Video Adherence](https://arxiv.org/abs/2608.12290)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-12 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[DreamFly: Causal Memory and Receding-Horizon Diffusion Planning for Aerial Vision-Language Navigation](https://arxiv.org/abs/2608.12308)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-12 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[AdvFD: Boosting Visual Generation via Adversarial Fr'echet Distance Loss](https://arxiv.org/abs/2608.11205)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[VidForensics-M1: Meta-Detection Reinforcement Learning with Verifiable Temporal Grounding for AI-Generated Video Forensics](https://arxiv.org/abs/2608.11201)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Embodied Multimodal Grounding for Open-Vocabulary Mobile Manipulation via Semantic 3D Gaussian Splatting](https://arxiv.org/abs/2608.10756)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-11 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[DreOPD: Degraded-Reference Extrapolative On-Policy Distillation for Flow-matching Models](https://arxiv.org/abs/2608.09233)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Reducing Pretraining-Generation Mismatch in Diffusion Language Models](https://arxiv.org/abs/2608.09424)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[CodecArena: Codec Quality Assessment via Visual Reinforcement Learning](https://arxiv.org/abs/2608.09139)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[FlowErase-OPD: Multi-Concept Erasure via Anchored On-Policy Distillation in Flow Matching Models](https://arxiv.org/abs/2608.07620)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-07 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[PAST: Prompt-Adaptive Sampling Termination for Efficient Diffusion Model](https://arxiv.org/abs/2608.06794)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-07 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Explore or Converge? Stage-Guided Per-Step Optimization for Diffusion Models](https://arxiv.org/abs/2608.06768)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-07 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Sample-Adaptive Latent Rewards for Uncertainty-Guided Diffusion Post-Training](https://arxiv.org/abs/2608.06125)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Vorch-Streamer: Extending Human Audio-Visual Generation to Real-Time Long-Form Streaming](https://arxiv.org/abs/2608.05663)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Robust-WAM: Bridging Generative Pretraining and Semantic Foresight in World-Action Models](https://arxiv.org/abs/2608.05903)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-06 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[ToolArtist: Tool-Using Unified Multimodal Models for Agentic Image Generation](https://arxiv.org/abs/2608.04436)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-05 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[STEP-OPD: Rethinking Output Targets and Internal Dynamics in On-Policy Distillation for Diffusion Models](https://arxiv.org/abs/2608.04887)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-05 · `academic-query-vote` · `arxiv-backfill`

### 2023

#### November

- **[Diffusion Model Alignment Using Direct Preference Optimization](https://arxiv.org/abs/2311.12908)** — Adapts direct preference optimization to diffusion likelihoods to align image generation without a learned reward model.  
  2023-11-22 · `diffusion` · `preference-optimization` · `dpo`

#### May

- **[Training Diffusion Models with Reinforcement Learning](https://arxiv.org/abs/2305.13301)** — Treats diffusion denoising as a multi-step decision process so image generators can optimize downstream rewards directly.  
  2023-05-22 · `diffusion` · `reinforcement-learning` · `ddpo`

## Embodied & VLA Post-Training

### 2026

#### August

- 🔎 **[Self-Aware Active Learning Enables Continual Improvement in Autonomous Driving](https://arxiv.org/abs/2608.29772)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-30 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[AdaVLA: Adaptive Step Flow Matching for Training-free Acceleration of Vision-Language-Action Models](https://arxiv.org/abs/2608.29208)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-29 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Beyond Pairwise Feedback: Listwise Vision-Language Supervision for Preference-Based Reward Learning](https://arxiv.org/abs/2608.25350)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[$R^3$: Training Robots to Reason in Natural Language via Reinforcement Learning](https://arxiv.org/abs/2608.26053)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[ConfAL-WM: Confidence-Guided Active Learning for Action-Conditioned World Models](https://arxiv.org/abs/2608.25572)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-26 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[TrAct: Bridging Robot Control and Visual Prediction with Visual Tracks](https://arxiv.org/abs/2608.24101)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-08-25 · `academic-query-vote` · `arxiv-backfill`

#### July

- 🔎 **[CLIFT: Turning Gemini Robotics On-Device into Humanoid Specialists via Non-Invasive Closed-Loop Iterative Fine-Tuning](https://arxiv.org/abs/2607.29172)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-31 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Athena-Brain Technical Report: An Efficient Robot Brain for General Intelligence and Embodied Interaction](https://arxiv.org/abs/2607.18985)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-21 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Reward-Driven LLM Agent Workflows: Synthesizing POMDP Routing and Self-Correction for Autonomous Decision-Making](https://arxiv.org/abs/2607.17038)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-19 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[PAVXploreRL: Physical-Action-Visual World Model Reinforcement Learning with Action Exploration](https://arxiv.org/abs/2607.16602)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-18 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[JoyNexus: Service-Oriented Multi-Tenant Post-Training for VLA Models](https://arxiv.org/abs/2607.16074)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-17 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Foresight Residual RL for Long-Horizon Robot Manipulation with Vision-Language-Action Models](https://arxiv.org/abs/2607.16506)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-17 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[HyMobileAgent: Data-Environment Co-Scaling for Efficient GUI Agents](https://arxiv.org/abs/2607.14548)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[CosFly-VLA: A Spatially Aware Vision-Language-Action Model for UAV Tracking](https://arxiv.org/abs/2607.15004)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Xiaomi-Robotics-1: Scaling Vision-Language-Action Models with over 100K Hours of Real-World Trajectories](https://arxiv.org/abs/2607.15330)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[NavCMPO: Critic-Guided MeanFlow Policy Optimization for Adaptive Navigation](https://arxiv.org/abs/2607.14643)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-16 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Joint On-and-Off Policy Learning for Vision-and-Language Navigation](https://arxiv.org/abs/2607.13461)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-15 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[S-squared-VLA: Decoupling Semantic and Spatial Streams in Vision-Language-Action Models for Autonomous Driving](https://arxiv.org/abs/2607.13926)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-15 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[ExToken: Structured Exploration for Efficient Vision-Language-Action Reinforcement Fine-tuning](https://arxiv.org/abs/2607.12931)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-14 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Learning More from Less: Reinforcement Learning from Hindsight](https://arxiv.org/abs/2607.09042)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[PAC-ACT: Post-training Actor-Critic for Action Chunking Transformers](https://arxiv.org/abs/2607.09590)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-10 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[CLAP: Direct VLM-to-VLA Adaptation via Language-Action Grounding](https://arxiv.org/abs/2607.08974)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-09 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[FlowDAgger: Human-in-the-Loop Adaptation of Generative Robot Policies in Latent Space](https://arxiv.org/abs/2607.08877)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-09 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Ego-Human Motion Prediction with 3D-Aware LLM](https://arxiv.org/abs/2607.07001)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-08 · `academic-query-vote` · `arxiv-backfill`

- 🔎 **[Optimal Transport Q-Learning for Flow Policy Steering and Acceleration](https://arxiv.org/abs/2607.06262)** — `discovery candidate`; awaiting primary-paper curation.  
  2026-07-07 · `academic-query-vote` · `arxiv-backfill`

### 2023

#### July

- **[RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818)** — Co-fine-tunes web-scale vision-language knowledge and robot trajectories by expressing actions as tokens.  
  2023-07-28 · `vla` · `co-fine-tuning` · `embodied`
<!-- PAPERS:END -->

## Paper Radar

The repository contains two complementary discovery agents:

1. the Daily Radar searches 31 direction-specific arXiv queries with pagination
   and adds Hugging Face Daily Papers popularity and code signals;
2. the Weekly Backfill Radar walks paginated arXiv results over a declared
   historical date range and persists a cursor for every taxonomy query;
3. candidate slots are balanced per direction so a high-volume topic cannot
   starve multimodal, agentic, generative-media, or embodied work;
4. both agents deduplicate curated, rejected, and already queued records and
   preserve the academic query and primary-source provenance;
5. an optional LLM judges scope, classifies direction, and drafts a
   one-sentence key idea;
6. each run opens a reviewable pull request instead of silently modifying the
   curated list.

It works without an API key. To enable semantic triage, add `OPENAI_API_KEY`
as a GitHub Actions secret. `OPENAI_MODEL` is optional.

```bash
python -m pip install -r requirements.txt
python -m radar.main --days 7
python -m radar.backfill --max-new 180
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
