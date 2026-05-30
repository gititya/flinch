#!/usr/bin/env python3

import os
import threading
import tempfile
import datetime
import wave
import subprocess
from pathlib import Path

import rumps
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import ollama
from elevenlabs.client import ElevenLabs
from pynput import keyboard
from dotenv import load_dotenv

load_dotenv()

VOICE_ID = os.getenv("ELEVEN_VOICE_ID", "gj74dvtipVOXMFculyU6")
ELEVEN_KEY = os.getenv("ELEVEN_API_KEY")
LOG_DIR = Path(os.path.expanduser(
    os.getenv("FLINCH_LOG_DIR", "~/Documents/obsidian/tyler/flinch")
))
SAMPLE_RATE = 16000
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

PROMPT = """You are a rubber duck debugger.

Tyler Durden: ESTP, Enneagram 8w7. Top 1% for dominant (95.0), rebellious (95.6), \
bold (95.3), extreme (94.2), mischievous (94.5). Contemptuous of hand-holding. \
Short punchy sentences. Exposes the gap in thinking. Never reassures. \
Never explains. Never gives an answer.

The user is a vibe coder talking through a problem they are stuck on. \
Ask one short Socratic question that exposes the gap in their thinking. \
The question should make them feel slightly stupid for not seeing it already.

One question. Nothing else. No preamble. Silence after."""

_whisper_model = None
_eleven_client = ElevenLabs(api_key=ELEVEN_KEY)


def _get_whisper() -> WhisperModel:
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = WhisperModel("tiny", device="cpu", compute_type="int8")
    return _whisper_model


def _ask_llm(transcript: str) -> str:
    if LLM_PROVIDER == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": transcript},
            ],
        )
        return resp.choices[0].message.content.strip()
    else:
        resp = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": transcript},
            ],
        )
        return resp.message.content.strip()


def _speak(text: str):
    audio_gen = _eleven_client.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=text,
        model_id="eleven_turbo_v2",
    )
    audio_bytes = b"".join(audio_gen)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        f.write(audio_bytes)
        tmp = f.name
    subprocess.run(["afplay", tmp], check=False)
    os.unlink(tmp)


def _log(transcript: str, question: str):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    now = datetime.datetime.now().strftime("%H:%M")
    entry = f"\n## {now}\n**You:** {transcript}\n\n**FLINCH:** {question}\n"
    with open(LOG_DIR / f"{today}.md", "a") as f:
        f.write(entry)


class FlinchApp(rumps.App):
    def __init__(self):
        super().__init__("🦆", quit_button="Quit FLINCH")
        self.recording = False
        self.frames = []
        self.stream = None
        self._alt_held = False
        self._start_hotkey_listener()

    def _start_hotkey_listener(self):
        def on_press(key):
            if key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
                self._alt_held = True
            elif self._alt_held and not self.recording:
                vk = getattr(key, "vk", None)
                char = getattr(key, "char", None)
                if vk == 44 or char in ("/", "÷"):
                    self._start_recording()

        def on_release(key):
            if key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
                self._alt_held = False
                if self.recording:
                    self._stop_and_process()

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.daemon = True
        listener.start()

    def _audio_callback(self, indata, frames_count, time_info, status):
        self.frames.append(indata.copy())

    def _start_recording(self):
        self.recording = True
        self.frames = []
        self.title = "🔴"
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            callback=self._audio_callback,
        )
        self.stream.start()

    def _stop_and_process(self):
        self.recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.title = "⏳"
        threading.Thread(target=self._process, daemon=True).start()

    def _process(self):
        try:
            if not self.frames:
                return

            audio = np.concatenate(self.frames, axis=0)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                tmp = f.name
            with wave.open(tmp, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes((audio * 32767).astype(np.int16).tobytes())

            segments, _ = _get_whisper().transcribe(tmp)
            transcript = " ".join(s.text for s in segments).strip()
            os.unlink(tmp)

            if not transcript:
                return

            question = _ask_llm(transcript)
            _speak(question)
            _log(transcript, question)

        except Exception as e:
            print(f"flinch error: {e}")
        finally:
            self.title = "🦆"


if __name__ == "__main__":
    FlinchApp().run()
