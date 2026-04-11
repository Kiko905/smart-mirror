import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    backend_url: str
    default_user_id: int
    face_mock_mode: bool
    voice_mock_mode: bool
    voice_enabled: bool
    speaker_enabled: bool
    display_output_enabled: bool
    runtime_config_path: Path
    runtime_state_path: Path
    reload_command: str



def _to_bool(value: str, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}



def load_settings() -> Settings:
    base_dir = Path(__file__).resolve().parent

    return Settings(
        backend_url=os.getenv("SMART_MIRROR_BACKEND_URL", "http://127.0.0.1:8000/api"),
        default_user_id=int(os.getenv("SMART_MIRROR_DEFAULT_USER_ID", "1")),
        face_mock_mode=_to_bool(os.getenv("SMART_MIRROR_FACE_MOCK_MODE"), True),
        voice_mock_mode=_to_bool(os.getenv("SMART_MIRROR_VOICE_MOCK_MODE"), True),
        voice_enabled=_to_bool(os.getenv("SMART_MIRROR_VOICE_ENABLED"), False),
        speaker_enabled=_to_bool(os.getenv("SMART_MIRROR_SPEAKER_ENABLED"), False),
        display_output_enabled=_to_bool(os.getenv("SMART_MIRROR_DISPLAY_OUTPUT_ENABLED"), True),
        runtime_config_path=Path(os.getenv("SMART_MIRROR_RUNTIME_CONFIG", str(base_dir / "runtime" / "config" / "active_layout.json"))),
        runtime_state_path=Path(os.getenv("SMART_MIRROR_RUNTIME_STATE", str(base_dir / "runtime" / "cache" / "sync_state.json"))),
        reload_command=os.getenv("SMART_MIRROR_RELOAD_COMMAND", ""),
    )
