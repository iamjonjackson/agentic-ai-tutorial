# AGENTS.md

## What this repo is

A from-scratch agentic terminal assistant, built as a teaching repo. The final commit history IS the tutorial: every commit is one small, self-contained, tested step. This file is read by the AI agent before every session.

## The two-pass method

- **Pass 1 (`build/wip` branch):** build the whole project end to end, testing as you go. Commit freely; history quality does not matter on this branch. Update the step files in `steps/` whenever reality differs from what a step file says — the step files must always match what actually works.
- **Pass 2 (`main` as an orphan branch):** replay every step file one at a time onto a clean history. This pass produces the public-facing repo.

Never mix the two passes. Never replay a step from memory of pass 1 — implement from the step file text, as a student following instructions would.

## Progress tracking (read this every session)

`PROGRESS.md` in the repo root is the single source of truth for where the build stands. It has one line per step:

`| steps/NN-....md | pass1 | not-started | build/wip a1b2c3d | |`

Status values: `not-started`, `in-progress`, `done`, `blocked (reason)`, `human-check (reason)`.

Session start protocol — always do this before anything else:

1. Read PROGRESS.md. Find the first step that is not `done`.
2. If it is `in-progress`, resume it: the repo already has the partial work; do not redo earlier steps.
3. If every line is `done` for the current pass, you are finished with that pass — report and stop.

Session rules for PROGRESS.md:

- Update the step's line to `in-progress` and commit+push PROGRESS.md BEFORE starting the step.
- Update it to `done` (or `blocked`/`human-check`) with the commit hash, and commit+push immediately after finishing the step.
- PROGRESS.md commits are exempt from the "one step per prompt" rule: updating and pushing it is always allowed and expected.

## Session rules (apply to both passes)

1. Read PROGRESS.md and the current step file before doing anything. Work only on the current step.
2. One step per prompt. Stop after committing. Do not start the next step.
3. Run the step's test command. Do not commit unless it passes. If the test cannot be automated, split it: implement with mock-based tests you can run (commit those), and mark the live check `human-check` in PROGRESS.md with what the human must verify.
4. Never amend or push commits on `main` without explicit instruction. On `build/wip`, history rewrites are fine. Push `build/wip` after every step.
5. Never commit secrets: `token.json`, `credentials.json`, `.env`, `.rag/` (embeddings are build artifacts).
6. Small diffs. If a step feels big, propose splitting the step file instead of writing a large commit.
7. If a step file is wrong or incomplete, fix the step file first (in pass 1), then proceed.
8. Keep test prompts tiny (a few tokens) — every step test makes live API calls and quota/cost are real constraints.
9. If a step fails for environmental reasons (network, quota, missing tool), mark it `blocked (reason)` in PROGRESS.md, commit+push, and move to the next non-blocked step in pass 1 only. Never silently skip.
10. Before ending any session, confirm PROGRESS.md is pushed. The next session starts from it cold.

## Commit message format (final history only)

```
Stage <n>, step <k>: <imperative summary>

<One or two sentences: what this adds and which production agent
concept it mirrors (e.g. "mirrors Claude Code's Grep tool truncation").>

Part of: Stage <n> — <stage title>
```

Stage-boundary commits are tagged `stage-0`, `stage-1`, ... and side quests `sq-1`, ...

## Reference notes

- All model calls: Mistral OpenAI-compatible endpoint, `https://api.mistral.ai/v1`, model `mistral-small-latest`, via the `openai` Python SDK. API key comes from the `MISTRAL_API_KEY` environment variable. Never hardcode keys.
- Tool results are capped and state their truncation. Guardrails are structural (policy check, path jail), never prompt-only.
