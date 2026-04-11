import argparse
import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.config import CONFIG
from services.sync_service import SyncService


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-id", type=int, default=CONFIG.mock_user_id)
    parser.add_argument("--profile-id", type=int, default=None)
    parser.add_argument("--no-restart", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    service = SyncService()
    ok = service.sync_layout(
        user_id=args.user_id,
        profile_id=args.profile_id,
        restart=not args.no_restart,
    )
    if not ok:
        print("\nLayout update failed.")
        return

    print("\nLayout update finished successfully.")

if __name__ == "__main__":
    main()
