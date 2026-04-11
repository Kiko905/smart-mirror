from config import Settings
from backend_client import BackendApiClient
from services.face.detector import MockFaceDetector, CameraFaceDetector
from services.face.encoder import MockFaceEncoder, FaceNetEncoder
from services.face.matcher import BackendFaceMatcher


class FaceRecognitionService:
    def __init__(self, settings: Settings, client: BackendApiClient):
        self.settings = settings
        self.matcher = BackendFaceMatcher(client)

        if settings.face_mock_mode:
            self.detector = MockFaceDetector()
            self.encoder = MockFaceEncoder()
        else:
            self.detector = CameraFaceDetector()
            self.encoder = FaceNetEncoder()

    def identify_user(self, fallback_user_id: int) -> int:
        frame = self.detector.capture_frame()

        if frame is None:
            return fallback_user_id

        probe_encoding = self.encoder.encode(frame)
        result = self.matcher.identify_user(probe_encoding)

        if not result.get("matched"):
            return fallback_user_id

        return int(result.get("user_id", fallback_user_id))
