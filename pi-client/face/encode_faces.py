import json
import os
import sys

import face_recognition

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.face_service import FaceEncoder

KNOWN_FACES_DIR = "/home/pi/smart-mirror/pi-client/face/known_faces"
OUTPUT_FILE = "/home/pi/smart-mirror/pi-client/face/encodings.json"


def main():
    encoder = FaceEncoder(KNOWN_FACES_DIR, face_recognition)
    encoded = encoder.encode_all()

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(encoded, file, indent=2)

    print(f"Saved {len(encoded)} encodings to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
