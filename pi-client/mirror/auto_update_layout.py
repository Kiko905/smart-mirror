import argparse
import time
import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend_client import BackendApiClient
from config import load_settings
from services.sync.sync_manager import SyncManager

CHECK_INTERVAL = 15


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-id", type=int, default=1)
    parser.add_argument("--profile-id", type=int, default=None)
    parser.add_argument("--interval", type=int, default=CHECK_INTERVAL)
    return parser.parse_args()


def main():
    args = parse_args()
    settings = load_settings()
    client = BackendApiClient(settings)
    manager = SyncManager(settings, client)

    print("Starting automatic layout watcher...")

    while True:
        try:
            manager.sync_for_user(args.user_id)
        except Exception as error:
            print(f"Sync failed: {error}")

        time.sleep(args.interval)

if __name__ == "__main__":
    main()
