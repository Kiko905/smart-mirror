import logging
import subprocess

from config import Settings


class VoiceOutputRouter:
    def __init__(self, settings: Settings):
        self.settings = settings

    def route(self, response: dict):
        if self.settings.display_output_enabled and response.get("display"):
            logging.info("DISPLAY OUTPUT: %s", response["display"])

        if self.settings.voice_enabled and response.get("speak") and response.get("text"):
            self._speak(response["text"])

    def _speak(self, text: str):
        if not self.settings.speaker_enabled:
            logging.info("SPEAKER OUTPUT (mock): %s", text)
            return

        try:
            subprocess.run(["espeak", text], check=False)
        except FileNotFoundError:
            logging.warning("espeak is not installed, fallback to log output")
            logging.info("SPEAKER OUTPUT (fallback): %s", text)
