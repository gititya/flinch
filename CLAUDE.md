# CLAUDE.md — FLINCH

## What this is

FLINCH is a macOS menu bar app. Hold ⌥/ anywhere, talk through a coding problem, release. One brutal Socratic question plays back in Tyler Durden's voice. No answers. No solutions. Logs every session to Obsidian.

## Stack

- `rumps` — menu bar (🦆 idle, 🔴 recording, ⏳ processing)
- `pynput` — global ⌥/ hotkey, hold to record, release to process
- `sounddevice` + `numpy` — mic capture
- `faster-whisper` tiny model — local STT, downloads on first run (~75MB)
- `ollama` → `gemma3:4b` — local LLM, already on device
- `elevenlabs` → voice ID `gj74dvtipVOXMFculyU6` — TTS only, key in macOS Keychain
- `afplay` — macOS native audio playback, no extra deps

## File structure

```
flinch.py          # entire app
requirements.txt
.env.example
.env               # not committed — voice ID + model config only, no secrets
.gitignore
SKILL.md
CLAUDE.md
README.md
```

## Config

- ElevenLabs key: macOS Keychain, service=`flinch`, account=`eleven_api_key`
- Everything else: `.env` (non-sensitive — voice ID, log dir, model config)
- Venv: `/Users/aditya/venvs/flinch`
- Logs: `/Users/aditya/Documents/obsidian/tyler/flinch/YYYY-MM-DD.md`

## Rules

- Single file. Do not split into modules unless it exceeds ~200 lines.
- No TypeScript. No type annotations beyond function signatures.
- Do not add error recovery that makes the duck softer — if it fails, it fails silently and resets the icon.
- The prompt is load-bearing. Do not change it without testing the character effect.
- Do not add cross-session memory to the LLM — the duck is stateless by design.
- Accessibility permission must be granted to whichever process runs flinch.py.
