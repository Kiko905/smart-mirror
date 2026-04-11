import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_PATH = os.path.join(BASE_DIR, ".env")


def _load_env_file(path):
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    _load_env_file(ENV_PATH)


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_int(name, default=0):
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def env_float(name, default=0.0):
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


class AppConfig:
    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
        self.api_timeout = env_int("API_TIMEOUT_SECONDS", 10)
        self.app_mode = os.getenv("SMART_MIRROR_MODE", "mock").strip().lower()

        self.mock_user_id = env_int("MOCK_RECOGNIZED_USER_ID", 1)
        self.mock_user_name = os.getenv("MOCK_RECOGNIZED_USER_NAME", "Mock User")
        self.face_camera_index = env_int("FACE_CAMERA_INDEX", 0)
        self.face_distance_threshold = env_float("FACE_DISTANCE_THRESHOLD", 0.5)

        self.voice_enabled = env_bool("VOICE_ENABLED", True)
        self.voice_mode = os.getenv("VOICE_MODE", self.app_mode).strip().lower()
        self.voice_mock_input = os.getenv("VOICE_MOCK_INPUT", "show my layout")

        self.face_last_user_file = os.getenv(
            "FACE_LAST_USER_FILE",
            "/home/pi/smart-mirror/pi-client/face/last_user.txt",
        )
        self.layout_output_file = os.getenv(
            "LAYOUT_OUTPUT_FILE",
            "/home/pi/smart-mirror/pi-client/mirror/current_layout.json",
        )
        self.profile_output_file = os.getenv(
            "PROFILE_OUTPUT_FILE",
            "/home/pi/smart-mirror/pi-client/mirror/current_profile.json",
        )

        self.magicmirror_restart = env_bool("MAGICMIRROR_RESTART", True)
        self.magicmirror_restart_cmd = os.getenv("MAGICMIRROR_RESTART_CMD", "pm2 restart magicmirror")


CONFIG = AppConfig()
