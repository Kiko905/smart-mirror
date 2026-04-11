import hashlib

from services.face.interfaces import FaceEncoder


class MockFaceEncoder(FaceEncoder):
    def encode(self, frame: dict) -> list[float]:
        frame_key = f"{frame.get('source')}:{frame.get('frame_id')}"
        digest = hashlib.sha256(frame_key.encode("utf-8")).digest()
        return [round(byte / 255.0, 4) for byte in digest[:16]]


class FaceNetEncoder(FaceEncoder):
    def encode(self, frame: dict) -> list[float]:
        # Placeholder for real inference pipeline integration.
        return MockFaceEncoder().encode(frame)
