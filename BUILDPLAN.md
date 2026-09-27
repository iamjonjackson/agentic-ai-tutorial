# BUILDPLAN.md — pass 1 and pass 2 instructions for the AI agent

You are working in a fresh repo that will become a teaching-quality tutorial: an agentic terminal assistant built from scratch, where the final commit history doubles as the tutorial. Work in two passes exactly as described in AGENTS.md.

## Phase A: scaffold

1. Create the `.devcontainer/devcontainer.json` from steps/00-setup.md, plus `.gitignore`, PROGRESS.md, and the AGENTS.md file.
2. Create branch `build/wip` and do all further work there.
3. Commit and push ("scaffold: devcontainer, gitignore, AGENTS.md, PROGRESS.md").

## Phase B: build and write step files together (pass 1)

Work through the step files in `steps/` in order. For each:

1. Set the step to `in-progress` in PROGRESS.md; commit and push PROGRESS.md.
2. Read the step file. Implement it fully in the codebase.
3. Run the step's test command. Fix until it passes.
4. Commit on `build/wip` with any message (history quality does not matter here) and push.
5. Update the step file so its instructions exactly match what you just built (imports, paths, exact commands, expected output). If you needed anything not in the file, the file is wrong — fix it. If you discovered a missing step, create a new step file.
6. Set the step to `done` (or `blocked`/`human-check`) in PROGRESS.md with the commit hash; commit and push.

When all step files are done and every test passes, run the full agent end to end once more, then say PASS 1 COMPLETE and stop. Do not start pass 2 in the same session.

## Phase C: replay onto clean history (pass 2, separate sessions)

1. Verify `build/wip` is fully green.
2. `git checkout --orphan main`, clear the index, and re-add AGENTS.md, steps/, PROGRESS.md, .devcontainer, .gitignore, requirements.txt as the first commit ("step 0: scaffold").
3. For each step file in order, one step per prompt:
   - Mark it `in-progress` in PROGRESS.md; commit and push PROGRESS.md (PROGRESS.md may live on `build/wip` or a `progress` branch if you want main's history pristine — ask the human which).
   - Read only that step file. Implement it from the file text alone, not from memory of pass 1.
   - Run the step's test. It must pass.
   - Diff the working tree against `build/wip`. If meaningful differences appear, the step file has a gap — fix the step file, amend your step commit, and note the gap for the human.
   - Commit with the AGENTS.md commit format, push, update PROGRESS.md to `done`, push. Stop and wait for the next prompt.
4. Tag the last commit of each stage (`stage-0` … `stage-6`, `sq-1` …).
5. Push `main` only when the human explicitly says to.

## Failure and recovery

- If the environment or tools fail mid-step (network, quota, missing dependency), mark the step `blocked (reason)` in PROGRESS.md, commit and push, and stop cleanly. Do not thrash.
- Never leave a session without PROGRESS.md pushed. A session that ends without a pushed ledger is a lost session.
- On resume, trust PROGRESS.md and the repo state, not your memory. If PROGRESS.md and the code disagree, PROGRESS.md wins; report the discrepancy.
