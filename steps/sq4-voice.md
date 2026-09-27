# steps/sq4-voice.md — Side quest 4: voice input/output via Mistral audio

## Goal
Speech as an input/output modality on the same agent loop, using Voxtral STT and TTS.

## Do
1. On a local machine (codespaces have no microphone passthrough): install sox, set MISTRAL_API_KEY.
2. `transcribe()`: record with `sox -d out.wav`, POST to `https://api.mistral.ai/v1/audio/transcriptions` (model `voxtral-small-latest`, language "en").
3. `speak(text)`: POST to `https://api.mistral.ai/v1/audio/speech` (model `voxtral-tts`, voice "alpha"), play the returned audio with sox.
4. Add a typed/voice input mode toggle, and optionally route final answers through `speak()` in voice mode.

## Production parallels
Multiple interfaces (CLI, IDE, SDK) feeding one shared agent loop — the loop is modality-agnostic, which is the point. Simplifications: no VAD, barge-in, streaming partial transcripts, or prompted transcription.

## Test
Say "list the files in this directory" — the tool loop must run from spoken input. Confirm the codespace-hosted core path is unaffected.
