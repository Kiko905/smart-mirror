import logging

from config import load_settings
from backend_client import BackendApiClient
from services.sync.sync_manager import SyncManager
from services.face.recognizer import FaceRecognitionService
from services.voice.voice_service import VoiceInteractionService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


class SmartMirrorRuntime:
    def __init__(self):
        self.settings = load_settings()
        self.client = BackendApiClient(self.settings)
        self.sync_manager = SyncManager(self.settings, self.client)
        self.face_service = FaceRecognitionService(self.settings, self.client)
        self.voice_service = VoiceInteractionService(self.settings)

    def run_once(self):
        user_id = self.face_service.identify_user(self.settings.default_user_id)
        sync_payload = self.sync_manager.sync_for_user(user_id)
        voice_response = self.voice_service.run_once(user_id)

        logging.info("Runtime cycle completed", extra={
            "user_id": user_id,
            "sync_token": sync_payload.get("sync_token"),
            "voice_action": voice_response.get("action"),
        })


if __name__ == "__main__":
    SmartMirrorRuntime().run_once()
