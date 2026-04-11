from services.config import CONFIG


class VoiceService:
    def __init__(self):
        self.enabled = CONFIG.voice_enabled
        self.mode = CONFIG.voice_mode

    def speak(self, text):
        if not self.enabled:
            return

        if self.mode == "mock":
            print(f"[VOICE][MOCK][OUT] {text}")
            return

        print(f"[VOICE][REAL][OUT] {text}")

    def listen(self):
        if not self.enabled:
            return ""

        if self.mode == "mock":
            command = CONFIG.voice_mock_input
            print(f"[VOICE][MOCK][IN] {command}")
            return command

        print("[VOICE][REAL][IN] Real microphone mode is not configured; returning empty input.")
        return ""
