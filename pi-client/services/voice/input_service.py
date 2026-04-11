import os

from config import Settings


class VoiceInputService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def capture_command(self) -> str | None:
        if self.settings.voice_mock_mode:
            return os.getenv("SMART_MIRROR_MOCK_VOICE_COMMAND", "show weather")

        # Hardware integration entrypoint for microphone capture.
        return None
