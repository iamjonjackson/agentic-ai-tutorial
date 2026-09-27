# steps/10-stage0-chat-loop.md — Stage 0

## Goal
A plain multi-turn chat loop against Mistral, no tools. The outer conversation loop every agent wraps.

## Do
1. Create `agent/__init__.py` (empty) and `agent/main.py`.
2. In `main.py`: create the client with `api_key=os.environ["MISTRAL_API_KEY"]`, `base_url="https://api.mistral.ai/v1"`.
3. Implement the loop: system message ("You are a terminal assistant. Be concise."), read input, append, call `client.chat.completions.create(model="mistral-small-latest", messages=messages)`, append the reply message object, print it. Exit on "exit"/"quit".

## Production parallel
Claude Code's outer loop is exactly this; the inner tool-dispatch loop comes in Stage 1. You keep the whole message list in memory and ignore context compaction (a real simplification — production agents summarise old turns near the window limit).

## Test
`python -m agent.main` — hold a two-turn conversation ("my name is X" then "what is my name?") and confirm memory across turns. Then type `exit`.
