# steps/sq2-gateway.md — Side quest 2: LLM gateway

## Goal
Route all model calls through a gateway (LiteLLM proxy) instead of directly to api.mistral.ai, proving provider independence with a one-line change.

## Do
1. `pip install "litellm[proxy]"`, run `litellm --model mistral/mistral-small-latest` with MISTRAL_API_KEY in its env.
2. Change the client `base_url` to `http://localhost:4000/v1` with the gateway key (`sk-1234`, LiteLLM's default master key when no `--api_key` is passed). Nothing else changes — the OpenAI-compatible interface is the point. In tests this was done without touching `agent/main.py` by overriding `main.client.base_url` / `main.client.api_key` after import; a student can equally edit the two literals in `main.py`.
3. Verify the agent works, then restart the gateway with a different model (e.g. `litellm --model mistral/open-mistral-nemo`) to prove routing by configuration — same client code, different model.

## Production parallels
One choke point for keys, rate limiting and cost tracking; provider routing and fallback; central logging, caching, and policy enforcement (e.g. the Stage 5 scrubber could move here). A full gateway deployment (DB for logs, budgets, virtual keys) is operational machinery; this is a local proxy proving the pattern.

## Test
Agent behaves identically through the gateway; flipping the gateway's model config changes the model with zero code changes.
