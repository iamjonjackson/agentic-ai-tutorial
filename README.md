# README — how to drive Mistral Code through the two-pass build

## One-time setup

1. Create the empty GitHub repo (private for now). Add `MISTRAL_API_KEY` as a repo Codespaces secret.
2. Copy the files in this package into the repo root:
   - `AGENTS.md` — agent conventions, read every session
   - `BUILDPLAN.md` — the two-pass method
   - `PROGRESS.md` — the resumability ledger (seed it with every step listed as `not-started`)
   - `steps/` — one file per step (the buildable tutorial)
3. Give the codespace/repo write access to itself (fine-grained PAT or GitHub CLI auth) so pushes work.
4. Open a codespace, install the Mistral Code CLI, authenticate.

## Pass 1 (one or a few sessions)

First prompt of any session — including brand-new sessions after a crash, quota stop, or codespace rebuild:

> Read AGENTS.md, BUILDPLAN.md, and PROGRESS.md. Follow the session start protocol in AGENTS.md, then continue pass 1 from the first step that is not done. Stop when PROGRESS.md is pushed and report the current state in one short paragraph.

For the first session only, use:

> Read AGENTS.md and BUILDPLAN.md. Execute Phase A and Phase B: work through every file in steps/ in order, on the build/wip branch, testing each step, updating the step files to match reality, and keeping PROGRESS.md committed and pushed after every step. When all steps pass, run the full agent once end to end and report PASS 1 COMPLETE.

If a session degrades, loops, or stalls: end it, open a new one, and use the resume prompt above. PROGRESS.md plus the pushed build/wip branch make every session resumable — the agent never needs memory of previous sessions, only the repo.

## Pass 2 (one session per step, or batch a whole stage if it stays clean)

Same resume prompt pattern, but the work step changes per prompt:

> Next step: steps/20-stage1-agent-loop.md. Same rules: read AGENTS.md, BUILDPLAN.md, PROGRESS.md, follow the session start protocol, do only this step, implement from the step file text alone, run its test, diff against build/wip, commit with the AGENTS.md format, update and push PROGRESS.md, stop.

The diff-against-build/wip check is the tutorial's own test: if the agent cannot reproduce the working state from the instructions alone, a student would hit the same gap — fix the step file, amend, and note it.

## Keeping it moving

- Expect the agent to mark Gmail (`sq1`) and voice (`sq4`) as `human-check` — those need you. Everything else in the plan is agent-testable in the codespace.
- Watch quota: every step test makes live model calls. Tests are designed to stay tiny; if you hit rate limits, wait and resume with the standard prompt.
- PROGRESS.md is the dashboard. Read it between sessions; if a step is `blocked`, decide whether to fix the environment or amend the step file.

## Finish

Tag stage boundaries (`git tag stage-0 ...`), make the repo public, push. `git log` now reads as the tutorial's table of contents, and each tag is a runnable checkpoint a learner can check out and follow.
