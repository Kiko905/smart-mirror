import json
import os
import sys
from datetime import datetime

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

from services.config import CONFIG
from services.face_service import FaceDetector, FaceMatcher
from services.flow_service import MirrorFlowService

ENCODINGS_FILE = "/home/pi/smart-mirror/pi-client/face/encodings.json"


def write_last_user(user):
    os.makedirs(os.path.dirname(CONFIG.face_last_user_file), exist_ok=True)
    with open(CONFIG.face_last_user_file, "w", encoding="utf-8") as file:
        file.write(json.dumps(user))


def recognize_user_mock():
    user = {
        "id": CONFIG.mock_user_id,
        "name": CONFIG.mock_user_name,
        "source": "mock",
        "recognized_at": datetime.utcnow().isoformat() + "Z",
    }
    print(f"[FACE][MOCK] Recognized user: {user['id']} - {user['name']}")
    return user


def _read_known_encodings():
    if not os.path.exists(ENCODINGS_FILE):
        return []

    with open(ENCODINGS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def recognize_user_real():
    try:
        import cv2
        import face_recognition
    except Exception as error:
        print(f"[FACE][REAL] Missing runtime dependency: {error}")
        return None

    known = _read_known_encodings()
    if not known:
        print("[FACE][REAL] No encodings found. Run encode_faces.py first.")
        return None

    detector = FaceDetector(cv2, face_recognition)
    matcher = FaceMatcher(CONFIG.face_distance_threshold)

    detected_encoding = detector.capture_encoding()
    match = matcher.match(detected_encoding, known, face_recognition)
    if not match:
        return None

    user = {
        "id": match.get("user_id") or CONFIG.mock_user_id,
        "name": match.get("name") or match.get("label", "Unknown"),
        "source": "real",
        "recognized_at": datetime.utcnow().isoformat() + "Z",
    }
    print(f"[FACE][REAL] Recognized user: {user['id']} - {user['name']}")
    return user


def recognize_user():
    if CONFIG.app_mode == "real":
        recognized = recognize_user_real()
        if recognized:
            return recognized
        print("[FACE] Falling back to mock recognition.")

    return recognize_user_mock()


def main():
    user = recognize_user()
    write_last_user(user)

    flow = MirrorFlowService()
    result = flow.run(user)

    print(
        f"[FLOW] Completed for user_id={user.get('id')} sync_ok={result.get('sync_ok')} "
        f"voice='{result.get('voice_command', '')}'"
    )


if __name__ == "__main__":
    main()
