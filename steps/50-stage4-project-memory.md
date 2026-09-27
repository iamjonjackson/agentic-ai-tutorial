# steps/50-stage4-project-memory.md — Stage 4

## Goal
Project memory: an AGENT.md file loaded into context at session start, the CLAUDE.md/AGENTS.md pattern from Claude Code and Codex.

## Do
1. Add `load_project_memory(cwd)` to `main.py`: check for `AGENT.md` then `CLAUDE.md` in cwd, return up to 4000 chars or "".
2. At session start, if non-empty, append it as a user message before the first real turn.
3. Create a sample `AGENT.md` in the repo (e.g. "Always reply in one sentence. Prefer mkdir -p semantics. Never delete files.").

## Production parallels
This is per-project memory the user writes, not something the model learns. Real subtlety you simplify away: Claude Code delivers CLAUDE.md as conversational context, not system prompt, so compliance is probabilistic; nested-directory files load lazily as the agent explores. You load one file once, eagerly.

## Test
`python -m agent.main` — with the sample AGENT.md in place, every answer should follow its rules (one-sentence replies). Remove the file and confirm behaviour reverts.
