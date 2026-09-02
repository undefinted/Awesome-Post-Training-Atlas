# Harness interoperability

The core skill is Markdown plus one optional Python query helper. This keeps the research behavior portable across agent harnesses.

## Codex

- Install the plugin directory containing `.codex-plugin/plugin.json`.
- Codex can discover `skills/post-training-atlas/SKILL.md` and its `agents/openai.yaml` metadata.
- When the atlas repository is open, use its local YAML files and validation commands.

## Other harnesses, including DeepSeek-based harnesses

- Load `skills/post-training-atlas/SKILL.md` as a system, project, or agent instruction according to that harness’s normal skill-loading convention.
- Expose the atlas repository as the working directory or pass it to `scripts/query_atlas.py --root <repo>`.
- Read only the references needed for the selected mode.
- If the harness has no skill registry, the folder still works as a prompt bundle: the Markdown entrypoint is the contract and the Python script is the optional deterministic data interface.

Do not assume that another harness understands Codex-specific UI metadata, marketplace files, or tool names. The research contract must remain usable without them.

## Portable invocation examples

```bash
python skills/post-training-atlas/scripts/query_atlas.py \
  --root /path/to/Awesome-Post-Training-Atlas \
  --direction agentic --year 2025 --label RLVR --json
```

```text
Use the post-training-atlas skill. Track the evolution of [method family].
Use primary sources, separate reported evidence from hypotheses, and end with
transferable ideas plus the smallest falsifiable experiment.
```
