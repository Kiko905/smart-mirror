from config import Settings
from services.voice.input_service import VoiceInputService
from services.voice.output_router import VoiceOutputRouter
from services.voice.command_handler import LocalCommandHandler


class VoiceInteractionService:
    def __init__(self, settings: Settings):
        self.input_service = VoiceInputService(settings)
        self.command_handler = LocalCommandHandler()
        self.output_router = VoiceOutputRouter(settings)

    def run_once(self, user_id: int):
        command = self.input_service.capture_command()
        response = self.command_handler.handle(command, user_id)
        self.output_router.route(response)
        return response
