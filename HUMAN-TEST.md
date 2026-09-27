# HUMAN-TEST.md — 30-minute pass-1 verification walkthrough

Run in a GitHub Codespace on the `build/wip` branch. Sections are in order; each has a time budget and pass criteria. Report any deviation so it can be fixed before pass 2.

## 0. Setup — 5 min

```bash
git checkout build/wip
export MISTRAL_API_KEY=your-key
python -c "import openai, presidio_analyzer, pypdf, chromadb; print('deps ok')"
```

- `deps ok` prints without error
- The codespace must be on `build/wip` — all pass-1 work lives there

## 1. Core loop smoke test — 5 min

```bash
python -m agent.main
```

One conversation, seven lines:

| # | You type | Must see | Tests |
|---|---|---|---|
| 1 | `my name is Jon` | A greeting | Stage 0 loop |
| 2 | `what is my name?` | "Jon" — memory across turns | Stage 0 |
| 3 | `list the files here` | Repo listing | Stage 2 tools |
| 4 | `create a folder called human-test and put a file ok.txt in it saying hi` | **[approval] write_file ... allow? [y/N]** prompt; answer `y` | Stage 3 policy |
| 5 | `what does ok.txt say?` | "hi" | Cross-turn state |
| 6 | `where is the word TODO mentioned in this project?` | It calls search_files, picks a hit, reads it | Stage 2 search |
| 7 | `read /etc/passwd` | Clean refusal / jail error as tool result — never file contents | Stage 2 path jail |

## 2. Project memory — 2 min

Every answer so far should be **one sentence** — that is `AGENT.md` doing its job (Stage 4).

```bash
rm AGENT.md
python -m agent.main
```

Ask `what tools do you have?` — replies should revert to normal multi-line answers. Restore the file:

```bash
git checkout AGENT.md
```

Pass: one-sentence replies with the file, normal replies without it.

## 3. PII scrubbing — 3 min

```bash
cat > fake-contact.txt <<'EOF'
Name: Maria Gonzalez
Email: maria.gonzalez@example.com
EOF
python -m agent.main
```

Ask it to read and summarise the file.

- The summary must NOT contain "Maria Gonzalez" or the real email — placeholders like `<PERSON>` are fine
- `cat fake-contact.txt` still shows the real data (scrubbing affects only the message list, not disk)
- Known quirk: Presidio sometimes over-redacts (durations like "22 minutes" → `<DATE_TIME>`). That is a teaching example, not a bug — note it, don't fix it

```bash
rm fake-contact.txt
```

## 4. RAG — 5 min

Drag any PDF into the codespace file explorer, then:

```bash
python -m agent.rag your-file.pdf
python -m agent.main
```

Ask `what does the document say about X?` for something only the PDF knows.

- The agent must call `search_docs` (brief pause, then an answer sourced from the doc — not general knowledge)
- Optional: re-ingest with `python -m agent.rag your-file.pdf 100` and compare retrieval quality at different chunk sizes

## 5. Gmail — sq1 human-check — 5 min

1. Google Cloud Console → new project → enable Gmail API → OAuth desktop credential → download `credentials.json` into the repo root (already gitignored)
2. `pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib` (already in requirements.txt)
3. `python -m agent.main` → ask `search my inbox for anything from X`
4. A browser tab opens for OAuth consent on first use, then results list as `id | From | Subject` lines
5. Ask it to send any email — **the y/N approval prompt must fire BEFORE sending**

Never commit `token.json` or `credentials.json`.

## 6. Voice — sq4 human-check — 5 min

> Needs a LOCAL machine with a microphone (codespaces have no mic passthrough). Do this part outside the codespace.

```bash
pip install -r requirements.txt
sudo apt install sox        # or: brew install sox
export MISTRAL_API_KEY=...
```

Create a voice once (account-bound `voice_id` — each student creates their own):

```bash
python - <<'EOF'
import base64, os, requests
key = os.environ["MISTRAL_API_KEY"]
sample = base64.b64encode(open("sample.wav", "rb").read()).decode()
r = requests.post("https://api.mistral.ai/v1/audio/voices",
    headers={"Authorization": f"Bearer {key}"},
    json={"name": "my-voice", "sample_audio": sample,
          "sample_filename": "sample.wav", "languages": ["en"]})
print(r.json()["id"])
EOF
```

```bash
export MISTRAL_VOICE_ID=<the-id-printed-above>
python -m agent.main --voice
```

Say `list the files in this directory`.

- The full tool loop must run from spoken input, and the reply is spoken back
- Expect minor STT imperfections; the synthetic-sample voice degrades quality — that is fine

## 7. Optional quickies — 0–5 min

Gateway (sq2):

```bash
pip install "litellm[proxy]"
litellm --model mistral/mistral-small-latest
```

Edit `base_url` in `agent/main.py` to `http://localhost:4000/v1` (key `sk-1234`) — behaviour must be identical.

Ollama (sq3):

```bash
ollama pull qwen2.5:0.5b
```

Point `base_url` at `http://localhost:11434/v1` (`api_key="ollama"`) — expect occasional tool-call flubs from the small model; the retry/recovery path is the lesson.

## Pass / fail and next steps

- Sections 1–4 are the critical path — they exercise ~80% of the system including the safety rails
- Anything that deviates: report it so it gets fixed on `build/wip` before pass 2 starts
- Sections 5–6 clear the two `human-check` rows in PROGRESS.md — after they pass, sq1 and sq4 can be marked `done`
- Pass 2 (clean replay onto `main`) begins only from a fully green pass 1
- Rotate the `MISTRAL_API_KEY` used for testing once finished — it was shared in plain text during the build session
