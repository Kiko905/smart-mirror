import os
import sys
from datetime import datetime

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.api_service import ApiService, write_json_file
from services.config import CONFIG
from services.sync_service import SyncService
from services.voice_service import VoiceService


class MirrorFlowService:
    def __init__(self):
        self.api = ApiService()
        self.voice = VoiceService()
        self.sync = SyncService()

    def run(self, recognized_user):
        user_id = recognized_user.get("id")
        user_name = recognized_user.get("name", "User")

        self.voice.speak(f"Welcome {user_name}")

        profile = self._load_profile(user_id)
        profile_data = profile.get("data", {}) if isinstance(profile, dict) else {}
        profile_id = profile_data.get("id")

        layout = self._load_layout(user_id, profile_id)
        if layout:
            self._write_local_snapshot(profile, layout)

        sync_ok = self.sync.sync_layout(user_id=user_id, profile_id=profile_id)

        voice_command = self.voice.listen()
        voice_response = self._process_voice_command(voice_command, user_id, profile_id)
        if voice_response:
            self.voice.speak(voice_response)

        self._post_events(user_id, profile_id, user_name, sync_ok, voice_command)

        return {
            "user": recognized_user,
            "profile": profile,
            "layout": layout,
            "sync_ok": sync_ok,
            "voice_command": voice_command,
            "voice_response": voice_response,
        }

    def _process_voice_command(self, command, user_id, profile_id):
        if not command:
            return "No voice command detected."

        normalized = command.strip().lower()
        if not normalized:
            return "No voice command detected."

        if "sync" in normalized or "refresh" in normalized or "update" in normalized:
            ok = self.sync.sync_layout(user_id=user_id, profile_id=profile_id)
            if ok:
                return "Layout synced successfully."
            return "Layout sync failed."

        if "profile" in normalized:
            return "Your profile is active."

        return "Command received."

    def _load_profile(self, user_id):
        try:
            profile = self.api.get_profile(user_id)
            print(f"[FLOW] Profile loaded via endpoint: {profile.get('endpoint')}")
            return profile
        except Exception as exc:
            print(f"[FLOW] Profile loading failed: {exc}")
            return {}

    def _load_layout(self, user_id, profile_id):
        try:
            layout = self.api.get_layout(user_id, profile_id=profile_id)
            print(f"[FLOW] Layout loaded via endpoint: {layout.get('endpoint')}")
            return layout
        except Exception as exc:
            print(f"[FLOW] Layout loading failed: {exc}")
            return {}

    def _write_local_snapshot(self, profile, layout):
        profile_payload = profile.get("data", profile)
        layout_payload = layout.get("data", layout)

        write_json_file(CONFIG.profile_output_file, profile_payload)

        if isinstance(layout_payload, dict) and "layout" in layout_payload:
            write_json_file(CONFIG.layout_output_file, layout_payload["layout"])
        else:
            write_json_file(CONFIG.layout_output_file, layout_payload)

    def _post_events(self, user_id, profile_id, user_name, sync_ok, voice_command):
        now = datetime.utcnow().isoformat() + "Z"
        face_payload = {
            "user_id": user_id,
            "profile_id": profile_id,
            "user_name": user_name,
            "recognized_at": now,
            "mode": CONFIG.app_mode,
        }
        self.api.post_face_recognition_event(face_payload)

        sync_payload = {
            "user_id": user_id,
            "profile_id": profile_id,
            "synced_at": now,
            "sync_ok": sync_ok,
            "voice_command": voice_command,
            "mode": CONFIG.app_mode,
        }
        self.api.post_sync_event(sync_payload)
