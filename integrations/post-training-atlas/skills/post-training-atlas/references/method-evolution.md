# Method-evolution brief

Use this reference for a method-family or “what changed?” request.

## Normalize each paper

Record only what the source supports:

| Field | What to capture |
|---|---|
| Method family | The shared mechanism, not only the title acronym |
| Baseline | Closest prior method or training pipeline |
| Change axis | Data, objective, feedback/reward, sampling, optimizer, model scope, task scope, or efficiency |
| Mechanism | One or two sentences describing the actual change |
| Evidence | Dataset, benchmark, ablation, scaling result, or robustness result |
| Reported limitation | Limitation stated by the authors |
| Transfer surface | Model, task, modality, or stage where the idea may transfer |
| Confidence | High when directly supported; medium for careful comparison; low for an inference |

## Compare variants

Use a compact matrix instead of a title dump:

| Variant | What changed? | Why, according to the source? | Evidence | Cost/risk |
|---|---|---|---|---|
| Baseline | — | — | — | — |
| Variant A | ... | reported / inferred | ... | ... |
| Variant B | ... | reported / inferred | ... | ... |

Do not call two papers a method family only because they share a keyword. Require a shared training mechanism, explicit predecessor relationship, or a defensible pipeline-level correspondence.

## Explain “why” carefully

- **Reported:** the paper explicitly motivates the change or demonstrates it in an ablation.
- **Observed:** the comparison shows a consistent difference, but the authors do not establish causality.
- **Hypothesis:** a plausible explanation or transfer idea that still needs testing.

Never turn “the later paper performs better” into “the new component caused the gain” without an ablation or controlled comparison.

## Timeline wording

Prefer:

> The family moves from [baseline mechanism] toward [later mechanism]. The main changes are [axes]. The evidence is strongest for [claim]; whether the gain transfers to [new setting] remains open.

Avoid:

> This is the definitive successor / best method / final version.

## Useful labels

Use the repository’s controlled vocabulary where possible, including `OPD`, `OPSD`, `counterfactual`, `distillation`, `RLVR`, `agent`, `VLM`, and `VLA`. Add a new label only when it describes a reusable mechanism and can be defined unambiguously.
