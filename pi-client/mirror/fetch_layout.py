import argparse
import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.api_service import ApiService, write_json_file
from services.config import CONFIG


def fetch_and_save_layout(user_id, profile_id=None):
    api = ApiService()
    layout_response = api.get_layout(user_id=user_id, profile_id=profile_id)
    endpoint = layout_response.get("endpoint")
    data = layout_response.get("data", {})

    payload = data.get("layout") if isinstance(data, dict) and "layout" in data else data
    write_json_file(CONFIG.layout_output_file, payload)

    print(f"Layout downloaded successfully from: {endpoint}")
    return True


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-id", type=int, default=CONFIG.mock_user_id)
    parser.add_argument("--profile-id", type=int, default=None)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    try:
        fetch_and_save_layout(user_id=arguments.user_id, profile_id=arguments.profile_id)
    except Exception as error:
        print(f"Connection error: {error}")
        sys.exit(1)
