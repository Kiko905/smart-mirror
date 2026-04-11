# Smart Mirror pi-client Run Guide

## Mock mode

### Required env values
In `.env`:

SMART_MIRROR_MODE=mock
VOICE_MODE=mock
VOICE_ENABLED=true
API_BASE_URL=http://192.168.100.11:8000

### Full flow (face -> profile/layout -> sync -> voice)

```bash
cd /home/pi/smart-mirror/pi-client
python3 face/recognize.py
```

### Layout sync only

```bash
cd /home/pi/smart-mirror/pi-client
python3 mirror/update_layout.py --user-id 1
```

## Raspberry real mode

### Prepare known faces
Put photos into `face/known_faces/` with file name pattern:

`<user_id>_<name>.jpg`

Example:

`12_Jan_Novak.jpg`

### Required env values
In `.env`:

SMART_MIRROR_MODE=real
VOICE_MODE=real
VOICE_ENABLED=true
FACE_CAMERA_INDEX=0
FACE_DISTANCE_THRESHOLD=0.5
API_BASE_URL=http://192.168.100.11:8000

### Generate face encodings

```bash
cd /home/pi/smart-mirror/pi-client
python3 face/encode_faces.py
```

### Run full flow

```bash
cd /home/pi/smart-mirror/pi-client
python3 face/recognize.py
```
