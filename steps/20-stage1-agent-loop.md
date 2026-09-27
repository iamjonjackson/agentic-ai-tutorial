# steps/20-stage1-agent-loop.md — Stage 1

## Goal
The agent loop: model emits structured tool calls, harness executes them, results feed back, loop ends when the model answers in plain text.

## Do
1. In `main.py`, wrap the model call in `run_agent(messages, max_turns=25)`: loop up to max_turns, pass `tools=TOOLS` (empty list for now), append the reply message; if it has no `tool_calls`, print and return; else for each call, `dispatch(call)` and append `{"role": "tool", "tool_call_id": call.id, "content": result}`.
2. Define `dispatch(call)` as a stub returning `f"error: unknown tool {call.function.name}"` (real dispatch arrives in Stage 2).
3. `main()` now calls `run_agent` instead of a single completion.

## Production parallels
- Max turns per request mirrors Codex CLI's loop limits (a confused agent must not loop forever).
- Tool calls are structured (name + JSON args), never shell strings — this is the mechanism in Claude Code, Codex CLI, and Copilot agent mode.
- Real simplification: single-shot results; production deals with streaming partial tool calls and parallel tool execution.

## Test
`python -m agent.main` — ask a plain question; with no tools defined the loop exits after one model call. Temporarily set max_turns=1 to see the cap fire, then restore it.
