import os
import re

from services.config import CONFIG


def parse_identity(filename):
    stem = os.path.splitext(filename)[0]
    match = re.match(r"^(\d+)_(.+)$", stem)
    if match:
        return int(match.group(1)), match.group(2).replace("_", " ")
    return None, stem.replace("_", " ")


class FaceEncoder:
    def __init__(self, known_faces_dir, face_lib):
        self.known_faces_dir = known_faces_dir
        self.face_lib = face_lib

    def encode_all(self):
        if not os.path.exists(self.known_faces_dir):
            print(f"Known faces directory not found: {self.known_faces_dir}")
            return []

        encoded = []
        for filename in sorted(os.listdir(self.known_faces_dir)):
            path = os.path.join(self.known_faces_dir, filename)
            if not os.path.isfile(path):
                continue
            if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            try:
                image = self.face_lib.load_image_file(path)
                embeddings = self.face_lib.face_encodings(image)
                if not embeddings:
                    print(f"No face found in {filename}, skipping.")
                    continue

                user_id, name = parse_identity(filename)
                encoded.append(
                    {
                        "label": os.path.splitext(filename)[0],
                        "user_id": user_id,
                        "name": name,
                        "encoding": embeddings[0].tolist(),
                    }
                )
                print(f"Encoded: {filename}")
            except Exception as error:
                print(f"Failed to encode {filename}: {error}")

        return encoded


class FaceDetector:
    def __init__(self, cv2_lib, face_lib):
        self.cv2 = cv2_lib
        self.face_lib = face_lib

    def capture_encoding(self):
        cap = self.cv2.VideoCapture(CONFIG.face_camera_index)
        if not cap.isOpened():
            print("[FACE][REAL] Camera is not available.")
            return None

        try:
            ok, frame = cap.read()
            if not ok:
                print("[FACE][REAL] Failed to capture frame.")
                return None

            rgb = self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2RGB)
            locations = self.face_lib.face_locations(rgb)
            encodings = self.face_lib.face_encodings(rgb, locations)
            if not encodings:
                print("[FACE][REAL] No face detected.")
                return None

            return encodings[0]
        finally:
            cap.release()


class FaceMatcher:
    def __init__(self, threshold):
        self.threshold = threshold

    def match(self, detected_encoding, known_records, face_lib):
        if detected_encoding is None:
            return None
        if not known_records:
            return None

        known_vectors = [record["encoding"] for record in known_records]
        distances = face_lib.face_distance(known_vectors, detected_encoding)
        if len(distances) == 0:
            return None

        best_idx = int(distances.argmin())
        best_distance = float(distances[best_idx])
        if best_distance > self.threshold:
            print(f"[FACE][REAL] Face detected, but no known match (distance={best_distance:.3f}).")
            return None

        return known_records[best_idx]
