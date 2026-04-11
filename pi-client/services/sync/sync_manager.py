import json
import logging
import subprocess
from pathlib import Path

from config import Settings
from backend_client import BackendApiClient


class SyncManager:
    def __init__(self, settings: Settings, client: BackendApiClient):
        self.settings = settings
        self.client = client

    def sync_for_user(self, user_id: int) -> dict:
        payload = self.client.fetch_sync_config(user_id)
        previous_token = self._load_state_token()
        current_token = payload.get("sync_token")

        if current_token and current_token == previous_token:
            logging.info("No config change detected for user %s", user_id)
            return payload

        self._write_runtime_config(payload)
        self._save_state_token(current_token)
        self._reload_display()

        logging.info("Config synced for user %s", user_id)
        return payload

    def _write_runtime_config(self, payload: dict):
        path = self.settings.runtime_config_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _load_state_token(self) -> str | None:
        path = self.settings.runtime_state_path

        if not path.exists():
            return None

        try:
            state = json.loads(path.read_text(encoding="utf-8"))
            return state.get("sync_token")
        except json.JSONDecodeError:
            return None

    def _save_state_token(self, token: str | None):
        path = self.settings.runtime_state_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"sync_token": token}, indent=2), encoding="utf-8")

    def _reload_display(self):
        command = self.settings.reload_command.strip()

        if not command:
            return

        subprocess.run(command, shell=True, check=False)
