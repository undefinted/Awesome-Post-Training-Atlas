# Transferable-idea workflow

Use this reference when the user wants research inspiration rather than a paper summary.

## 1. Select source mechanisms

Choose two or more mechanisms from different families or pipeline stages. Examples:

- verifier-guided feedback + multi-turn agent trajectories;
- on-policy distillation + multimodal instruction tuning;
- outcome-level rewards + embodied action traces;
- synthetic data selection + preference optimization.

Do not combine methods merely because their names are popular. State the common interface: data, signal, policy, state/trajectory, or evaluation loop.

## 2. Check compatibility

For each proposed transfer, ask:

- Does the target setting expose the same kind of feedback?
- Can the source signal be computed at the target time scale?
- Does the target model produce the states, actions, or traces the method expects?
- What changes in credit assignment, data quality, or compute cost?
- Could the method fail because the target modality has different observability or reward sparsity?

## 3. Write a falsifiable hypothesis

Use this format:

> If we transfer **[mechanism]** from **[source setting]** to **[target setting]**, while holding **[controls]** fixed, then **[measurable outcome]** should improve because **[mechanistic rationale]**.

Include a failure prediction:

> The idea is likely to fail when **[condition]**, which should appear as **[diagnostic]**.

## 4. Propose the smallest experiment

Specify:

1. baseline and one changed component;
2. data or trajectory budget;
3. primary metric and at least one quality/safety metric;
4. ablations that distinguish the mechanism from extra compute or data;
5. expected outcome and stop condition.

Keep speculative ideas clearly labeled as hypotheses. A good idea is not a claim that the source paper already validates the target setting.

## 5. Idea ledger

For multiple ideas, use:

| Idea | Source mechanisms | Target | Expected benefit | Main risk | Cheapest test | Confidence |
|---|---|---|---|---|---|---|
