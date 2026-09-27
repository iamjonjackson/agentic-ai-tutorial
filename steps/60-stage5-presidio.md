# steps/60-stage5-presidio.md — Stage 5

## Goal
A PII scrubbing layer at the boundary where tool results enter the message list, so personal data never reaches the third-party API.

## Do
1. Create `agent/scrub.py`: instantiate `AnalyzerEngine()` and `AnonymizerEngine()`; `scrub(text)` analyses for language "en" and returns the anonymised text (placeholders like `<PERSON>`, `<EMAIL_ADDRESS>`). Note: first use downloads a spaCy model (`en-core-web-lg`, ~400 MB) — expect this.
2. In `main.py`, import scrub (`from agent.scrub import scrub`) and wrap the dispatch result before appending: `messages.append(..., "content": scrub(result))`. Optionally also scrub user input.

## Production parallels
Real deployments tune recognizers per entity and region, handle false positives, and use reversible token vaults where the task needs the data back (e.g. actually sending an email). Scrubbing addresses privacy, not prompt injection — different threats. Presidio with defaults and one-way redaction is the simplification.

## Test
Create `fake-contact.txt` with a name, email, and phone number. Ask the agent to read it. Confirm the model sees placeholders but can still summarise the content. Check the file on disk still has the real data (scrubbing affects only what enters the message list).
