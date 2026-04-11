import argparse
import time
import hashlib
import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.config import CONFIG
from services.sync_service import SyncService

LAYOUT_FILE = CONFIG.layout_output_file

CHECK_INTERVAL = 15

def file_hash(path):
    if not os.path.exists(path):
        return None

    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-id", type=int, default=CONFIG.mock_user_id)
    parser.add_argument("--profile-id", type=int, default=None)
    parser.add_argument("--interval", type=int, default=CHECK_INTERVAL)
    return parser.parse_args()

def main():
    args = parse_args()
    sync = SyncService()

    print("Starting automatic layout watcher...")

    last_hash = file_hash(LAYOUT_FILE)

    while True:
        ok_fetch = sync.fetch_layout(
            user_id=args.user_id,
            profile_id=args.profile_id,
        )

        if ok_fetch:
            new_hash = file_hash(LAYOUT_FILE)

            if new_hash != last_hash:
                print("Layout change detected.")
                if sync.generate_config() and sync.restart_magicmirror():
                    last_hash = new_hash
                    print("MagicMirror updated.")
                else:
                    print("MagicMirror update failed.")
            else:
                print("No layout change detected.")
        else:
            print("Layout fetch failed. Retrying on next interval.")

        time.sleep(args.interval)

if __name__ == "__main__":
    main()
