# Taxonomy and inclusion policy

## Working definition

Post-training is an additional learning or feedback process applied after a
general pretrained model exists. It changes model behavior, capabilities, or
adaptation efficiency using supervised data, preferences, rewards, verifiers,
interaction, distillation, or iterative self-generated data.

## Included

- supervised instruction tuning and high-signal data selection;
- preference learning, alignment, reward modeling, and AI feedback;
- online or offline reinforcement learning, including verifiable rewards;
- reasoning distillation, self-correction, self-play, and iterative improvement;
- training agents through tools, environments, or multi-turn interaction;
- multimodal, generative-media, embodied, and VLA adaptation methods;
- evaluation work that directly diagnoses or changes a post-training decision.

## Usually excluded

- base-model pretraining without a distinct adaptation phase;
- inference-only prompting, search, or test-time compute without learning;
- ordinary downstream fine-tuning with no reusable post-training insight;
- post-training quantization (PTQ) and deployment compression without behavioral
  adaptation; these are important, but use a different meaning of the term;
- benchmark-only papers that do not inform a post-training method or decision.

Borderline papers should record an explicit inclusion rationale. Rejected
papers are retained in `data/rejected.yaml` so the radar does not repeatedly
propose them.

## Primary directions

Each paper has exactly one primary direction for navigation and may have
multiple tags for cross-cutting concepts and modalities.

| ID | Direction | Central question |
|---|---|---|
| `supervised-adaptation` | Supervised Adaptation & Data | What demonstrations or synthetic data should the model learn from? |
| `preference-alignment` | Preference Optimization & Alignment | How should comparative or scalar preferences change behavior? |
| `reward-verifiers` | Reward Models & Verifiers | How is a useful learning signal learned or checked? |
| `reinforcement-learning` | Reinforcement Learning & RLVR | How does the model learn from sampled actions and rewards? |
| `reasoning-self-improvement` | Reasoning & Self-Improvement | How are reasoning traces, critique, or iteration converted into learning? |
| `agentic` | Agentic & Interactive Post-Training | How does training incorporate tools, environments, and multi-turn trajectories? |
| `multimodal` | Multimodal, VLM & MLLM Post-Training | How are perception and language jointly adapted or aligned? |
| `generative-media` | Generative Media Post-Training | How are image, video, audio, or diffusion generators aligned? |
| `embodied-vla` | Embodied & VLA Post-Training | How does feedback improve grounded action and control? |

