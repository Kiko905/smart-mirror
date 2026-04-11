# Raspberry Pi Client Layer

This folder contains the Smart Mirror runtime scripts used on Raspberry Pi.

## Run once in mock mode

Set environment variables (optional):

- `SMART_MIRROR_BACKEND_URL` (default `http://127.0.0.1:8000/api`)
- `SMART_MIRROR_DEFAULT_USER_ID` (default `1`)
- `SMART_MIRROR_FACE_MOCK_MODE` (default `true`)
- `SMART_MIRROR_VOICE_MOCK_MODE` (default `true`)
- `SMART_MIRROR_VOICE_ENABLED` (default `false`)
- `SMART_MIRROR_SPEAKER_ENABLED` (default `false`)
- `SMART_MIRROR_RELOAD_COMMAND` (optional shell command to reload mirror display)
- `SMART_MIRROR_MOCK_VOICE_COMMAND` (default `show weather`)

Then run:

```bash
python main.py
```

## Runtime flow

1. Face service identifies user (real or mock).
2. Sync manager fetches latest user config from backend and updates local runtime config.
3. Voice service captures command (real or mock), processes it, and routes output to display/speaker.
