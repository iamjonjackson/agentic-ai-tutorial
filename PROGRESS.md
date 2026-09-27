# PROGRESS.md — build ledger. The agent updates and pushes this after every step. This file is the resume point for any new session.

Pass 1 = build/wip build-out. Pass 2 = clean replay onto main. Update the row for the step you are on; never delete rows.

| step | pass | status | commit | notes |
|---|---|---|---|---|
| steps/00-setup.md | pass1 | done | build/wip 1a08658 | deps ok |
| steps/10-stage0-chat-loop.md | pass1 | done | build/wip 9e52cc4 | two-turn memory verified via piped input |
| steps/20-stage1-agent-loop.md | pass1 | done | build/wip 9b448bb | loop exits after one call; max_turns cap verified |
| steps/30-stage2-fs-tools.md | pass1 | done | build/wip cbc2d31 | jail amended to session start dir (cwd not under ~ in sandbox); step file updated |
| steps/31-stage2-search-tool.md | pass1 | done | build/wip 79ee8dc | search->pick->read chain verified |
| steps/40-stage3-policy.md | pass1 | done | build/wip 07674c5 | y/N prompt, deny and allow paths all verified |
| steps/50-stage4-project-memory.md | pass1 | done | build/wip 75c9944 | one-sentence rule honored; reverts without file |
| steps/60-stage5-presidio.md | pass1 | done | build/wip 7dc3b16 | model saw placeholders; disk data intact; spacy model note added to step file |
| steps/70-stage6-rag.md | pass1 | done | build/wip 1035d00 | ingest+search_docs verified; presidio false positive on '22 minutes' noted |
| steps/sq1-gmail.md | pass1 | human-check (OAuth consent + first send need a human; mock tests pass at a661b69) | build/wip a661b69 | 4 mock tests green |
| steps/sq2-gateway.md | pass1 | done | build/wip 4a7a3ca | agent identical via gateway; config flip to open-mistral-nemo verified |
| steps/sq3-ollama.md | pass1 | in-progress | | |
| steps/sq4-voice.md | pass1 | not-started | | no microphone in codespace — human-check |
| steps/00-setup.md | pass2 | not-started | | |
| steps/10-stage0-chat-loop.md | pass2 | not-started | | |
| steps/20-stage1-agent-loop.md | pass2 | not-started | | |
| steps/30-stage2-fs-tools.md | pass2 | not-started | | |
| steps/31-stage2-search-tool.md | pass2 | not-started | | |
| steps/40-stage3-policy.md | pass2 | not-started | | |
| steps/50-stage4-project-memory.md | pass2 | not-started | | |
| steps/60-stage5-presidio.md | pass2 | not-started | | |
| steps/70-stage6-rag.md | pass2 | not-started | | |
