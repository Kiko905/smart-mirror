import json
import logging
from urllib import request, error
from typing import Any, Dict

from config import Settings


class BackendApiClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    def fetch_sync_config(self, user_id: int) -> Dict[str, Any]:
        url = f"{self.settings.backend_url}/sync/config/{user_id}"

        try:
            data = self._get_json(url)
            return data.get("data", {})
        except Exception as exc:
            logging.warning("Sync config fetch failed, using fallback payload: %s", exc)
            return self._mock_sync_payload(user_id)

    def match_face(self, probe_encoding: list[float] | None = None, mock_user_id: int | None = None) -> Dict[str, Any]:
        url = f"{self.settings.backend_url}/face-recognition/match"
        payload = {
            "use_mock": self.settings.face_mock_mode,
            "mock_user_id": mock_user_id,
            "probe_encoding": probe_encoding,
        }

        try:
            data = self._post_json(url, payload)
            return data
        except Exception as exc:
            logging.warning("Face match request failed, returning mock face response: %s", exc)
            return {
                "matched": True,
                "is_mock": True,
                "user_id": mock_user_id or self.settings.default_user_id,
                "confidence_distance": 0.0,
            }

    def _get_json(self, url: str) -> Dict[str, Any]:
        req = request.Request(url, method="GET")
        with request.urlopen(req, timeout=8) as response:
            return json.loads(response.read().decode("utf-8"))

    def _post_json(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        req = request.Request(url, data=body, method="POST")
        req.add_header("Content-Type", "application/json")

        try:
            with request.urlopen(req, timeout=8) as response:
                return json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"HTTP {exc.code}: {details}") from exc

    def _mock_sync_payload(self, user_id: int) -> Dict[str, Any]:
        return {
            "user": {"id": user_id, "name": "Mock User", "email": "mock@example.com"},
            "profile": {"id": None, "profile_name": "Default", "is_active": True},
            "layout": [
                {"module": "clock", "position": "top_left", "config": {}},
                {"module": "weather", "position": "top_right", "config": {}},
            ],
            "module_status": {
                "face_configured": True,
                "voice_enabled": self.settings.voice_enabled,
                "voice_mock_mode": self.settings.voice_mock_mode,
            },
            "sync_token": f"mock-{user_id}",
            "updated_at": None,
        }
