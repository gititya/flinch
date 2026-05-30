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

- [ ] Test end-to-end: grant accessibility, press ⌥/, confirm response plays and logs
- [ ] Verify ⌥/ hotkey fires correctly (pynput vk=44 + alt modifier)
- [ ] Set up launch agent so FLINCH starts on login (removes Terminal dependency)
- [ ] Add `flinch` alias to `~/.zshrc` as interim run command
- [ ] Re-grant accessibility permission to launch agent process (after launch agent set up)

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
- Venv in `/Users/aditya/venvs/flinch` (consistent with all other venvs)
