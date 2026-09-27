# steps/sq4-voice.md — Side quest 4: voice input/output via Mistral audio

## Goal
Speech as an input/output modality on the same agent loop, using Voxtral STT and TTS.

## Do
1. On a local machine (codespaces have no microphone passthrough): install sox, set MISTRAL_API_KEY.
2. `transcribe()`: record with `sox -d out.wav`, POST to `https://api.mistral.ai/v1/audio/transcriptions` (model `voxtral-mini-2602`, language "en" — reality note: `voxtral-small-latest` is a chat/audio-understanding model, not a valid transcription model name).
3. `speak(text)`: first create a voice via `POST /v1/audio/voices` (name + base64 sample audio) to get a `voice_id` — the TTS API requires a `voice_id`, there is no preset voice named "alpha" (that was the original step text; the API has changed). Then POST to `https://api.mistral.ai/v1/audio/speech` (model `voxtral-mini-tts-latest`, `voice_id`, `response_format: "wav"`); the response is JSON with base64 `audio_data`, decode and play with sox. Read the voice_id from the `MISTRAL_VOICE_ID` environment variable.
4. Add a typed/voice input mode toggle (`python -m agent.main --voice`), and optionally route final answers through `speak()` in voice mode.

## Production parallels
Multiple interfaces (CLI, IDE, SDK) feeding one shared agent loop — the loop is modality-agnostic, which is the point. Simplifications: no VAD, barge-in, streaming partial transcripts, or prompted transcription.

## Test
Say "list the files in this directory" — the tool loop must run from spoken input. Confirm the codespace-hosted core path is unaffected.
