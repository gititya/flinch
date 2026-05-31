# SKILL.md — FLINCH

## Current status

**Phase 1: COMPLETE (2026-05-30)**
- `flinch.py` built and pushed
- All dependencies in `requirements.txt`
- ElevenLabs key in macOS Keychain (`flinch` / `eleven_api_key`)
- Venv at `/Users/aditya/venvs/flinch`
- Logs to `/Users/aditya/Documents/obsidian/tyler/flinch/YYYY-MM-DD.md`
- Repo: https://github.com/gititya/flinch

## Pending (not started)

- [x] Test end-to-end: confirmed working (2026-05-31)
- [x] Hotkey working — switched from pynput to NSEvent global monitor, trigger is right ⌘ hold-to-record
- [x] LLM switched to OpenAI gpt-4o-mini (key from macOS Keychain: service=OPENAI_API_KEY, account=mars)
- [x] Launch agent created at `~/Library/LaunchAgents/com.aditya.flinch.plist` (2026-05-31)
- [ ] ~~Add `flinch` alias~~ — not needed, launch agent handles startup
- [ ] Fix Keychain permission prompts — macOS prompts on launch agent startup; solution is "Always Allow" in Keychain Access or grant ACL to venv Python binary

## Run command (current)

```bash
source /Users/aditya/venvs/flinch/bin/activate
python /Users/aditya/Documents/Projects/flinch/flinch.py
```

## Key decisions (do not revisit without reason)

- No LiveKit — browser tab requirement rejected
- Not merged into Tyler — Tyler is mid-architectural-crisis
- Tyler Durden voice not in ElevenLabs library — designed via Voice Design, ID: `gj74dvtipVOXMFculyU6`
- keep_alive: default 5 min — user talks back-to-back, unloading between turns kills flow
- Log is for user only — duck stays stateless, no cross-session memory fed to LLM
- ElevenLabs key in macOS Keychain, not `.env`
- OpenAI key in macOS Keychain: service=`OPENAI_API_KEY`, account=`mars` — default LLM is gpt-4o-mini
- Hotkey changed from ⌥/ (pynput, broken on macOS) to right ⌘ via NSEvent global monitor
- Menu icon changed from 🦆 to ⚡; dock icon hidden via `NSApplicationActivationPolicyAccessory`
- Venv in `/Users/aditya/venvs/flinch` (consistent with all other venvs)
