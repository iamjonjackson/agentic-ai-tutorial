# steps/sq3-ollama.md — Side quest 3: local LLM via Ollama

## Goal
Run the agent against a local model — no API key, no data leaving the machine.

## Do
1. Add the Ollama devcontainer feature: `"ghcr.io/devcontainers/features/ollama:1": {}`.
2. `ollama pull hf.co/mistralai/Ministral-3B-instruct-2412-GGUF:Q4_K_M`.
3. Swap the client: `base_url="http://localhost:11434/v1"`, `api_key="ollama"`, model name matching the pull.
4. Stress-test tool calling and add retry/error handling for malformed JSON arguments and hallucinated tool names — small local models fail at structured tool use far earlier than API models.

## Production parallels
GGUF is the quantised single-file format (Q4 ≈ 4 bits/weight, ~2GB for 3B). Ministral 3B is one of the few 3B-class models fine-tuned for function calling, Apache 2.0 licensed. Honest note: production agents use remote frontier models because tool-calling reliability is the capability most sensitive to model quality. Codespace default machines run 3B at roughly 3-8 tokens/s — fine for verifying the loop, not comfortable conversation.

## Test
The full Stage 0-2 flow works locally: ask it to list files and create a folder; expect occasional tool-call failures and confirm the retry path recovers.
