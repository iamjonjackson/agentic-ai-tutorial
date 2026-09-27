import os
import subprocess
import sys

import requests

API_BASE = "https://api.mistral.ai/v1"
STT_MODEL = "voxtral-mini-2602"
TTS_MODEL = "voxtral-mini-tts-latest"
VOICE_ID = os.environ.get("MISTRAL_VOICE_ID", "")


def _api_key():
    return os.environ["MISTRAL_API_KEY"]


def record(out_path="out.wav"):
    subprocess.run(["sox", "-d", out_path], check=True)
    return out_path


def transcribe(audio_path="out.wav", language="en"):
    with open(audio_path, "rb") as f:
        reply = requests.post(
            f"{API_BASE}/audio/transcriptions",
            headers={"Authorization": f"Bearer {_api_key()}"},
            files={"file": (audio_path, f, "audio/wav")},
            data={"model": STT_MODEL, "language": language},
        )
    reply.raise_for_status()
    return reply.json()["text"]


def speak(text, out_path="reply.wav"):
    reply = requests.post(
        f"{API_BASE}/audio/speech",
        headers={"Authorization": f"Bearer {_api_key()}"},
        json={
            "model": TTS_MODEL,
            "voice_id": VOICE_ID,
            "input": text,
            "response_format": "wav",
        },
    )
    reply.raise_for_status()
    import base64

    with open(out_path, "wb") as f:
        f.write(base64.b64decode(reply.json()["audio_data"]))
    subprocess.run(["sox", out_path, "-d"], check=True)
    return out_path


def run_voice_mode():
    from agent import main

    print("(voice mode: speak after each beep; say 'exit' to quit)")
    while True:
        audio = record()
        text = transcribe(audio)
        print(f"(heard) {text}")
        if text.strip().lower() in ("exit", "quit"):
            break
        messages = [{"role": "system", "content": main.SYSTEM_MESSAGE}]
        messages.append({"role": "user", "content": text})
        import io

        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            main.run_agent(messages, max_turns=25)
        finally:
            sys.stdout = old_stdout
        speak(captured.getvalue().strip() or "(no reply)")


if __name__ == "__main__":
    run_voice_mode()
