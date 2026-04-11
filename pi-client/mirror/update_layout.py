import argparse
import os
import subprocess
import sys

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend_client import BackendApiClient
from config import load_settings
from services.sync.sync_manager import SyncManager

GENERATE_SCRIPT = "/home/pi/smart-mirror/pi-client/mirror/generate_config.js"


def run_command(command, description):
    print(f"\n--- {description} ---")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    return result.returncode == 0


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-id", type=int, default=1)
    parser.add_argument("--profile-id", type=int, default=None)
    parser.add_argument("--no-restart", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    settings = load_settings()
    client = BackendApiClient(settings)
    manager = SyncManager(settings, client)

    manager.sync_for_user(args.user_id)

    if not run_command(f"node {GENERATE_SCRIPT}", "Generating MagicMirror config"):
        print("\nLayout update failed.")
        return

    if not args.no_restart and settings.reload_command.strip():
        run_command(settings.reload_command, "Reloading mirror process")

    print("\nLayout update finished successfully.")

if __name__ == "__main__":
    main()
