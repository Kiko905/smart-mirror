import argparse
import json
import os
import sys
from pathlib import Path

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend_client import BackendApiClient
from config import load_settings


OUTPUT_FILE = Path(PROJECT_ROOT) / "mirror" / "current_layout.json"


def fetch_and_save_layout(user_id, profile_id=None):
    settings = load_settings()
    client = BackendApiClient(settings)

    payload = client.fetch_sync_config(user_id)
    layout = payload.get("layout", [])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(layout, indent=2), encoding="utf-8")

    print(f"Layout downloaded successfully for user {user_id}.")
    return True


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-id", type=int, default=1)
    parser.add_argument("--profile-id", type=int, default=None)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    try:
        fetch_and_save_layout(user_id=arguments.user_id, profile_id=arguments.profile_id)
    except Exception as error:
        print(f"Connection error: {error}")
        sys.exit(1)
