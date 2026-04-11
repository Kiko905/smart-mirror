import json
import os
import requests

from services.config import CONFIG


class ApiService:
    def __init__(self):
        self.base_url = CONFIG.base_url.rstrip("/")
        self.timeout = CONFIG.api_timeout

    def _build_url(self, path):
        return f"{self.base_url}/{path.lstrip('/')}"

    def _request(self, method, path, **kwargs):
        url = self._build_url(path)
        response = requests.request(method, url, timeout=self.timeout, **kwargs)
        response.raise_for_status()
        return response

    def _first_success(self, candidates):
        last_error = None
        for method, path in candidates:
            try:
                response = self._request(method, path)
                return response.json(), path
            except Exception as exc:
                last_error = exc
        raise RuntimeError(f"No endpoint candidate matched. Last error: {last_error}")

    def get_profile(self, user_id):
        candidates = [
            ("GET", f"api/users/{user_id}/profile"),
            ("GET", f"api/profile/{user_id}"),
            ("GET", f"api/user-profile/{user_id}"),
        ]
        data, used_path = self._first_success(candidates)
        return {"data": data, "endpoint": used_path}

    def get_layout(self, user_id, profile_id=None):
        candidates = [
            ("GET", f"api/users/{user_id}/layout"),
            ("GET", f"api/mirror-layout/{user_id}"),
        ]

        if profile_id:
            candidates.insert(0, ("GET", f"api/profiles/{profile_id}/layout"))
            candidates.insert(1, ("GET", f"api/profile-layout/{profile_id}"))

        data, used_path = self._first_success(candidates)
        return {"data": data, "endpoint": used_path}

    def post_face_recognition_event(self, payload):
        candidates = [
            "api/face/recognitions",
            "api/face-recognition",
            "api/face/sync",
        ]
        for path in candidates:
            try:
                response = self._request("POST", path, json=payload)
                return {"data": response.json(), "endpoint": path}
            except Exception:
                continue
        return {"data": {"status": "skipped"}, "endpoint": None}

    def post_sync_event(self, payload):
        candidates = [
            "api/sync",
            "api/mirror/sync",
            "api/layout/sync",
        ]
        for path in candidates:
            try:
                response = self._request("POST", path, json=payload)
                return {"data": response.json(), "endpoint": path}
            except Exception:
                continue
        return {"data": {"status": "skipped"}, "endpoint": None}


def write_json_file(path, payload):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)
