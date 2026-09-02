# Post-Training Atlas plugin

This directory packages the atlas as a reusable research skill.

It has two layers:

- `.codex-plugin/plugin.json` makes it discoverable as a Codex plugin.
- `skills/post-training-atlas/` contains the tool-agnostic Markdown skill, UI metadata, and focused references.

The skill is intentionally portable. In Codex, install the plugin through the normal local-plugin flow. In another harness, load `skills/post-training-atlas/SKILL.md` as a project/system instruction and make the repository root available as the atlas workspace. The instructions do not require a proprietary model or a specific MCP server.

See `skills/post-training-atlas/references/harness-interop.md` for the portable loading contract and query-script example.

## What it does

1. Tracks how post-training method families evolve instead of only counting papers.
2. Compares data, objectives, feedback, optimization, and transfer changes.
3. Extracts cautious, testable cross-method research ideas.
4. Turns a research brief into a repository-aware vibe-coding plan.
5. Preserves the atlas rules: primary-source evidence, visible candidate status, provenance, and no guessed metadata.

## Example prompts

- “Use the Post-Training Atlas to explain how GRPO-style methods changed across recent variants.”
- “Find transferable ideas between verifier training and interactive agents; separate evidence from hypotheses.”
- “Research this post-training feature, then turn it into a minimal implementation plan for this repository.”

## Repository-aware commands

When working from the atlas root, the skill can use the existing radar and validation commands documented in the main README. The plugin does not silently publish or merge updates; review remains explicit.
