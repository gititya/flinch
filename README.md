# FLINCH

You've been staring at the same bug for 20 minutes. You've Googled it twice. You're about to paste your code into Claude and ask it to fix everything.

Don't.

Press ⌥/. Talk. FLINCH asks one question. You find the answer yourself.

---

You vibe code. You paste things and hope. That works until it stops working. When it stops working, you need to think, not get more suggestions.

FLINCH is a rubber duck debugger. It does not help you. It does not fix your code. It asks one question in Tyler Durden's voice that makes you feel stupid for not seeing the answer already. That is the mechanism. That is all it is.

---

## What happens

Hold ⌥/, talk through your problem, release.

Your voice gets transcribed locally. A local LLM generates one Socratic question. A voice that has lost patience with you speaks it back. Everything logs to your Obsidian vault.

Your voice never leaves your machine. Only the spoken response touches a cloud service.

---

## Requirements

- macOS
- Python 3.11+
- Ollama running with gemma3:4b pulled (`ollama pull gemma3:4b`)
- ElevenLabs account (free tier is 10K chars per month, enough)
- One accessibility permission in System Settings

---

## Setup

```bash
git clone https://github.com/gititya/flinch
cd flinch
pip install -r requirements.txt
cp .env.example .env
```

Fill in your `.env`. Then:

```bash
python flinch.py
```

macOS will ask for accessibility access on first run. Allow it. That is what makes the hotkey work everywhere. You do this once.

A duck appears in your menu bar. You are done.

---

## Keys and config

ElevenLabs API key goes in macOS Keychain, not in `.env`:

```bash
python -c "import keyring; keyring.set_password('flinch', 'eleven_api_key', 'your_key')"
```

Everything else goes in `.env`:

```
ELEVEN_VOICE_ID=gj74dvtipVOXMFculyU6

FLINCH_LOG_DIR=~/Documents/obsidian/tyler/flinch

LLM_PROVIDER=ollama
OLLAMA_MODEL=gemma3:4b

# Only if LLM_PROVIDER=openai
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
```

---

## The hotkey

⌥/ (option + slash). Hold to record, release to send.

---

## Logs

Each session appends to:

```
~/Documents/obsidian/tyler/flinch/YYYY-MM-DD.md
```

Change `FLINCH_LOG_DIR` in `.env` if your vault lives somewhere else.

---

## The voice

The default voice (`gj74dvtipVOXMFculyU6`) was designed in ElevenLabs Voice Design using a Tyler Durden character prompt. It is not in the public voice library. You can keep it or build your own at elevenlabs.io/app/voice-design.

Voice Design prompt that created it:

```
Native American English. Male, early thirties. Studio quality. Calm, detached, certain.
Mid-range voice with a slight rasp, not deep. Speaks slowly with deliberate pauses,
like each sentence is the last one he plans to say. No warmth. No performance.
Sounds like someone who already figured it out and is waiting for you to catch up.
```

---

## If you are not me

You need your own ElevenLabs account. Free tier works. Your keys go in your `.env`. Nothing is shared.

Want to use a cloud LLM instead of Ollama? Set `LLM_PROVIDER=openai` and add your OpenAI key. About $0.01 per 100 sessions. Not necessary.

A setup script for easier sharing is a v1.1 task. For now: clone, fill in `.env`, run.

---

## What FLINCH is not

It does not answer questions. It does not write code. It does not suggest solutions. It does not remember your last session.

If you want AI to fix your code, you already have Claude.
